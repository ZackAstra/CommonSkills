# CommonSkills 椤圭洰

> **AI Agent 鍏叡鎶€鑳戒粨搴擄紙CommonSkills锛?* 鈥斺€?缁熶竴绠＄悊璺?Agent 骞冲彴鐨勫叡浜妧鑳斤紙Skills锛夛紝瀹炵幇涓€澶勭紪鍐欍€佸澶勫鐢ㄣ€?
---

## 馃搶 椤圭洰瀹氫綅

鏈粨搴撻泦涓鐞嗘墍鏈夊彲琚涓?AI Agent 骞冲彴澶嶇敤鐨勬妧鑳斤紙Skill锛夛紝鍖呮嫭锛?
- **Kimi**锛圵ork 妯″紡 / Kimi Code IDE 鎻掍欢锛?- **Cursor**
- **Codex**
- **Trae**
- **Qoder**
- 浠ュ強浠讳綍鏀寔 `~/.agents/skills/` 鎴?`~/.kimi/skills/` 瑙勮寖鐨?Agent 宸ュ叿

---

## 馃搧 鐩綍缁撴瀯

```
CommonSkills/
鈹溾攢鈹€ README.md                    # 鏈枃浠?鈹溾攢鈹€ .gitignore                   # Git 蹇界暐瑙勫垯
鈹溾攢鈹€ scripts/
鈹?  鈹斺攢鈹€ sync-to-kimi.sh          # Kimi Work 妯″紡澶嶅埗鍚屾鑴氭湰
鈹?  鈹斺攢鈹€ setup-symlinks.ps1       # Windows 杞摼鎺ユ壒閲忚缃剼鏈?鈹溾攢鈹€ [skill-name-1]/              # 鎶€鑳界洰褰?1
鈹?  鈹斺攢鈹€ SKILL.md                 # 鎶€鑳戒富鏂囦欢锛堝繀椤伙級
鈹溾攢鈹€ [skill-name-2]/              # 鎶€鑳界洰褰?2
鈹?  鈹溾攢鈹€ SKILL.md
鈹?  鈹斺攢鈹€ references/              # 鍙€夛細鍙傝€冭祫鏂?鈹斺攢鈹€ ...
```

褰撳墠鍏辨湁 **62 涓叕鍏辨妧鑳?*锛屾兜鐩栵細鍐欎綔銆佷唬鐮佸紑鍙戙€佹暟鎹垎鏋愩€佹姇鐮斻€佸姙鍏嚜鍔ㄥ寲銆丳PT 鐢熸垚绛夈€?
---

## 馃敡 鍙岄€氶亾 Agent 鍔犺浇鏈哄埗

涓嶅悓 Agent 骞冲彴瀵规妧鑳界洰褰曠殑鍔犺浇鏂瑰紡涓嶅悓锛屾湰椤圭洰閲囩敤 **鍙岄€氶亾鏂规**锛?
### 閫氶亾 A锛歋ymbolic Link锛堣蒋閾炬帴锛夆€斺€?閫傜敤浜?Cursor / Codex / Trae / Qoder / Kimi Code IDE

杩欎簺 Agent 骞冲彴鎵弿鏈湴鏂囦欢绯荤粺鏃?*璺熼殢杞摼鎺ワ紙Symbolic Link锛?*锛屽洜姝ら噰鐢ㄨ蒋閾炬帴鏂瑰紡锛?
| Agent 绋嬪簭 | 杞摼鎺ヨ矾寰?| 鎸囧悜鐩爣 |
|-----------|-----------|---------|
| Cursor / Codex / Trae / Qoder | `~/.agents/skills/<skill-name>` | `~/CommonSkills/<skill-name>` |
| Kimi Code IDE 鎻掍欢 | `~/.kimi/skills/<skill-name>` | `~/CommonSkills/<skill-name>` |

**浼樺娍**锛?- 瀹炴椂鍚屾锛氫慨鏀?`CommonSkills` 涓殑婧愭枃浠讹紝鎵€鏈?Agent 绔嬪嵆鐢熸晥
- 闆剁淮鎶わ細鏃犻渶鎵嬪姩澶嶅埗
- 鑺傜渷纾佺洏绌洪棿

