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
        "merchants_list_merchants",
        "merchants_get_merchant",
        "merchants_update_merchant",
        "merchants_delete_merchant",
        "household_get_current_user",
        "household_get_household",
        "household_get_household_member",
        "household_get_household_preferences",
        "household_list_household_members",
        "household_update_current_user",
        "household_update_household_preferences",
        "recurring_list_recurring_streams",
        "recurring_get_recurring_stream",
        "recurring_list_recurring_occurrences",
        "recurring_get_recurring_summary",
        "recurring_create_recurring_stream",
        "recurring_update_recurring_stream",
        "recurring_remove_recurring_stream",
        "investments_list_investment_accounts",
        "investments_list_holdings",
        "investments_get_holding",
        "investments_get_holding_performance",
        "investments_get_portfolio",
        "investments_get_security",
        "investments_search_securities",
        "investments_create_manual_holding",
        "investments_update_manual_holding",
        "investments_delete_manual_holding",
        "reports_get_report_data",
        "reports_list_saved_reports",
        "reports_get_saved_report",
        "reports_create_saved_report",
        "reports_update_saved_report",
        "reports_delete_saved_report",
    }
    assert {str(resource.uri) for resource in resources} == set()
