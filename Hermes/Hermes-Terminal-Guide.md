---
tags:
  - hermes
  - terminal
  - cli
  - reference
  - guide
  - tooling
type: reference
created: 2026-07-07
source: hermes-agent skill + live `hermes --help`
---

# Hermes Agent — Terminal Commands & Usage Guide

> A full, educational reference for driving Hermes Agent from the terminal/CLI.
> Compiled from the `hermes-agent` skill and verified against the live `hermes --help`
> / `hermes chat --help` output on this machine (2026-07-07). Run `hermes --version`
> to see your installed build — command details may shift between versions, so the
> binary's own `--help` is always the final authority.

---

## 0. 60-Second Start

```bash
hermes                    # launch interactive chat (REPL)
hermes --tui              # launch the modern TUI instead of the classic REPL
hermes -z "fix the typo in ~/foo.txt"   # one-shot, prints ONLY the final answer (script-friendly)
hermes chat -q "what is my IP?"         # single query, non-interactive-ish
hermes -c                 # resume the most recent session
hermes doctor             # health check of config + dependencies
hermes --help             # the full command list (always current)
```

Hermes has **two ways to run**:

1. **Interactive chat** (`hermes`, `hermes chat`) — you and the agent talk live in the terminal. This is the default and does **not** need the gateway.
2. **One-shot / scriptable** (`hermes -z "..."`) — send one prompt, get only the final text back on stdout. Built for pipes, scripts, and CI.

Everything else below is a management command (`hermes config`, `hermes skills`, `hermes cron`, …) or an in-session slash command (`/reset`, `/model`, …).

---

## 1. Mental Model: Terminal vs Gateway

| You are… | Use | Needs gateway? |
|---|---|---|
| At the terminal, talking face-to-face | `hermes`, `hermes chat -q` | No |
| Running it from a script / cron / CI | `hermes -z`, `hermes chat -q` | No |
| Reached from Telegram / Discord / Slack | the **gateway** (`hermes gateway start`) | Yes |

The **gateway** is a background process that waits for messages from messaging platforms and routes them to the agent. You only need it if you want to talk to Hermes from somewhere other than the terminal. This guide is **terminal-first**; the gateway gets a short section at the end (§9) rather than a centerpiece.

---

## 2. Global Flags (apply to `hermes` itself)

These go before the subcommand: `hermes [FLAGS] <command>`.

| Flag | Meaning |
|---|---|
| `--version`, `-V` | Print version and exit |
| `-z PROMPT`, `--oneshot PROMPT` | **One-shot mode**: send a single prompt, print ONLY the final response text to stdout. No banner, no spinner, no tool previews, no session-id line. Approvals auto-bypassed. Ideal for scripts/pipes. |
| `--usage-file PATH` | One-shot only: write a JSON usage report (cost, tokens, model, api_calls) to PATH after the run — even if it fails. |
| `-m MODEL`, `--model MODEL` | Model override for this invocation (e.g. `anthropic/claude-sonnet-4`). Also `HERMES_INFERENCE_MODEL` env var. |
| `--provider PROVIDER` | Provider override (e.g. `openrouter`, `anthropic`). Persistent provider lives in `config.yaml` under `model.provider`. |
| `-t TOOLSETS`, `--toolsets TOOLSETS` | Comma-separated toolsets to enable for this run (e.g. `web,terminal`). |
| `--resume SESSION`, `-r SESSION` | Resume a previous session by ID or title |
| `--continue [NAME]`, `-c [NAME]` | Resume by name, or most recent if no name |
| `--worktree`, `-w` | Run in an isolated git worktree (parallel agents on the same repo) |
| `--accept-hooks` | Auto-approve unseen shell hooks (CI/headless). Same as `HERMES_ACCEPT_HOOKS=1`. |
| `--skills SKILLS`, `-s SKILLS` | Preload one or more skills (repeat flag or comma-separate) |
| `--yolo` | Bypass all dangerous-command approval prompts (use at your own risk) |
| `--pass-session-id` | Include the session ID in the agent's system prompt |
| `--ignore-user-config` | Ignore `~/.hermes/config.yaml`; fall back to built-in defaults (`.env` creds still load) |
| `--ignore-rules` | Skip auto-injection of `AGENTS.md`, `SOUL.md`, `.cursorrules`, memory, preloaded skills |
| `--safe-mode` | Troubleshooting: disable ALL customizations (implies the two above) |
| `--tui` | Launch the modern TUI |
| `--cli` | Force the classic prompt_toolkit REPL (overrides `display.interface: tui`) |
| `--dev` | With `--tui`: run TypeScript sources via tsx (skip dist build) |