### 閫氶亾 B锛歂ative Directory Copy锛堝師鐢熺洰褰曞鍒讹級鈥斺€?閫傜敤浜?Kimi Work 妯″紡

**Kimi 妗岄潰瀹㈡埛绔紙Work 妯″紡锛夌殑 `daimon` 鍐呮牳鍦ㄦ壂鎻忔妧鑳界洰褰曟椂锛屼細璺宠繃 Symbolic Link锛堣蒋閾炬帴锛?*銆傚洜姝ゅ繀椤婚噰鐢?*鍘熺敓鐩綍澶嶅埗**鏂瑰紡锛?
| Agent 绋嬪簭 | 澶嶅埗鐩爣璺緞 | 鏉ユ簮 |
|-----------|-----------|------|
| Kimi Work 妯″紡 | `~/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills/<skill-name>` | `~/CommonSkills/<skill-name>` |

**鐗圭偣**锛?- 闇€瑕佸鍒讹紙涓嶆槸杞摼鎺ワ級
- `daimon` 鍐呮牳鍔犺浇鏃惰涓哄師鐢熸妧鑳斤紝UI 鍙甯告樉绀哄拰璋冪敤
- 鏇存柊鍚庨渶閲嶆柊鍚屾

---

## 馃殌 蹇€熷紑濮?
### 1. 棣栨璁剧疆锛圵indows锛?
#### 姝ラ 1锛氬垱寤?CommonSkills 杞摼鎺ワ紙閫氶亾 A锛?
鎵撳紑 PowerShell锛堢鐞嗗憳锛夛紝杩愯锛?
```powershell
# 涓?~/.agents/skills/ 鍒涘缓杞摼鎺ワ紙Cursor / Codex / Trae / Qoder锛?$common = "C:\Users\$env:USERNAME\CommonSkills"
$agents = "C:\Users\$env:USERNAME\.agents\skills"

# 濡傛灉鐩綍涓嶅瓨鍦ㄥ垯鍒涘缓
if (-not (Test-Path $agents)) { New-Item -ItemType Directory -Path $agents }

# 閬嶅巻 CommonSkills 涓墍鏈夋妧鑳斤紝鍒涘缓杞摼鎺?Get-ChildItem $common -Directory | ForEach-Object {
    $skill = $_.Name
    $src = Join-Path $common $skill
    $dst = Join-Path $agents $skill
    if (Test-Path $dst) { Remove-Item $dst -Force }
    New-Item -ItemType SymbolicLink -Path $dst -Target $src
}

# 鍚屾牱涓?~/.kimi/skills/ 鍒涘缓杞摼鎺ワ紙Kimi Code IDE 鎻掍欢锛?$kimi = "C:\Users\$env:USERNAME\.kimi\skills"
if (-not (Test-Path $kimi)) { New-Item -ItemType Directory -Path $kimi }
Get-ChildItem $common -Directory | ForEach-Object {
    $skill = $_.Name
    $src = Join-Path $common $skill
    $dst = Join-Path $kimi $skill
    if (Test-Path $dst) { Remove-Item $dst -Force }
    New-Item -ItemType SymbolicLink -Path $dst -Target $src
}
```

#### 姝ラ 2锛氬鍒跺埌 Kimi Work 妯″紡锛堥€氶亾 B锛?
```powershell
# 澶嶅埗鍒?Kimi 妗岄潰瀹㈡埛绔妧鑳界洰褰?$common = "C:\Users\$env:USERNAME\CommonSkills"
$kimiWork = "C:\Users\$env:USERNAME\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills"

Get-ChildItem $common -Directory | ForEach-Object {
    $skill = $_.Name
    $src = Join-Path $common $skill
    $dst = Join-Path $kimiWork $skill
    if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
    Copy-Item -Path $src -Destination $dst -Recurse
}
```

---

## 馃攧 鑷姩鍚屾鏈哄埗锛圙it Hook锛?
### 鍘熺悊

閫氳繃 Git Hook 瀹炵幇锛氬綋 `CommonSkills` 浠撳簱鏇存柊锛坧ull / merge / checkout锛夋椂锛?*鑷姩瑙﹀彂鍚屾鑴氭湰**锛岀‘淇?Kimi Work 妯″紡鐨勬妧鑳界洰褰曞缁堜笌浠撳簱鏈€鏂扮増鏈竴鑷淬€?
### 宸查厤缃殑 Hook

