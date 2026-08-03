import subprocess
import json
import os
import sys
import winreg
import base64

def run_cmd(cmd, encoding='gbk', timeout=20):
    """Execute a shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                                encoding=encoding, errors='replace', timeout=timeout)
        return {'returncode': result.returncode, 'output': result.stdout + result.stderr}
    except subprocess.TimeoutExpired:
        return {'returncode': -2, 'output': 'TIMEOUT'}
    except Exception as e:
        return {'returncode': -1, 'output': str(e)}

def read_reg(path, value_name, hive=winreg.HKEY_CURRENT_USER):
    """Read a Windows registry value."""
    try:
        with winreg.OpenKey(hive, path) as key:
            val, typ = winreg.QueryValueEx(key, value_name)
            return {'value': str(val), 'type': str(typ)}
    except FileNotFoundError:
        return {'value': None, 'error': 'Not found'}
    except Exception as e:
        return {'value': None, 'error': str(e)}

def read_file_tail(path, max_lines=40, encoding='utf-8'):
    """Read the tail of a text file (best effort)."""
    try:
        if not os.path.exists(path):
            return {'path': path, 'exists': False}
        with open(path, 'r', encoding=encoding, errors='replace') as f:
            lines = f.readlines()
        tail = ''.join(lines[-max_lines:])
        return {'path': path, 'exists': True, 'size': os.path.getsize(path),
                'last_write': os.path.getmtime(path), 'tail': tail}
    except Exception as e:
        return {'path': path, 'exists': True, 'error': str(e)}

def get_vpn_connections():
    """Get list of configured VPN/dial-up connections."""
    pbk_dirs = [
        os.path.expandvars(r'%APPDATA%\Microsoft\Network\Connections\Pbk'),
        os.path.expandvars(r'%PROGRAMDATA%\Microsoft\Network\Connections\Pbk'),
    ]
    connections = []
    for d in pbk_dirs:
        if os.path.exists(d):
            try:
                files = [f for f in os.listdir(d) if f.endswith('.pbk')]
                connections.extend(files)
            except Exception:
                pass
    return connections

def query_mihomo_rules():
    """Query mihomo runtime rules via named pipe (best effort, -EncodedCommand 避免引号嵌套问题)."""
    ps = r'''
$pipe = New-Object System.IO.Pipes.NamedPipeClientStream(".", "verge-mihomo", [System.IO.Pipes.PipeDirection]::InOut, [System.IO.Pipes.PipeOptions]::None)
try {
  $pipe.Connect(2000)
  $sw = New-Object System.IO.StreamWriter($pipe); $sw.AutoFlush = $true
  $sw.WriteLine("GET /rules HTTP/1.1"); $sw.WriteLine("Host: localhost")
  $sw.WriteLine("Authorization: Bearer set-your-secret"); $sw.WriteLine("Connection: close"); $sw.WriteLine("")
  $sr = New-Object System.IO.StreamReader($pipe)
  $buf = New-Object char[] 8192; $sb = New-Object System.Text.StringBuilder
  $dl = [DateTime]::Now.AddSeconds(3)
  while ([DateTime]::Now -lt $dl) {
    if ($sr.Peek() -ge 0) { $n = $sr.Read($buf, 0, 8192); if ($n -le 0) { break }; [void]$sb.Append($buf, 0, $n) }
    else { Start-Sleep -Milliseconds 60 }
  }
  $resp = $sb.ToString()
  $js = $resp.IndexOf('{"rules"')
  if ($js -ge 0) {
    $json = $resp.Substring($js); $json = $json.Substring(0, $json.LastIndexOf('}')+1)
    $obj = $json | ConvertFrom-Json
    $vpn = $obj.rules | Where-Object { $_.payload -match '134\.224|VPDN|TrustAgent|trustservice|vpn_start|JxVpn' } | Select-Object -First 10
    "RULES_COUNT=$($obj.rules.Count)"
    $vpn | ForEach-Object { "[$($_.index)] $($_.type) $($_.payload) -> $($_.proxy)" }
    if (-not $vpn) { "NO_VPDN_RULES_IN_RUNTIME" }
  } else { "PIPE_NO_JSON" }
} catch { "PIPE_FAIL: $($_.Exception.Message)" } finally { if ($pipe.IsConnected) { $pipe.Dispose() } }
'''
    encoded = base64.b64encode(ps.encode('utf-16-le')).decode('ascii')
    return run_cmd('powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand ' + encoded,
                   encoding='utf-8', timeout=15)

def diagnose():
    """Run comprehensive VPDN diagnosis and return results dict."""
    results = {}

    # 1. Proxy Settings (Registry) - 含 SDP PAC
    reg_base = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
    results['proxy_enable'] = read_reg(reg_base, 'ProxyEnable')
    results['proxy_server'] = read_reg(reg_base, 'ProxyServer')
    results['proxy_override'] = read_reg(reg_base, 'ProxyOverride')
    results['auto_config_url'] = read_reg(reg_base, 'AutoConfigURL')  # SDP PAC
    results['winhttp_proxy'] = run_cmd('netsh winhttp show proxy')

    # 2. System Services (用正确的短名称)
    services = [
        'RasMan',          # Remote Access Connection Manager
        'RemoteAccess',    # Routing and Remote Access
        'TapiSrv',         # Telephony（短名称，实测651根因）
        'Netman',          # Network Connections
        'trustservice',    # 奇安信 TrustAgent（若存在）
        'trustdservice',
        'trustfixservice',
    ]
    for svc in services:
        results[f'service_{svc}'] = run_cmd(f'sc query {svc}')

    # 3. Network Interfaces（含 ctEAO 虚拟网卡）
    results['interfaces'] = run_cmd('netsh interface show interface')
    results['ipconfig'] = run_cmd('ipconfig /all')
    results['route'] = run_cmd('route print')
    results['cteao_adapter'] = run_cmd(
        'powershell.exe -NoProfile -Command "Get-NetAdapter -IncludeHidden -Name ctEAO-10 -ErrorAction SilentlyContinue | Select-Object Name,InterfaceDescription,Status,MediaConnectionState | Format-List"',
        encoding='utf-8')

    # 4. VPDN Client Files & 客户端日志（第一证据）
    vpdn_dirs = [r'C:\Program Files (x86)\dx_vpdn', r'D:\JxTelecomVPDN']
    results['vpdn_dirs'] = {}
    for d in vpdn_dirs:
        if os.path.exists(d):
            try:
                results['vpdn_dirs'][d] = os.listdir(d)
            except Exception as e:
                results['vpdn_dirs'][d] = str(e)
        else:
            results['vpdn_dirs'][d] = 'NOT_FOUND'
    results['dx_log'] = read_file_tail(os.path.expandvars(r'%USERPROFILE%\dx_log.txt'))
    results['dx_log_assets'] = read_file_tail(r'C:\Program Files (x86)\dx_vpdn\assets\dx_log.txt')

    # 5. TrustAgent / vpnclient 数据目录
    results['trustagent_data'] = run_cmd(
        'powershell.exe -NoProfile -Command "Get-ChildItem C:\\ProgramData\\TrustAgent\\logs,C:\\ProgramData\\vpnclient\\logs -File -ErrorAction SilentlyContinue | Select-Object Name,Length,LastWriteTime | Sort-Object LastWriteTime -Descending | Select-Object -First 8 | Format-Table -AutoSize"',
        encoding='utf-8')

    # 6. VPDN PBK Configurations
    results['vpn_connections'] = get_vpn_connections()

    # 7. Windows Event Logs (RasClient, last 48 hours)
    results['rasclient_events'] = run_cmd(
        'wevtutil qe Application '
        '/q:"*[System[Provider[@Name=\'RasClient\'] and EventID=20227 and '
        'TimeCreated[timediff(@SystemTime) <= 172800000]]]" '
        '/f:text /c:20'
    )

    # 8. Active Processes
    results['vpdn_process'] = run_cmd('tasklist /FI "IMAGENAME eq VPDN*" /FO LIST')
    results['trustagent_process'] = run_cmd('tasklist /FI "IMAGENAME eq dx_TrustAgent*" /FO LIST')

    # 9. Network Connections & Ports
    results['netstat'] = run_cmd('netstat -an | findstr "1723 500 4500 443 80"')
    results['listeners'] = run_cmd('netstat -ano | findstr "LISTENING"')

    # 10. Firewall Status
    results['firewall'] = run_cmd('netsh advfirewall show currentprofile')

    # 11. DNS
    results['dns_display'] = run_cmd('ipconfig /displaydns')

    # 12. WMI Permissions (for 651 errors)
    results['wmi_perms'] = run_cmd('icacls "C:\\Windows\\System32\\LogFiles\\WMI"')

    # 13. Environment Proxy Variables
    results['env_http_proxy'] = os.environ.get('HTTP_PROXY', 'not_set')
    results['env_https_proxy'] = os.environ.get('HTTPS_PROXY', 'not_set')
    results['env_all_proxy'] = os.environ.get('ALL_PROXY', 'not_set')

    # 14. mihomo 运行时规则（权威：确认直连规则真正加载）
    results['mihomo_runtime_rules'] = query_mihomo_rules()

    return results

def save_report(results, output_path=None):
    """Save diagnosis results to a JSON file."""
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), 'vpdn_diagnosis.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return output_path

def print_summary(results):
    """Print a human-readable summary of key findings."""
    print("=" * 60)
    print("VPDN DIAGNOSIS SUMMARY")
    print("=" * 60)

    # Proxy check
    proxy = results.get('proxy_enable', {})
    if proxy.get('value') == '1':
        server = results.get('proxy_server', {}).get('value', 'unknown')
        print(f"[ALERT] System proxy is ENABLED: {server}")
        print("        #1 cause of 'VPDN server access failed' -> see SKILL.md 路径 A")
    else:
        print("[OK] System proxy is disabled")

    override = results.get('proxy_override', {}).get('value', '')
    if override and '134.224' in override:
        print("[OK] ProxyOverride 已含 VPDN 段 (134.224.0.0/15)")
    else:
        print("[WARN] ProxyOverride 未含 VPDN 段 134.224.0.0/15")

    pac = results.get('auto_config_url', {}).get('value')
    if pac:
        print(f"[WARN] AutoConfigURL (SDP PAC) 存在: {pac} —— 应清除")
    else:
        print("[OK] AutoConfigURL 为空")

    # 客户端日志（第一证据）
    dx = results.get('dx_log', {})
    if dx.get('exists') and dx.get('tail'):
        tail = dx['tail']
        print("\n[CLIENT LOG dx_log.txt] 末尾片段:")
        for line in tail.splitlines()[-8:]:
            print(f"  {line[:150]}")
        if '127.0.0.1' in tail and ('Read timed out' in tail or 'Err 289' in tail):
            print("  >>> 命中代理劫持模式（Err 289/127.0.0.1:7897）")
        if 'Req OK 200' in tail:
            print("  >>> 最近请求成功（Req OK 200）")

    # Services
    print("\n[SERVICES]")
    for key, val in results.items():
        if key.startswith('service_'):
            svc_name = key.replace('service_', '')
            out = val.get('output', '')
            if 'RUNNING' in out:
                print(f"  [OK] {svc_name}: RUNNING")
            elif 'STOPPED' in out:
                print(f"  [WARN] {svc_name}: STOPPED")
            elif '1060' in out:
                print(f"  [INFO] {svc_name}: Not installed (may be normal)")
            else:
                print(f"  [?] {svc_name}: {out[:60]}")

    # ctEAO 网卡
    cteao = results.get('cteao_adapter', {}).get('output', '')
    if 'ctEAO-10' in cteao:
        status = [l.strip() for l in cteao.splitlines() if 'Status' in l]
        print(f"\n[ctEAO-10] {'; '.join(status) if status else '存在'}")
    else:
        print("\n[ctEAO-10] 未启用/不存在（禁用状态，属正常，用于防 DNS 污染）")

    # mihomo 运行时规则
    mr = results.get('mihomo_runtime_rules', {}).get('output', '')
    if mr:
        print("\n[mihomo 运行时规则]")
        for line in mr.splitlines()[:12]:
            print(f"  {line[:150]}")

    # Events
    events = results.get('rasclient_events', {}).get('output', '')
    if 'CoId=' in events:
        print("\n[EVENT LOG] Recent RasClient errors found:")
        import re
        codes = re.findall(r'error code returned on failure is (\d+)', events)
        if codes:
            print(f"  Recent error codes: {', '.join(set(codes))}")
    else:
        print("\n[EVENT LOG] No recent RasClient errors (client may not reach dial stage -> 路径 A)")

    print("\n" + "=" * 60)

def main():
    """Main entry point."""
    results = diagnose()
    output_path = save_report(results)
    print_summary(results)
    print(f"\nFull report saved to: {output_path}")
    return results

if __name__ == '__main__':
    main()