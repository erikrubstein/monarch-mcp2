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
        "tags_list_tags",
        "tags_get_tag",
        "tags_create_tag",
        "tags_update_tag",
        "tags_delete_tag",
        "tags_reorder_tag",
        "categories_list_categories",
        "categories_list_category_groups",
        "categories_get_category_catalog",
        "categories_get_category_group",
        "categories_get_category",
        "categories_create_category",
        "categories_update_category",
        "categories_remove_category",
        "categories_reactivate_category",
        "categories_reorder_category",
        "categories_create_category_group",
        "categories_update_category_group",
        "categories_delete_category_group",
        "categories_reorder_category_group",
        "cashflow_get_cashflow_summary",
        "cashflow_get_cashflow_trends",
        "cashflow_get_cashflow_breakdown",
    }
    assert {str(resource.uri) for resource in resources} == set()