| Hook 绫诲瀷 | 瑙﹀彂鏃舵満 | 浣滅敤 |
|----------|---------|------|
| `post-merge` | 鎵ц `git pull` 鎴?`git merge` 鍚?| 鍚屾鏈€鏂版妧鑳藉埌 Kimi Work 妯″紡 |
| `post-checkout` | 鎵ц `git checkout` 鍒囨崲鍒嗘敮鍚?| 鍚屾褰撳墠鍒嗘敮鎶€鑳藉埌 Kimi Work 妯″紡 |
| `post-commit` | 鎵ц `git commit` 鍚?| 鍙€夛細鍚屾鏈湴淇敼鍒?Kimi Work 妯″紡 |

### 鍚屾鑴氭湰閫昏緫锛坄scripts/sync-to-kimi.sh`锛?
```bash
#!/bin/bash
# 鍙岄€氶亾鍚屾鑴氭湰
# 閫氶亾 A锛氳蒋閾炬帴锛堝凡瀛樺湪锛屾棤闇€鎿嶄綔锛?# 閫氶亾 B锛氬鍒跺埌 Kimi Work 妯″紡鐩綍

COMMON="C:/Users/$(whoami)/CommonSkills"
KIMI_WORK="C:/Users/$(whoami)/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills"

echo "[Sync] 寮€濮嬪悓姝?CommonSkills -> Kimi Work 妯″紡..."

cd "$COMMON" || exit 1
for skill in */; do
    skill=${skill%/}
    src="$COMMON/$skill"
    dst="$KIMI_WORK/$skill"
    
    # 璺宠繃闈炵洰褰曢」鍜岄殣钘忔枃浠?    [ -d "$src" ] || continue
    [[ "$skill" == .* ]] && continue
    
    # 濡傛灉鐩爣鏄蒋閾炬帴锛屽厛鍒犻櫎
    if [ -L "$dst" ]; then
        rm -f "$dst"
        echo "  [绉婚櫎杞摼鎺 $skill"
    fi
    
    # 澶嶅埗涓哄師鐢熺洰褰?    rm -rf "$dst"
    cp -r "$src" "$dst"
    echo "  [宸插鍒禲 $skill"
done

echo "[Sync] 鍚屾瀹屾垚銆?
```

### 婵€娲?Hook

```bash
# 鍦?CommonSkills 鐩綍涓?cd ~/CommonSkills
chmod +x scripts/sync-to-kimi.sh

# 閾炬帴 hook
cp scripts/sync-to-kimi.sh .git/hooks/post-merge
cp scripts/sync-to-kimi.sh .git/hooks/post-checkout
chmod +x .git/hooks/post-merge
chmod +x .git/hooks/post-checkout
```

---

## 鉃?鏂板鎶€鑳界殑鏍囧噯娴佺▼

1. **鍦?`CommonSkills/` 涓嬪垱寤烘柊鎶€鑳界洰褰?*
   ```bash
   mkdir -p ~/CommonSkills/my-new-skill
   cat > ~/CommonSkills/my-new-skill/SKILL.md << 'EOF'
   ---
   name: my-new-skill
   description: 鏂版妧鑳芥弿杩?   version: 1.0.0
   ---
   
   # 鏂版妧鑳藉唴瀹?   ...
   EOF
   ```

2. **鎻愪氦鍒?Git**
   ```bash
   cd ~/CommonSkills
   git add my-new-skill/
   git commit -m "add: my-new-skill"
   git push
   ```

3. **鑷姩鍚屾锛圙it Hook锛?*
   - `post-commit` / `post-merge` / `post-checkout` 浼氳嚜鍔ㄦ墽琛屽悓姝ヨ剼鏈?   - Kimi Work 妯″紡鐩綍浼氬鍒舵柊澧炴妧鑳?   - 鍏朵粬 Agent锛圕ursor/Codex/Trae/Qoder/KimiCodeIDE锛夐€氳繃杞摼鎺ュ疄鏃剁敓鏁?
