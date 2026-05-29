from __future__ import annotations

import pytest

from monarch_mcp.server import create_mcp


@pytest.mark.anyio
async def test_server_registers_auth_group() -> None:
    mcp = create_mcp()

    tools = await mcp.list_tools()
    resources = await mcp.list_resources()

    assert {tool.name for tool in tools} == {
        "auth_create_session",
        "auth_save_session",
        "auth_load_session",
        "accounts_list_accounts",
        "accounts_get_account",
        "accounts_get_net_worth_performance",
        "accounts_get_net_worth_breakdown",
        "accounts_get_historical_balances",
        "accounts_get_account_history",
        "accounts_create_manual_account",
        "accounts_update_account",
        "accounts_delete_account",
    }
    assert {str(resource.uri) for resource in resources} == set()