> **Note:** with no subcommand, `hermes` defaults to `chat`. So `hermes` == `hermes chat`.

---

## 3. `hermes chat` — Interactive & One-Shot Chat

```bash
hermes chat                          # interactive session
hermes chat -q "Hello"              # single query (banner + spinner shown)
hermes chat -q "describe this" --image ~/screenshot.png
hermes chat -q "refactor x.py" -m anthropic/claude-sonnet-4 -t terminal,file
hermes chat -q "research X" -s hermes-agent,github   # preload skills
hermes chat --resume <session_id>   # resume specific session
hermes chat -c "my project"         # resume by name
hermes chat --checkpoints           # enable /rollback for destructive file ops
hermes chat --max-turns 20          # cap tool-calling iterations per turn
hermes chat -Q                      # quiet: suppress banner/spinner/previews (programmatic)
hermes chat --source tool           # tag session source (keeps it out of user session lists)
```

| Flag | Meaning |
|---|---|
| `-q, --query QUERY` | Single query (non-interactive mode) |
| `--image IMAGE` | Local image path to attach to a single query |
| `-m, --model MODEL` | Model to use |
| `-t, --toolsets TOOLSETS` | Comma-separated toolsets to enable |
| `-s, --skills SKILLS` | Preload one or more skills |
| `--provider PROVIDER` | Inference provider (default auto) |
| `-v, --verbose` | Verbose output |
| `-Q, --quiet` | Quiet: suppress banner, spinner, tool previews |
| `--resume / --continue` | Resume a session (by ID / by name) |
| `--worktree / --accept-hooks / --checkpoints` | worktree mode / auto-approve hooks / filesystem checkpoints |
| `--max-turns N` | Max tool-calling iterations per turn (default 90) |
| `--yolo / --pass-session-id` | approval bypass / pass session id |
| `--ignore-user-config / --ignore-rules / --safe-mode` | isolation flags |
| `--source SOURCE` | Session source tag (default `cli`; use `tool` for integrations) |
| `--tui / --cli / --dev` | interface selection |

---

## 4. CLI Command Reference (management commands)

Below are the management subcommands. Grouped by purpose. Run `hermes <cmd> --help` for the full flag list of any of them.

### 4.1 Setup, config & health

| Command | What it does |
|---|---|
| `hermes setup [section]` | Interactive wizard: `model`, `terminal`, `gateway`, `tools`, `agent` |
| `hermes model` | Interactive model/provider picker (sets the default) |
| `hermes config` | View current config. Subcommands: `show`, `edit` (opens `config.yaml` in `$EDITOR`), `set KEY VAL`, `path`, `env-path`, `check`, `migrate` |
| `hermes config set model gpt-4` | Set a single config value non-interactively |
| `hermes doctor [--fix]` | Diagnose config + dependencies. `--fix` attempts auto-fix. `--ack ID` silences a security advisory |
| `hermes status [--all] [--deep]` | Show component status (`--deep` = slower thorough checks) |
| `hermes migrate` | Migrate config for retired models / deprecated settings |
| `hermes postinstall` | Bootstrap non-Python deps (node, browser, ripgrep, ffmpeg) |
| `hermes dump` | Dump a setup summary for support/debugging |
| `hermes debug share` | Upload logs + system info for support |
| `hermes prompt-size` | Byte breakdown of system prompt + tool schemas |

**Key paths**

```
~/.hermes/config.yaml                  Main configuration
~/.hermes/.env                         Root-level API keys (shared by all profiles)
~/.hermes/profiles/<name>/.env         Profile-specific keys (override root on duplicates)
~/.hermes/sessions/                    Session transcripts (SQLite)
~/.hermes/logs/                        Gateway + error logs
~/.hermes/auth.json                    OAuth token / credential pool (PER PROFILE)
```

`.env` loading order: **root first**, then **profile** (profile wins on duplicates).

### 4.2 Auth & credentials