4. **楠岃瘉**
   - 閲嶅惎 Kimi 瀹㈡埛绔紙Work 妯″紡锛夛紝鎼滅储鏂版妧鑳藉悕绉?   - 鍦?Cursor/Codex/Trae/Qoder 涓獙璇佹柊鎶€鑳藉彲鐢?   - 閲嶅惎 Kimi 瀹㈡埛绔紝鎼滅储鏂版妧鑳藉悕绉?   - 鍦?Cursor/Codex/Trae/Qoder 涓獙璇佹柊鎶€鑳藉彲鐢?
---

## 馃摑 鍚?Agent 鎶€鑳界洰褰曢€熸煡

| Agent | 鎶€鑳界洰褰?| 鍔犺浇鏂瑰紡 | 鏄惁闇€瑕侀噸鍚?|
|-------|---------|---------|------------|
| **Kimi Work 妯″紡** | `~/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills/` | 澶嶅埗锛堝師鐢熺洰褰曪級 | 鉁?闇€瑕侀噸鍚鎴风 |
| **Kimi Code IDE** | `~/.kimi/skills/` | 杞摼鎺?| 鉂?瀹炴椂鐢熸晥 |
| **Cursor** | `~/.cursor/skills/` 鎴?`~/.agents/skills/` | 杞摼鎺?| 鉂?瀹炴椂鐢熸晥 |
| **Codex** | `~/.codex/skills/` 鎴?`~/.agents/skills/` | 杞摼鎺?| 鉂?瀹炴椂鐢熸晥 |
| **Trae** | `~/.trae/skills/` 鎴?`~/.agents/skills/` | 杞摼鎺?| 鉂?瀹炴椂鐢熸晥 |
| **Qoder** | `~/.qoder/skills/` 鎴?`~/.agents/skills/` | 杞摼鎺?| 鉂?瀹炴椂鐢熸晥 |

> 娉細`~/.agents/skills/` 鏄€氱敤鍏变韩鐩綍锛岃澶氫釜 Agent 鏀寔銆?
---

## 鈿狅笍 宸茬煡闄愬埗涓庢敞鎰忎簨椤?
### 1. Kimi Work 妯″紡涓嶆敮鎸佽蒋閾炬帴

**鏍规湰鍘熷洜**锛欿imi 妗岄潰瀹㈡埛绔殑 `daimon` 鍐呮牳鍦ㄦ壂鎻?`daimon-share/daimon/skills/` 鏃讹紝浣跨敤 `fs.readdir` 鐨?`withFileTypes: true` 骞舵鏌?`dirent.isSymbolicLink()`锛屼富鍔ㄨ烦杩囨墍鏈?Symbolic Link锛堣蒋閾炬帴锛夊拰 Junction锛堢洰褰曡仈鎺ワ級銆?
**楠岃瘉杩囩▼**锛?- `test-native-daimon`锛堝師鐢熺洰褰曪級鈫?鉁?鍙姞杞?- `cubox`锛堝師鐢熺洰褰曪級鈫?鉁?鍙姞杞?- `agently-mail`锛堣蒋閾炬帴锛夆啋 鉂?涓嶅彲鍔犺浇
- `backend-dev`锛堣蒋閾炬帴锛夆啋 鉂?涓嶅彲鍔犺浇

**缁撹**锛氬彧鏈?*鍘熺敓鐩綍**锛堥潪杞摼鎺ワ級鎵嶈兘琚?Kimi Work 妯″紡鍔犺浇銆?
### 2. 閰嶇疆宸紓

