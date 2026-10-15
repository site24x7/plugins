# Copilot Instructions: Site24x7 Plugins Repository

This repository (`site24x7/plugins`) hosts plugin integrations for the Site24x7 Linux and Windows server monitoring agents. The agent runs each plugin script, reads its JSON output, and pushes it to Site24x7. Languages: Python (majority), Shell, PowerShell, Batch, Java.

Docs:
- Plugin overview: https://www.site24x7.com/help/getting-started/plugins.html
- Linux plugin format: https://www.site24x7.com/help/admin/adding-a-monitor/plugins/custom-plugins.html
- Windows plugin format: https://www.site24x7.com/help/admin/adding-a-monitor/plugins/windows-custom-plugins.html
- Contributing: https://www.site24x7.com/help/developers/contribute-plugins.html

## Repository layout

One folder per plugin. The folder name and the main script name must be identical (`nginx/nginx.py`, `windows_defender/windows_defender.ps1`).

```
<plugin_name>/
  <plugin_name>.py | .sh | .ps1 | .bat   # plugin script (required)
  <plugin_name>.cfg                      # configuration (required if the plugin takes arguments)
  README.md                              # documentation (required)
  installer/Site24x7<Name>PluginInstaller.sh   # optional installer
  images/ or sample images               # optional dashboard screenshots
```

- Do not put multiple plugins in one folder. Do not edit unrelated plugin folders in the same PR.
- Plugin folders use lowercase snake_case (legacy exceptions such as `LinuxCommandMonitoring` exist; do not rename them).
- Install paths: Linux `/opt/site24x7/monagent/plugins/<plugin_name>/`, Windows `C:\Program Files (x86)\Site24x7\WinAgent\monitoring\plugins\<plugin_name>\`.

## Plugin output contract (blocking if violated)

The script must print a single JSON object to stdout and nothing else.

- `plugin_version`: required, whole number, default `1`. Must be incremented by 1 whenever metric keys, units, or tables change (this changes the plugin template).
- `heartbeat_required`: `true` or `false`. Default `true` for new plugins.
- Metrics: flat key/value pairs (numeric or string). Max 200 metrics per plugin.
- `units`: optional object mapping metric key to unit (`%`, `MB`, `ms`, `count`, ...). Every key in `units` must exist in the data. For tables, nest as `"units": {"<TableName>": {"<col>": "<unit>"}}`.
- `status`: reserved. `1` = up, `0` = down. Set `status = 0` and `msg = <error>` on any failure (connection, auth, parse, missing dependency). Never use `status` for other purposes.
- `msg`: optional error text shown when the monitor is down.
- `applog`: optional object for log collection: `logs_enabled`, `log_type_name`, `log_file_path`.
- Tabular data: a list of objects under a table key. Requires at least one top-level integer attribute. `name` is a reserved, case-sensitive column. Limits: 10 tables per plugin, 15 columns and 25 rows per table, 5 string columns per table, `name` up to 520 chars, other strings up to 100 chars.
- Do not use reserved keys as metric names (see https://support.site24x7.com/portal/en/kb/articles/reserved-keys-in-plugins).
- The script must always exit with valid JSON, including on exceptions. Wrap collection logic in try/except (or try/catch in PowerShell) and report via `status`/`msg`.
- Shell plugins may use the `key:value|key:value|units:{key-unit}` format; prefer Python JSON for new plugins.

Reference implementation: `nginx/nginx.py`.

## Python plugin conventions

- First line is a shebang (`#!/usr/bin/python`). Installers rewrite it to the agent or system Python path; do not hardcode user-specific paths.
- Must run on Python 3. If Python 2 compatibility is already present in a plugin, preserve it; do not add Python-2-only code to new plugins.
- Prefer the standard library. If a third-party module is needed, import it inside a try/except that returns `status = 0` with a message such as `"Install <module> module"`, and document the install command in the README.
- Read settings through `argparse` with defaults, including the standard arguments:
  `--plugin_version`, `--heartbeat`, `--logs_enabled`, `--log_type_name`, `--log_file_path`.
  This is what allows the agent to pass `.cfg` values as arguments and to run several instances from one script.
- Output with `print(json.dumps(result, indent=4, sort_keys=True))` under `if __name__ == '__main__':`.
- Set request/connection timeouts on every network call.
- Do not write temp files, state, or logs outside the plugin folder unless the plugin genuinely needs it; handle file encoding explicitly (`encoding='utf-8'`).
- Metric names are user-visible; use clear, human-readable, stable names. Renaming a key requires a `plugin_version` bump.

## Configuration (`.cfg`) conventions

