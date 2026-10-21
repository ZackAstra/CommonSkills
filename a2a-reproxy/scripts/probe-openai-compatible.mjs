#!/usr/bin/env node
/**
 * Probe an OpenAI-compatible endpoint (including local A2A bridges).
 *
 * Usage:
 *   node probe-openai-compatible.mjs --base http://127.0.0.1:8787/v1 --model <id>
 *   node probe-openai-compatible.mjs --base ... --model ... --image ./fixture.png --stream
 *
 * Exit codes: 0 = HTTP success + non-empty content, 1 = failure, 2 = usage error.
 * Never prints the API key or image data.
 */

import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';

const EXIT_OK = 0;
const EXIT_FAIL = 1;
const EXIT_USAGE = 2;

const MIME = {
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.gif': 'image/gif',
  '.bmp': 'image/bmp',
};

function usage() {
  console.log(`Probe an OpenAI-compatible endpoint.

Options:
  --base <url>          Base URL including /v1 (default: http://127.0.0.1:8787/v1)
  --key <token>         Bearer token (default: $OPENAI_API_KEY or "local-placeholder")
  --model <id>          Model ID (default: first model returned by /models)
  --prompt <text>       Prompt (default: "Reply with exactly: BRIDGE_OK_7319")
  --image <path>        Attach an image (sent as a data URL)
  --stream              Use SSE streaming
  --max-tokens <n>      Output cap (default: 64)
  --timeout <sec>       Request timeout (default: 120)
  --skip-models         Do not call /v1/models
  --strict              Fail on warnings as well as errors
  --json                Machine-readable output
  --help                Show this help
`);
}

function parseArgs(argv) {
  const opts = {
    base: 'http://127.0.0.1:8787/v1',
    key: process.env.OPENAI_API_KEY || 'local-placeholder',
    model: '',
    prompt: 'Reply with exactly: BRIDGE_OK_7319',
    image: '',
    stream: false,
    maxTokens: 64,
    timeoutSec: 120,
    skipModels: false,
    strict: false,
    json: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      if (i + 1 >= argv.length) throw new Error(`Missing value for ${arg}`);
      i += 1;
      return argv[i];
    };
    switch (arg) {
      case '--base': opts.base = next(); break;
      case '--key': opts.key = next(); break;
      case '--model': opts.model = next(); break;
      case '--prompt': opts.prompt = next(); break;
      case '--image': opts.image = next(); break;
      case '--stream': opts.stream = true; break;
      case '--max-tokens': opts.maxTokens = Number(next()); break;
      case '--timeout': opts.timeoutSec = Number(next()); break;
      case '--skip-models': opts.skipModels = true; break;
      case '--strict': opts.strict = true; break;
      case '--json': opts.json = true; break;
      case '--help': case '-h': usage(); process.exit(EXIT_OK); break;
      default: throw new Error(`Unknown argument: ${arg}`);
    }
  }

  opts.base = opts.base.replace(/\/+$/, '');
  if (!/^https?:\/\//i.test(opts.base)) throw new Error('--base must start with http:// or https://');
  if (!Number.isFinite(opts.maxTokens) || opts.maxTokens <= 0) throw new Error('--max-tokens must be positive');
  if (!Number.isFinite(opts.timeoutSec) || opts.timeoutSec <= 0) throw new Error('--timeout must be positive');
  return opts;
}

function authHeaders(key) {
  return key ? { Authorization: `Bearer ${key}` } : {};
}

function errorMessage(error) {
  if (!error) return 'unknown error';
  if (error.name === 'TimeoutError') return 'request timed out';
  if (error.name === 'AbortError') return 'request aborted';
  const cause = error.cause?.code || error.cause?.message;
  return cause ? `${error.message} (${cause})` : error.message;
}

async function fetchText(url, options, timeoutMs) {
  const response = await fetch(url, {
    ...options,
    signal: AbortSignal.timeout(timeoutMs),
  });
  const text = await response.text();
  return { response, text };
}

function parseJson(text) {
  try {
    return { value: JSON.parse(text), error: null };
  } catch (error) {
    return { value: null, error };
  }
}

function contentToText(content) {
  if (typeof content === 'string') return content;
  if (!Array.isArray(content)) return content == null ? '' : JSON.stringify(content);
  return content.map((part) => {
    if (typeof part === 'string') return part;
    return part?.text ?? part?.content ?? '';
  }).join('');
}

function normalizeUsage(usage) {
  if (!usage) return null;
  const prompt = usage.prompt_tokens ?? usage.input_tokens ?? usage.promptTokens;
  const completion = usage.completion_tokens ?? usage.output_tokens ?? usage.completionTokens;
  const total = usage.total_tokens ?? usage.totalTokens;
  const cached = usage.prompt_tokens_details?.cached_tokens
    ?? usage.cache_read_input_tokens
    ?? usage.cached_tokens;
  return {
    prompt_tokens: prompt ?? null,
    completion_tokens: completion ?? null,
    total_tokens: total ?? null,
    cached_tokens: cached ?? null,
    raw: usage,
  };
}