Kimi 瀹㈡埛绔?Work 妯″紡涓?Kimi Code IDE 鎻掍欢浣跨敤**涓嶅悓鐨勯厤缃枃浠?*锛?- Kimi Code IDE 鎻掍欢锛歚~/.kimi/config.toml`锛堟敮鎸?`extra_skill_dirs`锛?- Kimi Work 妯″紡锛歚daimon-share/daimon/runtime/kimi-code/config.toml`锛坄extra_skill_dirs` 鍙兘鏃犳晥锛?
### 3. 鍐呯疆鎶€鑳斤紙builtin-skills锛?
Kimi 瀹㈡埛绔墦鍖呬簡 34 涓唴缃妧鑳斤紙`builtin-skills`锛夛紝浣嶄簬锛?```
~/AppData/Roaming/kimi-desktop/daimon-bundle/app/daimon/assets/builtin-skills/
```
杩欎簺鎶€鑳芥湁 `builtInSkillsSha256` 鏍￠獙锛屼笉寤鸿淇敼銆?
---

## 馃敡 鏁呴殰鎺掓煡

### 闂锛欿imi Work 妯″紡鎵句笉鍒版煇涓妧鑳?
**鎺掓煡姝ラ**锛?1. 纭鎶€鑳界洰褰曞湪 `daimon-share/daimon/skills/` 涓嬫槸**鍘熺敓鐩綍**锛堜笉鏄蒋閾炬帴锛?   ```bash
   ls -la ~/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills/<skill-name>
   # 濡傛灉鏄剧ず lrwxrwxrwx -> ...锛岃鏄庢槸杞摼鎺ワ紝闇€瑕佹浛鎹负澶嶅埗
   ```
2. 纭 `SKILL.md` 鐨?YAML frontmatter 鏍煎紡姝ｇ‘锛?   ```yaml
   ---
   name: skill-name
   description: 鎶€鑳芥弿杩?   version: 1.0.0
   ---
   ```
3. 纭鎶€鑳界洰褰曞悕涓?`SKILL.md` 涓殑 `name` 涓€鑷?4. 閲嶅惎 Kimi 瀹㈡埛绔?
### 闂锛氳蒋閾炬帴鍦ㄥ叾浠?Agent 涓け鏁?
**鎺掓煡姝ラ**锛?1. 纭杞摼鎺ョ洰鏍囪矾寰勫瓨鍦?2. 纭杞摼鎺ユ病鏈夎鐮村潖锛堝鐩爣鐩綍琚Щ鍔ㄦ垨鍒犻櫎锛?3. 閲嶆柊鍒涘缓杞摼鎺ワ細
   ```bash
   rm -f ~/.agents/skills/<skill-name>
   ln -s ~/CommonSkills/<skill-name> ~/.agents/skills/<skill-name>
   ```

---

## 馃摎 鍙傝€冩枃妗?
- [yaolifeng.com - symlink_git_personal_agent_skill](https://yaolifeng.com/shorts/symlink_git_personal_agent_skill)
- Kimi Code 瀹樻柟鏂囨。锛歚.kimi/skills/` 鍜?`.agents/skills/` 鐩綍瑙勮寖
- Node.js `fs.readdir` 涓?`dirent.isSymbolicLink()` 琛屼负璇存槑

---

## 馃彿锔?鐗堟湰鍘嗗彶

| 鐗堟湰 | 鏃ユ湡 | 鍙樻洿 |
|------|------|------|
| 1.0.0 | 2026-07-15 | 鍒濆寤虹珛锛屾敮鎸?Kimi/Cursor/Codex/Trae/Qoder 鍙岄€氶亾鍚屾 |
| 1.0.1 | 2026-07-15 | docs: 鏄庣‘鍚屾鑼冨洿浠呴檺 Kimi Work 妯″紡锛孋hat 妯″紡涓嶅彈褰卞搷 |
| 1.0.2 | 2026-07-15 | docs: 瀹屽叏绉婚櫎 Chat 妯″紡寮曠敤锛屽悓姝ヨ寖鍥寸簿纭负 Kimi Work + Kimi Code IDE |
| 1.0.3 | 2026-07-15 | fix: 鍒犻櫎鎶€鑳界洰褰曢€熸煡琛ㄤ腑鐨勯噸澶?Kimi Code IDE 琛?|
| 1.1.0 | 2026-07-15 | fix: 淇 5 涓妧鑳界殑鍓嶇疆鍏冩暟鎹紙time-awareness銆亀orker-safety 琛ュ厖 frontmatter锛沢ongkao-review-allinone銆乲imi-webbridge-desktop銆乲imiim 淇 name 涓庣洰褰曞悕涓嶅尮閰嶏級 |
| 1.1.1 | 2026-07-15 | fix: 绉婚櫎鍚屾鑴氭湰涓殑 Chat 妯″紡娈嬬暀寮曠敤锛涗慨澶嶆椂闂存埑姣旇緝閫昏緫锛堢洰褰曠骇 鈫?SKILL.md 鏂囦欢绾э級 |
| 1.1.2 | 2026-07-15 | fix: 淇鎶€鑳芥€绘暟 64 鈫?62锛涙洿鏂?git hooks 鍒版渶鏂板悓姝ヨ剼鏈増鏈?|
| 1.1.3 | 2026-07-15 | docs: 鏂板瀹屾暣澶嶇洏楠岃瘉鎶ュ憡 `_FINAL_VERIFICATION_REPORT.md` |

