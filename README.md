# monarch-mcp2

Unofficial MCP server for Monarch Money.

This project is not affiliated with, endorsed by, or supported by Monarch Money.

`monarch-mcp2` exposes the public function surface from
[`monarch-api2`](https://github.com/erikrubstein/monarch-api2) as Model Context
Protocol tools for AI agents. Tools are organized by Monarch feature area and
map 1-to-1 to backend API functions:

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

Install from GitHub:

```bash
pipx install git+https://github.com/erikrubstein/monarch-mcp2.git
```

Or install from a local checkout:

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
```

For local sibling development against an editable `monarch-api2` checkout:

```bash
.venv/bin/pip install -e ../monarch-api2
```

After installation, the `monarch-mcp` command should be available:

```bash
monarch-mcp
```

## Usage

Run the MCP server over stdio:

```bash
monarch-mcp
```

The default session file is:

```text
~/.config/monarch/session.json
```

You can override it with `MONARCH_SESSION_PATH`, or set `MONARCH_CONFIG_DIR` to
change the config directory.

Example MCP client configuration:

```json
{
  "mcpServers": {
    "monarch": {
      "command": "/absolute/path/to/monarch-mcp2/.venv/bin/monarch-mcp",
      "env": {
        "MONARCH_SESSION_PATH": "/absolute/path/to/session.json"
      }
    }
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

## Authentication

Use `auth_create_session` to create a Monarch session. Auth tools redact the
session token by default. Set `include_token=true` only when a trusted caller
explicitly needs the bearer token, such as when saving a session.

You can also provide a session file created by `monarch-api2`,
`monarch-cli2`, or another trusted tool. The MCP server loads the configured
session file for authenticated tools.

## Development

Run the test suite:

```bash
.venv/bin/python -m pytest
```

Run the server from a local checkout:

```bash
.venv/bin/monarch-mcp
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