function imageDataUrl(buffer, filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const mime = MIME[ext];
  if (!mime) throw new Error(`Unsupported image extension: ${ext || '(none)'}`);
  return `data:${mime};base64,${buffer.toString('base64')}`;
}

async function readModels(opts, warnings) {
  const result = { status: null, ok: false, ids: [], error: null };
  try {
    const { response, text } = await fetchText(
      `${opts.base}/models`,
      { headers: { Accept: 'application/json', ...authHeaders(opts.key) } },
      opts.timeoutSec * 1000,
    );
    result.status = response.status;
    result.ok = response.ok;
    const parsed = parseJson(text);
    if (parsed.value?.data && Array.isArray(parsed.value.data)) {
      result.ids = parsed.value.data.map((item) => item?.id).filter(Boolean);
    } else {
      warnings.push('GET /models returned a non-standard body');
    }
    if (!response.ok) {
      result.error = `HTTP ${response.status}: ${text.slice(0, 300)}`;
    }
  } catch (error) {
    result.error = errorMessage(error);
    warnings.push(`GET /models failed: ${result.error}`);
  }
  return result;
}

function collectAssistant(message, state) {
  if (!message) return;
  const content = contentToText(message.content);
  if (content) state.content += content;
  if (message.reasoning_content) state.reasoning += message.reasoning_content;
  if (message.reasoning) state.reasoning += message.reasoning;
  if (Array.isArray(message.tool_calls) && message.tool_calls.length > 0) {
    state.toolCalls = message.tool_calls;
  }
}

async function consumeStream(response, state) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let done = false;

  while (!done) {
    const { value, done: readerDone } = await reader.read();
    if (readerDone) break;
    buffer += decoder.decode(value, { stream: true });
    buffer = buffer.replace(/\r\n/g, '\n');

    let boundary = buffer.indexOf('\n\n');
    while (boundary >= 0) {
      const frame = buffer.slice(0, boundary);
      buffer = buffer.slice(boundary + 2);
      boundary = buffer.indexOf('\n\n');

      for (const line of frame.split('\n')) {
        if (!line.startsWith('data:')) continue;
        const payload = line.slice(5).trim();
        if (!payload) continue;
        if (payload === '[DONE]') {
          done = true;
          break;
        }
        const parsed = parseJson(payload);
        if (parsed.error) {
          state.warnings.push(`Malformed SSE frame: ${payload.slice(0, 120)}`);
          continue;
        }
        const chunk = parsed.value;
        state.events += 1;
        if (chunk?.model) state.echoModel = chunk.model;
        if (chunk?.usage) state.usage = normalizeUsage(chunk.usage);
        const choice = chunk?.choices?.[0];
        if (!choice) continue;
        const delta = choice.delta ?? choice.message;
        if (delta) {
          const text = contentToText(delta.content);
          if (text) state.content += text;
          if (delta.reasoning_content) state.reasoning += delta.reasoning_content;
          if (delta.reasoning) state.reasoning += delta.reasoning;
          if (Array.isArray(delta.tool_calls) && delta.tool_calls.length > 0) {
            state.toolCalls = delta.tool_calls;
          }
        }
        if (choice.finish_reason) state.finishReason = choice.finish_reason;
      }
    }
  }
  if (!done) state.warnings.push('SSE stream ended without [DONE]');
}

function evaluate(state, opts) {
  const warnings = state.warnings;
  if (!state.content.trim()) warnings.push('Response content is empty');
  if (!state.usage) warnings.push('No usage in response');
  if (state.usage && (state.usage.prompt_tokens === 0 || state.usage.prompt_tokens == null)) {
    warnings.push('Usage has no prompt_tokens');
  }
  if (!state.content.trim() && state.reasoning.trim()) {
    warnings.push('Reasoning-only response (reasoning present, content empty)');
  }
  if (state.finishReason === 'tool_calls') {
    warnings.push('finish_reason is tool_calls: this is not a final answer');
  }
  if (state.finishReason === 'length') {
    warnings.push('finish_reason is length: output was truncated');
  }
  if (state.echoModel && opts.model && state.echoModel !== opts.model) {
    warnings.push(`Response model "${state.echoModel}" differs from requested "${opts.model}"`);
  }
  const ok = state.status >= 200 && state.status < 300 && state.content.trim().length > 0;
  const failed = !ok || (opts.strict && warnings.length > 0);
  return { ok, failed };
}