---

*鏈」鐩敱 ZackAstra 缁存姢锛屾妧鑳芥潵婧愬寘鎷涓?Agent 骞冲彴鍐呯疆鎶€鑳藉拰鑷畾涔夋妧鑳姐€?
## 🆕 TeleAgent 接入说明

**TeleAgent** 是一款 Windows 桌面端 AI Agent 工具（v2.0.3），技能目录位于 C:\Users\zhaox\.config\TeleAgent\skills\。

### 同步机制

TeleAgent 采用 **Junction（目录联接）** 方式接入 CommonSkills：

| Agent 程序 | 技能目录路径 | 方式 |
|-----------|-----------|------|
| **TeleAgent** | ~/.config/TeleAgent/skills/CS_<skill-name> | Junction → ~/CommonSkills/<skill-name> |

### 命名约定

| 来源 | 在 TeleAgent 中的名称 | 说明 |
|------|---------------------|------|
| **CommonSkills** | CS_<skill-name> | Junction 指向 CommonSkills 源目录 |
| **TeleAgent 官方** | 保持原名 | canvas-design, docx 等内置技能 |
| **TeleAgent Hub** | 保持原名 | 	eleppt-pro, 	elecom-ppt-writer 等市场技能 |
| **TeleAgent → CommonSkills** | 保持原名 | 已添加 create_source: teleagent 标记 |
| **同名冲突** | Tele_<skill-name> | 如 Tele_skill-creator 避免与 CommonSkills 冲突 |

### 初始化

首次设置需以管理员身份运行：

`powershell
# 1. 停止 TeleAgent
Stop-Process -Name "TeleAgent" -Force

# 2. 运行初始化脚本
powershell -ExecutionPolicy Bypass -File "scripts\init-teleagent-junctions.ps1"
# 或手动执行：
# 备份
Copy-Item "C:\Users\zhaox\.config\TeleAgent\skills\*" "C:\Users\zhaox\CommonSkills\_backup\teleagent\" -Recurse
# 创建 junction
Get-ChildItem "C:\Users\zhaox\CommonSkills" -Directory | Where-Object { .Name -notin @('.git','scripts','_backup') } | ForEach-Object {
    New-Item -ItemType Junction -Path "C:\Users\zhaox\.config\TeleAgent\skills\CS_" -Target .FullName -Force
}

# 3. 重启 TeleAgent
Start-Process "D:\Program Files\TeleAgent\TeleAgent.exe"
`

### 日常维护

使用 scripts\sync-teleagent.ps1 脚本进行同步：

`powershell
# 检查状态（管理员）
powershell -ExecutionPolicy Bypass -File "scripts\sync-teleagent.ps1" -Action check

# 执行同步（管理员）
powershell -ExecutionPolicy Bypass -File "scripts\sync-teleagent.ps1" -Action sync

# 从备份恢复（管理员）
powershell -ExecutionPolicy Bypass -File "scripts\sync-teleagent.ps1" -Action restore
`

### 注意事项

- TeleAgent 的 .config\TeleAgent\skills\ 目录受 Windows 权限保护，**所有操作需管理员权限**
- TeleAgent 维护 skills-metadata.json 记录技能指纹，junction 内容实时更新，指纹自然匹配
- 部分 TeleAgent 内置技能（如 canvas-design、rontend-design）在 CommonSkills 中没有对应项
- 来自 TeleAgent Hub 的技能（如 	eleppt-pro、	elecom-ppt-writer）已反向导入 CommonSkills，create_source: teleagent 标记
- 如果 TeleAgent 更新版本，需检查 uildin-meta.json 确保技能加载逻辑未改变