| Command | What it does |
|---|---|
| `hermes auth add <provider> --type oauth` | OAuth device-code login (replaces old `hermes login`). e.g. `hermes auth add nous --type oauth` |
| `hermes auth list [provider]` | List pooled credentials |
| `hermes auth remove <p> <t>` | Remove a credential by provider + index/id/label |
| `hermes auth reset <provider>` | Clear exhaustion status for a provider |
| `hermes logout` | Clear stored auth for an inference provider |
| `hermes login` | (Legacy) re-authenticate OAuth — prefer `hermes auth add` |
| `hermes secrets bitwarden|onepassword` | Pull API keys from Bitwarden / 1Password at startup instead of `.env` |

> **Gotcha — credentials are per-profile.** Each profile has its own `auth.json`. API keys in `.env` are shared (root→profile), but **OAuth tokens are not** — a profile you don't authenticate in starts with an empty pool.

### 4.3 Models & providers

| Command | What it does |
|---|---|
| `hermes model` | Pick default model + provider |
| `hermes moa {list,configure,delete}` | Configure the Mixture-of-Agents model slots used by `/moa <prompt>` |
| `hermes fallback {list,add,remove,clear}` | Manage the fallback provider chain — tried in order when the primary fails (rate-limit / overload / connection) |
| `hermes proxy` | Local OpenAI-compatible proxy to OAuth providers |

### 4.4 Tools, skills & extensions

| Command | What it does |
|---|---|
| `hermes tools` | Interactive tool enable/disable (curses UI). Subcommands: `list`, `enable NAME`, `disable NAME`, `post-setup` |
| `hermes tools list --summary` | Print enabled tools per platform |
| `hermes skills` | Search/install/manage skills. Subcommands: `browse`, `search QUERY`, `install ID`, `inspect ID`, `list`, `check`, `update`, `audit`, `uninstall`, `diff`, `reset`, `config`, `tap add REPO`, `publish PATH`, `snapshot` |
| `hermes bundles` | Create/list/manage **skill bundles** — one slash command (`/<bundle>`) that loads several skills at once |
| `hermes mcp` | Manage MCP servers + run Hermes as an MCP server. Subcommands: `serve`, `add`, `remove`, `list`, `test`, `configure`, `login`, `reauth`, `catalog`, `install` |
| `hermes lsp` | Language Server Protocol management (semantic diagnostics). Subcommands: `status`, `list`, `install <id>`, `install-all`, `restart`, `which <id>` |
| `hermes plugins` | Manage plugins (code that registers new tools). Subcommands: `list`, `install <repo> --enable`, `remove`, … |
| `hermes hooks` | Inspect shell-script hooks: `list`, `test <event>`, `revoke`, `doctor` |
| `hermes computer-use` | Manage the Computer Use (cua-driver) backend (macOS/Windows/Linux) |
| `hermes curator` | Background skill-maintenance (curator) status/run/pause/pin |