async function main() {
  let opts;
  try {
    opts = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(`Error: ${error.message}`);
    usage();
    process.exit(EXIT_USAGE);
  }

  const warnings = [];
  const startedAt = performance.now();

  const models = opts.skipModels
    ? { status: null, ok: null, ids: [], error: null }
    : await readModels(opts, warnings);

  if (!opts.model) {
    opts.model = models.ids[0] || '';
    if (!opts.model) {
      console.error('No --model provided and /models returned no usable model.');
      process.exit(EXIT_FAIL);
    }
  }
  const modelPresent = models.ids.length > 0 ? models.ids.includes(opts.model) : null;
  if (modelPresent === false) warnings.push(`Model "${opts.model}" is not listed by /models`);

  const content = [{ type: 'text', text: opts.prompt }];
  if (opts.image) {
    const filePath = path.resolve(opts.image);
    const info = await stat(filePath).catch(() => null);
    if (!info || !info.isFile()) {
      console.error(`Image not found: ${filePath}`);
      process.exit(EXIT_USAGE);
    }
    if (info.size > 15 * 1024 * 1024) {
      console.error('Image exceeds 15 MB; refusing to send.');
      process.exit(EXIT_USAGE);
    }
    const buffer = await readFile(filePath);
    content.push({ type: 'image_url', image_url: { url: imageDataUrl(buffer, filePath) } });
  }

  const body = {
    model: opts.model,
    messages: [{ role: 'user', content: content.length === 1 ? opts.prompt : content }],
    max_tokens: opts.maxTokens,
    stream: opts.stream,
  };

  const state = {
    status: 0,
    contentType: '',
    content: '',
    reasoning: '',
    toolCalls: [],
    finishReason: null,
    usage: null,
    echoModel: '',
    events: 0,
    warnings,
  };

  const chatStartedAt = performance.now();
  let rawError = '';
  try {
    const response = await fetch(`${opts.base}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: opts.stream ? 'text/event-stream' : 'application/json',
        ...authHeaders(opts.key),
      },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(opts.timeoutSec * 1000),
    });
    state.status = response.status;
    state.contentType = response.headers.get('content-type') || '';

    if (!response.ok) {
      rawError = (await response.text()).slice(0, 1000);
    } else if (opts.stream && state.contentType.includes('text/event-stream')) {
      await consumeStream(response, state);
    } else {
      const text = await response.text();
      if (opts.stream) warnings.push(`Requested stream but received ${state.contentType || 'unknown content type'}`);
      const parsed = parseJson(text);
      if (parsed.error) {
        rawError = `Invalid JSON: ${text.slice(0, 300)}`;
      } else {
        const data = parsed.value;
        if (data?.model) state.echoModel = data.model;
        if (data?.usage) state.usage = normalizeUsage(data.usage);
        const choice = data?.choices?.[0];
        state.finishReason = choice?.finish_reason ?? null;
        collectAssistant(choice?.message, state);
        if (!state.content && data?.content) state.content = contentToText(data.content);
        if (data?.reasoning_content) state.reasoning += data.reasoning_content;
      }
    }
  } catch (error) {
    rawError = errorMessage(error);
  }

  const latencyMs = Math.round(performance.now() - chatStartedAt);
  const { ok, failed } = evaluate(state, opts);

  const report = {
    base: opts.base,
    model: opts.model,
    stream: opts.stream,
    image: Boolean(opts.image),
    models: {
      status: models.status,
      count: models.ids.length,
      model_present: modelPresent,
      error: models.error,
    },
    chat: {
      status: state.status,
      content_type: state.contentType,
      latency_ms: latencyMs,
      finish_reason: state.finishReason,
      content: state.content,
      reasoning_chars: state.reasoning.length,
      tool_calls: state.toolCalls.length,
      usage: state.usage,
      events: state.events,
      error: rawError || null,
    },
    warnings,
    ok,
    total_ms: Math.round(performance.now() - startedAt),
  };

  if (opts.json) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log(`base:        ${opts.base}`);
    console.log(`model:       ${opts.model}${modelPresent === false ? ' (not listed)' : ''}`);
    if (!opts.skipModels) console.log(`models:      HTTP ${models.status ?? '-'}, ${models.ids.length} listed`);
    console.log(`chat:        HTTP ${state.status || '-'}, ${latencyMs} ms, finish=${state.finishReason ?? '-'}`);
    if (state.usage) {
      console.log(`usage:       prompt=${state.usage.prompt_tokens ?? '?'} completion=${state.usage.completion_tokens ?? '?'} total=${state.usage.total_tokens ?? '?'} cached=${state.usage.cached_tokens ?? '?'}`);
    }
    console.log(`content:     ${state.content.trim() ? JSON.stringify(state.content.trim().slice(0, 500)) : '(empty)'}`);
    if (state.reasoning.length > 0) console.log(`reasoning:   ${state.reasoning.length} chars (not returned as content)`);
    if (state.toolCalls.length > 0) console.log(`tool_calls:  ${state.toolCalls.length}`);
    if (rawError) console.log(`error:       ${rawError.replace(/\s+/g, ' ').slice(0, 500)}`);
    if (warnings.length > 0) {
      console.log('warnings:');
      for (const warning of warnings) console.log(`  - ${warning}`);
    }
    console.log(`result:      ${failed ? 'FAIL' : ok ? 'PASS' : 'WARN'}`);
  }

  process.exit(failed ? EXIT_FAIL : EXIT_OK);
}

main().catch((error) => {
  console.error(`Probe crashed: ${errorMessage(error)}`);
  process.exit(EXIT_FAIL);
});
