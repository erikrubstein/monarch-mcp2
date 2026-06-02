# monarch-mcp2

Unofficial MCP server for Monarch Money.

This project is not affiliated with, endorsed by, or supported by Monarch Money.

`monarch-mcp2` gives agents like Codex and Claude access to Monarch Money
through Model Context Protocol tools. It exposes the public function surface
from [`monarch-api2`](https://github.com/erikrubstein/monarch-api2), organized
by Monarch feature area, with tool names that map 1-to-1 to backend API
functions:

```text
{group}_{function_name}
```

## Features

- MCP tools backed directly by `monarch-api2`, not the CLI
- 1-to-1 tool names matching the API function surface
- Typed input schemas for filters, enums, nested objects, and mutations
- Tool annotations for read-only, write, and destructive operations
- Compact `summary` output by default, similar to the CLI's table/detail views
- `full` output when agents need the complete structured API data
- `raw` output when agents explicitly need retained raw response payloads
- Dotted-path field projection for targeted output
- Tools for auth, accounts, transactions, receipts, cashflow, reports,
  merchants, tags, household, categories, recurring items, investments, goals,
  and budgets

## Installation

This package depends on `monarch-api2` version `0.1.0`, installed directly from
GitHub:

```toml
monarch-api2 @ git+https://github.com/erikrubstein/monarch-api2.git@v0.1.0
```

Install the MCP server from GitHub:

```bash
pipx install git+https://github.com/erikrubstein/monarch-mcp2.git
```

After installation, confirm the `monarch-mcp` command is available:

```bash
which monarch-mcp
```

## Codex

Add the server to Codex:

```bash
codex mcp add monarch -- monarch-mcp
```

If your session file is somewhere other than the default path, include
`MONARCH_SESSION_PATH`:

```bash
codex mcp add \
  --env MONARCH_SESSION_PATH="/absolute/path/to/session.json" \
  monarch \
  -- monarch-mcp
```

Verify the server was added:

```bash
codex mcp list
```

Restart Codex after adding the server. Once loaded, Codex should see tools such
as `accounts_list_accounts`, `transactions_list_transactions`, and
`budget_get_budget`.

## Claude Code

Add the server to Claude Code:

```bash
claude mcp add --scope user monarch -- monarch-mcp
```

If your session file is somewhere other than the default path, include
`MONARCH_SESSION_PATH`:

```bash
claude mcp add \
  --scope user \
  -e MONARCH_SESSION_PATH="/absolute/path/to/session.json" \
  monarch \
  -- monarch-mcp
```

Verify the server was added:

```bash
claude mcp list
```

Restart Claude Code after adding the server.

## Claude Desktop

Claude Desktop uses a JSON config file rather than the Claude Code `claude mcp`
command.

On macOS, the config file is usually:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

Example:

```json
{
  "mcpServers": {
    "monarch": {
      "command": "/absolute/path/to/monarch-mcp",
      "args": [],
      "env": {
        "MONARCH_SESSION_PATH": "/absolute/path/to/session.json"
      }
    }
  }
}
```

Restart Claude Desktop after editing the config.

## Sessions

The default session file is:

```text
~/.config/monarch/session.json
```

You can override it with `MONARCH_SESSION_PATH`, or set `MONARCH_CONFIG_DIR` to
change the config directory.

Use `auth_create_session` to create a Monarch session. Auth tools redact the
session token by default. Set `include_token=true` only when a trusted caller
explicitly needs the bearer token, such as when saving a session.

You can also provide a session file created by `monarch-api2`,
`monarch-cli2`, or another trusted tool. The MCP server loads the configured
session file for authenticated tools.

## MCP Inspector

You can inspect the server with MCP Inspector:

```bash
npx @modelcontextprotocol/inspector /absolute/path/to/monarch-mcp
```

If Inspector asks for transport details, use stdio with:

```json
{
  "command": "/absolute/path/to/monarch-mcp",
  "args": [],
  "env": {
    "MONARCH_SESSION_PATH": "/absolute/path/to/session.json"
  }
}
```

## Tools

Tool names mirror `monarch-api2` function names:

```text
auth_create_session
accounts_list_accounts
transactions_list_transactions
transactions_get_transaction
receipts_list_receipts
cashflow_get_cashflow_summary
reports_get_report_data
merchants_list_merchants
tags_list_tags
household_get_current_user
categories_list_categories
recurring_list_recurring_streams
investments_get_portfolio
goals_list_goals
budget_get_budget
```

The full server currently exposes 125 tools across all implemented API groups.
Use an MCP client or MCP Inspector to browse the complete tool list and schemas.

## Output

By default, tools return compact `summary` output. This is intended for agent
workflows where the caller usually needs the same fundamental fields a person
would scan in the CLI.

All tools accept common output controls:

- `output_mode="summary"` returns compact CLI-style output.
- `output_mode="full"` returns complete structured API output without `raw`.
- `output_mode="raw"` returns complete structured API output including `raw`.
- `fields=[...]` returns only selected dotted-path fields.

Examples:

```json
{
  "limit": 10
}
```

```json
{
  "limit": 10,
  "output_mode": "full"
}
```

```json
{
  "transaction_id": "TRANSACTION_ID",
  "output_mode": "raw"
}
```

```json
{
  "limit": 10,
  "output_mode": "raw",
  "fields": ["id", "date", "merchant.name", "category.name", "raw"]
}
```

When `fields` is provided, it is applied to the selected full/raw data and the
tool returns the projected object directly.

## Transaction Review Skill

This repo includes a Codex skill at:

```text
skills/monarch-transaction-review
```

The skill helps agents prepare unreviewed Monarch transactions without marking
them reviewed. It uses workflow tags such as `AI Review Ready` and keeps private
learned preferences in:

```text
~/.config/monarch/transaction-review-memory.md
```

Install or reference the skill from your Codex skills directory when you want
agents to use the transaction review workflow automatically.

## Development

Run the test suite:

```bash
.venv/bin/python -m pytest
```

The MCP source lives in `src/monarch_mcp`. Group-specific tools live in
`src/monarch_mcp/groups`.

## Security

This is an unofficial tool that can access sensitive personal finance data.
Treat saved session files like passwords.

- Do not commit session files, tokens, downloaded receipts, or personal finance
  exports.
- Use `output_mode="raw"` carefully, since raw payloads may include large or
  sensitive response data.
- Only connect this server to trusted MCP clients.
- Report security-sensitive issues privately instead of opening a public issue
  with credentials or personal financial data.

## License

MIT License. See [LICENSE](LICENSE).