**Skills vs Plugins (don't mix them up):**

| | Skill | Plugin |
|---|---|---|
| Manifest | `SKILL.md` (markdown) | `plugin.yaml` |
| Content | Methodology / procedures | Python code that registers tools |
| Install | `hermes skills install <id>` | `hermes plugins install <repo> --enable` |
| Location | `~/.hermes/skills/` or `~/.hermes/profiles/<name>/skills/` | `~/.hermes/plugins/` or profile equivalent |

### 4.5 Sessions, projects & profiles

| Command | What it does |
|---|---|
| `hermes sessions` | Manage session history. Subcommands: `list`, `export OUT`, `delete ID`, `prune [--older-than N days]`, `archive`, `optimize` (FTS5 merge + VACUUM), `repair`, `stats`, `rename ID TITLE`, `browse` (interactive picker) |
| `hermes project` | Named multi-folder workspaces. Subcommands: `create`, `list`, `show`, `add-folder`, `remove-folder`, `rename`, `set-primary`, `use`, `archive`, `restore`, `bind-board` |
| `hermes profile` | Multiple isolated Hermes instances. Subcommands: `list`, `use NAME` (sticky default), `create NAME [--clone …]`, `delete`, `show`, `alias`, `rename A B`, `export`, `import`, `install <git-url>`, `update`, `info` |
| `hermes kanban` | Durable SQLite task board shared across profiles (multi-agent orchestration). Subcommands include `init`, `create`, `swarm`, `list`, `show`, `assign`, `claim`, `complete`, `block`, `schedule`, `daemon`, `dispatch`, `decompose`, `gc`, … |

> **Profiles** are independent Hermes instances with isolated config, sessions, skills, memory, and (crucially) **their own gateway + credential pool**. `hermes profile use senna` makes one the sticky default so bare `hermes …` commands target it.

### 4.6 Automation: cron, webhooks, send

| Command | What it does |
|---|---|
| `hermes cron` | Scheduled tasks. Subcommands: `list`, `create SCHED` (`'30m'`, `'every 2h'`, `'0 9 * * *'`), `edit ID`, `pause/resume ID`, `run ID`, `remove ID`, `status`, `tick` |
| `hermes webhook` | Dynamic webhook subscriptions: `subscribe NAME`, `list`, `remove NAME`, `test NAME` |
| `hermes send` | Pipe text to a configured platform (Telegram/Discord/Slack/Signal) — no LLM, no running gateway needed for bot-token platforms. Flags: `-t/--to TARGET`, `-f/--file PATH`, `-s/--subject`, `-l/--list`, `-q`, `--json`. Example: `echo "RAM 92%" \| hermes send --to telegram` |

**Cron delivery modes:** `deliver: local` (silent — maintenance only), `deliver: origin` (report to your home channel). Long-running bounded tasks should use `notify_on_complete`; deterministic shell-only jobs can use **no_agent script mode** (zero tokens).

### 4.7 Gateway (messaging platforms) — short version

| Command | What it does |
|---|---|
| `hermes gateway run` | Run gateway in foreground |
| `hermes gateway install` | Install as a systemd/launchd background service |
| `hermes gateway start/stop/restart` | Control the service |
| `hermes gateway status` | Show status |
| `hermes gateway list` | List all profiles + their gateway status |
| `hermes gateway setup` | Configure platforms (Telegram, Discord, Slack, WhatsApp, Signal, Email, Matrix, …) |
| `hermes gateway enroll` | Enroll with a relay connector |

> Each profile has its own gateway. To expose the OpenAI-compatible HTTP API, set `API_SERVER_ENABLED=true` in the **profile** `.env` *before* starting the gateway (it's snapshotted at startup).

### 4.8 Memory & secrets

| Command | What it does |
|---|---|
| `hermes memory` | Configure an external memory provider (`setup` / `status` / `off`) |
| `hermes memory-graph` | Memory graph utilities |
| `hermes journey` | Timeline of learned skills + memories over time |
| `hermes learning` | Learning/memory-graph utilities |
| `hermes secrets` | Bitwarden / 1Password secret sourcing (see §4.2) |

### 4.9 Diagnostics, logs, backups & housekeeping

| Command | What it does |
|---|---|
| `hermes logs` | View/filter logs: `agent` (default), `errors`, `gateway`, `gui`, `desktop`. Flags: `-n LINES`, `-f` (follow), `--level`, `--session ID`, `--since 1h`, `--component`. `hermes logs list` shows files |
| `hermes insights [--days N]` | Usage analytics |
| `hermes security` | Supply-chain audit (OSV.dev) for venv, plugins, MCP servers |
| `hermes backup` | Back up `~/.hermes` to a zip |
| `hermes import` | Restore a backup from zip |
| `hermes checkpoints` | Inspect/prune/clear `~/.hermes/checkpoints/` |
| `hermes completion {bash,zsh,fish}` | Print shell completion script → source it in your shell rc |
| `hermes console` | Open the safe Hermes command console |
| `hermes pairing` | Manage DM pairing codes for user authorization |
| `hermes update` | Update to latest version |
| `hermes uninstall` | Uninstall Hermes |
| `hermes version` | Show version |
| `hermes claw` | OpenClaw migration tools |

### 4.10 Frontends & servers

| Command | What it does |
|---|---|
| `hermes dashboard` | Web UI dashboard (port 9119). `--stop`, `--status`, `--no-open`, `--isolated`, `--register` (Nous Portal OAuth) |
| `hermes serve` | Headless backend server (powers desktop app + remote backends) |
| `hermes desktop` (alias `gui`) | Build + launch the native desktop app |
| `hermes acp` | Run as an ACP (Agent Client Protocol) server (IDE integration) |
| `hermes pets` | Browse/install animated "petdex" pets (cosmetic) |

---

## 5. In-Session Slash Commands

Type these during an interactive chat. Many mirror the CLI but act on the *live* session.

### Session control
```
/new  (/reset)       Fresh session
/clear               Clear screen + new session (CLI)
/retry               Resend last message
/undo                Remove last exchange
/title [name]        Name the session
/compress            Manually compress context
/stop                Kill background processes
/rollback [N]        Restore filesystem checkpoint (needs --checkpoints at launch)
/background <prompt> Run a prompt in the background
/queue <prompt>      Queue for next turn
/resume [name]       Resume a named session
```

### Configuration (live)
```
/config              Show config (CLI)
/model [name]        Show or change model
/personality [name]  Set personality
/reasoning [level]   none|minimal|low|medium|high|xhigh|show|hide
/verbose             Cycle: off → new → all → verbose
/voice [on|off|tts]  Voice mode (see note)
/yolo                Toggle approval bypass
/skin [name]         Change theme (CLI)
/statusbar           Toggle status bar (CLI)
```

> **`/voice on` vs `/voice tts`:** `/voice tts` = agent speaks replies, you still type. `/voice on` = bidirectional (you speak, it speaks). Both need `/reset` (CLI) or `/restart` (gateway) after config change.

### Tools & skills
```
/tools               Manage tools (CLI)
/toolsets            List toolsets (CLI)
/skills              Search/install skills (CLI)
/skill <name>        Load a skill into the session
/cron                Manage cron jobs (CLI)
/reload-mcp          Reload MCP servers
/plugins             List plugins (CLI)
```

### Gateway (only meaningful when a gateway is running)
```
/approve             Approve a pending command
/deny                Deny a pending command
/restart             Restart gateway
/sethome             Set current chat as home channel
/update              Update Hermes (gateway)
/platforms (/gateway)  Show platform connection status
```

### Utility
```
/branch (/fork)      Branch the current session
/fast                Toggle priority/fast processing
/browser             Open CDP browser connection
/history             Show conversation history (CLI)
/save                Save conversation to file (CLI)
/paste               Attach clipboard image (CLI)
/image               Attach local image file (CLI)
```

### Info & exit
```
/help                Show commands
/commands [page]     Browse all commands (gateway)
/usage               Token usage
/insights [days]     Usage analytics
/status              Session info (gateway)
/profile             Active profile info
/quit (/exit, /q)    Exit CLI
```

---

## 6. Ways to Use Hermes from the Terminal (practical workflows)

This is the "how do I actually drive this thing" section.

### 6.1 Daily interactive driver
```bash
hermes                 # classic REPL
hermes --tui           # modern TUI (set display.interface: tui in config to make default)
```
Inside: ask questions, let it use tools (terminal, file, web, browser…), `/reset` to start fresh, `/model` to swap models mid-session.

### 6.2 One-shot from a script or pipe
Use `-z` when you want *only the answer* on stdout — no banner, no spinner, no session id. Perfect for scripts.
```bash
# Summarize a log file
hermes -z "summarize the key errors in this file: $(cat /tmp/app.log)"

# Pipe stdin
cat report.md | hermes -z "give me a 3-bullet TL;DR"

# Track cost
hermes -z "explain quicksort" --usage-file /tmp/usage.json

# Exit code is usable in scripts; usage report is written even on failure
```

### 6.3 Attach an image
```bash
hermes chat -q "what's wrong in this screenshot?" --image ~/Desktop/error.png
```

### 6.4 Resume where you left off
```bash
hermes -c                  # most recent session
hermes -c "murim combat"   # by name (latest in lineage)
hermes --resume <id>       # exact session id (shown on exit / in hermes sessions list)
```
`hermes sessions list` shows titles + ids; `hermes sessions browse` is an interactive picker.

### 6.5 Scope tools & skills per run
```bash
hermes -t web,terminal,file          # only these toolsets this run
hermes -s hermes-agent,github        # preload specific skills
hermes -m anthropic/claude-sonnet-4 -t code_execution   # specific model + toolset
```

### 6.6 Run a long task in the background (shell-level)
```bash
hermes chat -q 'Set up CI/CD for ~/myapp and report when done' &
# …or use the in-session /background <prompt> for agent-managed background work
```

### 6.7 Profiles for isolation
```bash
hermes profile list                 # see all profiles + which is default (◆)
hermes -p senna chat -q "..."       # run one command as the senna profile
hermes profile use senna            # make senna the sticky default
```
Each profile = isolated config, memory, skills, sessions, gateway, credentials.

### 6.8 Automate with cron (no LLM needed for checks)
```bash
hermes cron create '0 3 * * *' --prompt "Consolidate old memory" --deliver local
# For pure-shell deterministic jobs, convert to no_agent script mode (zero tokens):
#   cronjob update <ID> --script "my-scan.sh" --no-agent true
```
Pipeline idea: silent maintenance jobs at 2–5am, a reporting briefing at 7am that summarizes them.

### 6.9 Send notifications from any script
```bash
# No gateway running needed for bot-token platforms
./deploy.sh && hermes send --to telegram "deploy finished"
echo "RAM 92%" | hermes send --to telegram:-1001234567890
hermes send --to discord:#ops --file /tmp/report.md
```

### 6.10 Shell completion (stop retyping)
```bash
hermes completion zsh >> ~/.zshrc     # then restart shell
hermes completion bash >> ~/.bashrc
hermes completion fish  > ~/.config/fish/completions/hermes.fish
```

### 6.11 TUI vs CLI vs Desktop
- `--cli` forces the classic REPL even if `display.interface: tui` is set.
- `--tui` forces the modern TUI.
- `hermes desktop` builds/launches a native GUI app; `hermes dashboard` starts a web UI on port 9119.

### 6.12 Safety / isolation flags
```bash
hermes --yolo                  # skip all approval prompts (careful!)
hermes --safe-mode             # disable ALL customizations — isolate setup vs Hermes bugs
hermes --ignore-rules          # skip AGENTS.md/SOUL.md/memory injection
hermes --ignore-user-config    # fall back to built-in defaults
```
Use `--safe-mode` when diagnosing whether a problem is your config or Hermes itself.

---

## 7. Tips & Gotchas (learned the hard way)

- **Tool/skill changes need a fresh session.** Enabling a toolset or installing a skill takes effect on `/reset` (CLI) or `/restart` (gateway) — not mid-conversation (preserves prompt caching).
- **`/new` freeze:** a known issue can leave `/new` hanging or create a 0-message session. If it happens, exit and relaunch, or use `hermes chat` fresh.
- **Credentials are per-profile.** OAuth tokens don't inherit across profiles; API keys in `.env` do (root → profile override).
- **Gateway is per-profile too.** `hermes gateway status` shows *which* profile's gateway is running. Use `hermes profile use <name>` then `hermes gateway start` to avoid a two-gateway mess.
- **`API_SERVER_ENABLED=true` must be set before the gateway starts** — it's snapshotted at process launch.
- **`hermesd --profile senna` is broken** (`Profile 'senna' does not exist`). Run `hermesd` with no flag; it detects the gateway via process scan.
- **`--resume` vs `-c`:** `--resume <id>` is exact; `-c [name]` resumes by name or most-recent. Both reopen full history + memory.
- **One-shot = clean stdout.** Reach for `hermes -z` (not `hermes chat -q`) whenever another program will parse the output.
- **`.env` location matters.** Don't put active keys in `~/.hermes/archive/.env` — that's for state snapshots only.
- **LSP diagnostics** only run inside a git worktree and fail silently if a language server is missing — they never block a write.

---

## 8. Quick Cheat Sheet

```bash
# Talk
hermes                                   # interactive
hermes --tui                             # modern TUI
hermes -z "do X"                         # one-shot, clean stdout
hermes chat -q "do X" --image ~/x.png    # with image

# Resume
hermes -c                                # latest session
hermes --resume <id>                     # exact id

# Scope
hermes -t web,terminal -s hermes-agent   # toolsets + skills
hermes -m anthropic/claude-sonnet-4       # model override
hermes -p senna chat -q "..."             # run as profile

# Manage
hermes doctor                            # health
hermes config set model gpt-4            # config
hermes skills install <id>               # add a skill
hermes tools list --summary              # what's enabled
hermes cron create '0 9 * * *' --prompt "…"   # schedule
hermes logs -f                           # follow logs
hermes sessions list                     # history
hermes profile list                      # profiles
hermes completion zsh >> ~/.zshrc        # shell completion
hermes send --to telegram "done"         # notify

# Isolate / recover
hermes --safe-mode                       # disable all customizations
hermes --yolo                            # skip approvals
```

---

*Generated for the Senna profile. Source of truth: the `hermes-agent` skill + live `hermes --help` output. For the always-current reference, see https://hermes-agent.nousresearch.com/docs/*