- INI format. Section name identifies the instance (`[nginx]` or `[nginx-localhost]`). Multiple sections = multiple monitors from one script.
- Keys map 1:1 to the script's `argparse` arguments (e.g. `nginx_status_url` -> `--nginx_status_url`).
- Always include `plugin_version`, `heartbeat`, and the three log keys when the plugin supports logs.
- Values are quoted strings where the existing plugins do so (`host="localhost"`, `password="None"`); numbers unquoted (`port=3306`, `timeout=60`).
- Use placeholder values only. Never commit real hostnames, IPs, usernames, passwords, tokens, API keys, or client secrets.
- The agent encrypts `password` automatically on first run. Extra keys to encrypt go in `[global_configurations]` -> `keys_to_encrypt=password,username`.

## README requirements

Every plugin README.md should follow the structure of `nginx/README.md`:

1. Title: `# <Technology> Plugin` and a one-line purpose.
2. Installer one-liner (if an installer exists), using `https://raw.githubusercontent.com/site24x7/plugins/master/<plugin_name>/...`.
3. Prerequisites: Site24x7 Linux/Windows agent, language/runtime version, required modules, required DB/application privileges, and any application-side setup (status endpoints, users, permissions).
4. Plugin installation (manual): create folder, download files, verify JSON by running the script manually with arguments, fill the `.cfg`, move the folder into the agent plugin directory.
5. Configuration table or `.cfg` example with placeholder values.
6. Supported metrics table: metric name and description (and unit).
7. Sample output/dashboard image if available (store under the plugin folder; use relative or raw GitHub links).

Rules: all download URLs point at `site24x7/plugins/master`; commands must be copy-pasteable; mention the Windows variant only if the plugin supports it.

## Installer scripts (`installer/*.sh`)

- Named `Site24x7<Name>PluginInstaller.sh`.
- Check prerequisites (agent installed, Python present, required modules), create the plugin folder under `/opt/site24x7/monagent/plugins/`, download the script and `.cfg` from `master`, and set the Python shebang.
- Must be idempotent and must not delete or overwrite unrelated files. Do not run destructive commands (`rm -rf` on variable paths) without guarding the variable.
- Do not pass credentials through insecure channels or echo them to logs.

## Windows plugins

- PowerShell (`.ps1`), Batch, VB, or DLL. Output the same JSON contract (`plugin_version`, `heartbeat_required`, metrics, `units`, `status`, `msg`).
- Use `try/catch` and set `status = 0` plus `msg` on failure. Avoid prompts or interactive input. Convert output with `ConvertTo-Json`.
- Python plugins on Windows must not rely on a Linux shebang (see `okta` history: the header was removed to fix a Windows error).

## Security review checklist

- No hardcoded credentials, tokens, private keys, internal hostnames, or customer data in any file, README, or sample image.
- No `eval`/`exec` on external input; no `shell=True` or string-concatenated shell commands with user-supplied values. Use argument lists for `subprocess`.
- Parameterize SQL; for custom-query plugins validate that only read operations are executed and document required read-only privileges.
- Prefer HTTPS and certificate verification; if `verify=False` / `--no-check-certificate` is offered, make it opt-in and documented.
- Minimum privileges: README must document the least-privileged account needed.
- Do not log secrets in `msg` or stdout.
- Do not include secrets in exception text copied to `msg` (connection strings, URLs with embedded credentials, auth headers).
- Credentials must come from `.cfg`/arguments only, never from defaults in code. Placeholders in `.cfg`/README must be obviously fake (`"None"`, `<password>`).
- Validate and bound user-supplied values (ports, paths, URLs, query strings). Reject path traversal in file-path arguments (`log_file_path`, folder names) and do not follow untrusted symlinks.
- Installers: download only from `site24x7/plugins/master` over HTTPS, quote all variables, avoid `curl | sh` of third-party URLs, never `chmod 777`, and do not require running the plugin itself as root unless documented.
- Subprocess calls: fixed executable, argument list, timeout set, output size bounded; no `shell=True`.
- Third-party modules: document the install command in the README and do not auto-install at runtime.
- Flag any new network destination, file write outside the plugin folder, or privilege requirement in the PR description.

## Code review: logic and correctness

When reviewing or generating plugin code, verify:

- **Failure paths:** every network call, file read, subprocess, and parse is inside try/except (try/catch). A failure sets `status = 0` and `msg`, and the script still prints valid JSON. No bare `except: pass` that hides errors and reports `status` 1 with empty data.
- **Partial data:** a missing or `None` metric is omitted or reported as an explicit value, not as a fabricated `0`. A single failed sub-query must not crash the whole collection.
- **Types and units:** numeric metrics are numbers, not numeric strings (convert with `int()`/`float()` and handle the failure). Units match the value (bytes vs MB, ms vs s, ratio vs %). Conversions and divisions guard against division by zero.
- **Counters vs gauges:** cumulative counters are not reported as rates without a documented, persisted previous sample. Any state file lives in the plugin folder.
- **Limits:** metric count <= 200; table rows <= 25 and columns <= 15 (truncate or sort deterministically before output); string lengths within limits.
- **Argument handling:** `argparse` types and defaults are correct. Do not use `type=bool` for flags (any non-empty string is `True`); parse `"true"/"false"` explicitly for new code. Instance-specific `.cfg` arguments must match the script's CLI arguments; exempt agent-only settings such as `use_agent_python` and `keys_to_encrypt` under `[global_configurations]`. Optional CLI arguments may use their documented defaults when omitted from `.cfg`.
- **Config sections:** each `.cfg` section runs independently; the script must not rely on global state shared across invocations.
- **Timeouts and performance:** every network call has a timeout lower than the agent's script execution timeout (default 50 seconds). No unbounded loops, unbounded pagination, or full-file reads of large logs.
- **Python compatibility:** no syntax that breaks the Python versions stated in the README (f-strings, walrus operator, `match`); keep existing Python 2 compatibility where already present.
- **Encoding and locale:** read/write with explicit `encoding='utf-8'`; decode bytes from subprocess/HTTP before JSON serialization; do not depend on locale-specific command output.
- **Output cleanliness:** no debug `print`, warnings, or stack traces on stdout (send diagnostics to stderr or omit). `json.dumps` input contains only serializable values (no `datetime`, `bytes`, `Decimal` without conversion).
- **Idempotency:** repeated runs produce the same shape of output; key names do not change between runs (changes require a `plugin_version` bump).
- **Windows:** PowerShell scripts set `$ErrorActionPreference = 'Stop'` inside try/catch, avoid culture-specific number formatting, and emit a single `ConvertTo-Json` object.

Review output format: list findings grouped as **Security**, **Logic**, and **Style/Docs**, each with severity (blocking, should-fix, nit), file and line, and a concrete suggested fix. State explicitly when no issues are found in a category.

## Pull request guidelines

Scope:
- One plugin (or one logical fix) per PR. Branch from `master`; use descriptive branch names (e.g. `milvus_monitoring`, `fix-postgres-17-bg-stats`).
- Do not include IDE files, `__pycache__`, `.DS_Store`, compiled files, or large binaries.
- Keep the license header/author conventions of the existing files; the repository is BSD-licensed (`LICENSE.txt`).

PR title: `<plugin_name>: <short imperative summary>` (e.g. `weaviate_monitoring: add new plugin`, `mysql: fix max_connections type`).

PR description must contain:
- What changed and why (new plugin, new metrics, bug fix, docs).
- `plugin_version` change and the reason (required when keys/units/tables change).
- Supported OS and runtime versions tested (Linux/Windows, Python/PowerShell version, application version).
- Sample JSON output from a manual run.
- Screenshot of the plugin monitor in Site24x7 for new plugins or UI-visible changes.
- Any new prerequisites, privileges, or modules.

Reviewer checklist (apply when reviewing or generating a PR):
- [ ] Folder name == script name == `.cfg` name; README present.
- [ ] Script prints only valid JSON; includes `plugin_version`, `heartbeat_required`.
- [ ] Failure paths set `status: 0` and a useful `msg`; no uncaught exceptions or stack traces on stdout.
- [ ] `units` keys all exist in metrics; metric/column counts within limits.
- [ ] `plugin_version` bumped if metrics/units/tables changed.
- [ ] `.cfg` keys match script arguments, contain placeholders only, and have timeouts.
- [ ] README follows the template: prerequisites, install steps, config, metrics table, correct `master` URLs.
- [ ] Installer (if present) is safe, idempotent, and uses the correct agent path.
- [ ] No secrets, no unrelated file changes, no generated or binary clutter.
- [ ] Security review done (see Security review checklist): no injection, no secret leakage, least privilege, safe installer.
- [ ] Logic review done (see Code review: logic and correctness): failure paths, types/units, limits, timeouts, clean stdout.
- [ ] Verified by running the script manually and confirming valid JSON (`python3 <plugin>.py ... | python3 -m json.tool`).

## Guidance for Copilot when editing this repo

- Follow the nearest existing plugin (for example `nginx/`, `mysql/`, `milvus/`) as the template; do not invent new structures.
- Keep changes minimal and scoped to the plugin being modified; do not reformat or refactor unrelated code.
- When adding or removing a metric, update the script, `units`, README metrics table, and `plugin_version` together.
- When adding a CLI argument, update the `.cfg`, the README example, and any installer that writes the `.cfg`.
- Never fabricate metrics, endpoints, or privileges; base them on the application's official documentation.
- Ask for the target application version and OS if unspecified.
