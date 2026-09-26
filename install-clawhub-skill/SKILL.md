---
name: Install ClawHub Skill
slug: install-clawhub-skill
version: 1.0.0
description: Install a skill from ClawHub registry into the user's .agent/skills directory, audit it for safety, and make it runnable in WorkBuddy (which is not OpenClaw).
metadata:
  openclaw:
    emoji: 🛠️
---

# Install ClawHub Skill for WorkBuddy

Use when the user wants to install an OpenClaw/ClawHub skill while running in WorkBuddy.

## Important differences

- WorkBuddy can load skills from `C:\Users\<user>\.agent\skills`, but it does **not** support the `openclaw exec` command.
- Therefore, after installing a ClawHub skill, you usually need to invoke its underlying script/tool directly (PowerShell, Node, Python, etc.) instead of relying on OpenClaw wrappers.

## Steps

1. **Verify ClawHub CLI is usable**
   ```bash
   npx clawhub@latest --help
   ```

2. **Search for the skill**
   ```bash
   npx clawhub@latest search <keyword>
   ```

3. **Audit before installing**  
   Install to a temporary directory first, read `SKILL.md` and any scripts, and verify there is no destructive behavior, network exfiltration, or credential theft.
   ```bash
   mkdir -p "C:/Users/<user>/.workbuddy/tmp/<skill>-audit"
   cd "C:/Users/<user>/.workbuddy/tmp/<skill>-audit"
   npx clawhub@latest install --dir . <skill-slug>
   ```

4. **Install to the user's skill directory**
   ```bash
   cd "C:/Users/<user>/.agent"
   npx clawhub@latest install --dir skills <skill-slug>
   ```

5. **Adapt execution for WorkBuddy**
   - Open the installed skill folder.
   - Identify the actual script/executable (e.g., `.ps1`, `.js`, `.py`).
   - Run it directly with the appropriate runtime.
   - If a script has a non-standard extension (e.g., `.txt`), copy or rename it to the required extension (e.g., `.ps1`) before execution.

6. **Handle output paths**
   - Many OpenClaw skills default to `$env:USERPROFILE\.openclaw\media`.
   - Set `OPENCLAW_MEDIA_DIR` or pass a custom output path so files land in the current workspace.

## Windows screenshot example

```powershell
$env:OPENCLAW_MEDIA_DIR = "C:\Users\<user>\WorkBuddy\Claw\.workbuddy\media"
powershell.exe -File "C:\Users\<user>\.agent\skills\windows-screenshot\screenshot.ps1"
```

## Safety rules

- Never install a skill without reading its `SKILL.md` and scripts first.
- Refuse skills that send data to remote servers, modify system files, or request elevated privileges without clear user benefit.
- For Windows PowerShell scripts, require `.ps1` extension before executing.
