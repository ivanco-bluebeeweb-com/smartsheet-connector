"""Resource handlers for Smartsheet Connector."""
from __future__ import annotations
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from handlers_connection import resolve_client
from schemas import (
    ListSheetsParams, GetSheetParams, CreateSheetParams, DeleteSheetParams,
    AddRowsParams, UpdateRowsParams, DeleteRowsParams, ListWorkspacesParams,
    GetWorkspaceParams, CreateWebhookParams, AuditHealthParams,
    GenericListResult, GenericRecordResult, DeleteResult, HealthAuditResult
)

@chat.function(
    "audit_smartsheet_health",
    "Audit Smartsheet connectivity, user identity, and accessible sheets.",
    action_type="read",
    chain_callable=True,
    data_model=HealthAuditResult
)
async def audit_smartsheet_health(ctx, params: AuditHealthParams) -> ActionResult:
    """Audit Smartsheet account health."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        user = await client.get_current_user()
        sheets = await client.list_sheets()
        return ActionResult.success(
            {
                "status": "healthy",
                "user": user.get("email", "Unknown"),
                "sheets_count": len(sheets),
                "summary": f"Smartsheet connection is healthy. Accessible sheets: {len(sheets)}."
            },
            summary="Smartsheet health check passed."
        )
    except Exception as e:
        return ActionResult.error(f"Smartsheet health audit failed: {e}")

@chat.function(
    "list_sheets",
    "List sheets in the connected Smartsheet account.",
    action_type="read",
    chain_callable=True,
    data_model=GenericListResult
)
async def list_sheets(ctx, params: ListSheetsParams) -> ActionResult:
    """List sheets in Smartsheet."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        sheets = await client.list_sheets(include_all=params.include_all)
        return ActionResult.success({"items": sheets, "count": len(sheets)}, summary=f"Found {len(sheets)} sheet(s).")
    except Exception as e:
        return ActionResult.error(f"Error listing sheets: {e}")

@chat.function(
    "get_sheet",
    "Get details of a sheet by sheet ID.",
    action_type="read",
    chain_callable=True,
    data_model=GenericRecordResult
)
async def get_sheet(ctx, params: GetSheetParams) -> ActionResult:
    """Get a sheet's details and data."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        sheet = await client.get_sheet(sheet_id=params.sheet_id)
        return ActionResult.success({"data": sheet, "id": str(sheet.get("id"))}, summary=f"Retrieved sheet {params.sheet_id}.")
    except Exception as e:
        return ActionResult.error(f"Error getting sheet: {e}")

@chat.function(
    "create_sheet",
    "Create a new sheet with columns in Smartsheet.",
    action_type="write",
    chain_callable=True,
    event="smartsheet-connector.create_sheet",
    effects=["create:sheet"],
    data_model=GenericRecordResult
)
async def create_sheet(ctx, params: CreateSheetParams) -> ActionResult:
    """Create a new sheet."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        res = await client.create_sheet(name=params.name, columns=params.columns)
        return ActionResult.success({"data": res, "id": str(res.get("id"))}, summary=f"Created sheet '{params.name}'.")
    except Exception as e:
        return ActionResult.error(f"Error creating sheet: {e}")

@chat.function(
    "delete_sheet",
    "Delete a sheet from Smartsheet.",
    action_type="write",
    chain_callable=True,
    event="smartsheet-connector.delete_sheet",
    effects=["delete:sheet"],
    data_model=DeleteResult
)
async def delete_sheet(ctx, params: DeleteSheetParams) -> ActionResult:
    """Delete a sheet."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        await client.delete_sheet(sheet_id=params.sheet_id)
        return ActionResult.success({"success": True, "message": f"Sheet {params.sheet_id} deleted."}, summary=f"Deleted sheet {params.sheet_id}.")
    except Exception as e:
        return ActionResult.error(f"Error deleting sheet: {e}")

@chat.function(
    "add_rows",
    "Add one or more rows to a sheet.",
    action_type="write",
    chain_callable=True,
    event="smartsheet-connector.add_rows",
    effects=["create:row"],
    data_model=GenericListResult
)
async def add_rows(ctx, params: AddRowsParams) -> ActionResult:
    """Add rows to a Smartsheet sheet."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        rows = await client.add_rows(sheet_id=params.sheet_id, rows=params.rows)
        return ActionResult.success({"items": rows, "count": len(rows)}, summary=f"Added {len(rows)} row(s) to sheet {params.sheet_id}.")
    except Exception as e:
        return ActionResult.error(f"Error adding rows: {e}")

@chat.function(
    "update_rows",
    "Update existing rows in a sheet.",
    action_type="write",
    chain_callable=True,
    event="smartsheet-connector.update_rows",
    effects=["update:row"],
    data_model=GenericListResult
)
async def update_rows(ctx, params: UpdateRowsParams) -> ActionResult:
    """Update rows in a Smartsheet sheet."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        rows = await client.update_rows(sheet_id=params.sheet_id, rows=params.rows)
        return ActionResult.success({"items": rows, "count": len(rows)}, summary=f"Updated {len(rows)} row(s) in sheet {params.sheet_id}.")
    except Exception as e:
        return ActionResult.error(f"Error updating rows: {e}")

@chat.function(
    "delete_rows",
    "Delete rows from a sheet by row IDs.",
    action_type="write",
    chain_callable=True,
    event="smartsheet-connector.delete_rows",
    effects=["delete:row"],
    data_model=DeleteResult
)
async def delete_rows(ctx, params: DeleteRowsParams) -> ActionResult:
    """Delete rows from a sheet."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        await client.delete_rows(sheet_id=params.sheet_id, row_ids=params.row_ids)
        return ActionResult.success({"success": True, "message": f"Deleted {len(params.row_ids)} row(s)."}, summary=f"Deleted {len(params.row_ids)} row(s) from sheet {params.sheet_id}.")
    except Exception as e:
        return ActionResult.error(f"Error deleting rows: {e}")

@chat.function(
    "list_workspaces",
    "List workspaces in Smartsheet.",
    action_type="read",
    chain_callable=True,
    data_model=GenericListResult
)
async def list_workspaces(ctx, params: ListWorkspacesParams) -> ActionResult:
    """List workspaces."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        workspaces = await client.list_workspaces()
        return ActionResult.success({"items": workspaces, "count": len(workspaces)}, summary=f"Found {len(workspaces)} workspace(s).")
    except Exception as e:
        return ActionResult.error(f"Error listing workspaces: {e}")

@chat.function(
    "get_workspace",
    "Get details of a workspace by workspace ID.",
    action_type="read",
    chain_callable=True,
    data_model=GenericRecordResult
)
async def get_workspace(ctx, params: GetWorkspaceParams) -> ActionResult:
    """Get workspace details."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        ws = await client.get_workspace(workspace_id=params.workspace_id)
        return ActionResult.success({"data": ws, "id": str(ws.get("id"))}, summary=f"Retrieved workspace {params.workspace_id}.")
    except Exception as e:
        return ActionResult.error(f"Error getting workspace: {e}")

@chat.function(
    "create_webhook",
    "Create a webhook subscription in Smartsheet.",
    action_type="write",
    chain_callable=True,
    event="smartsheet-connector.create_webhook",
    effects=["create:webhook"],
    data_model=GenericRecordResult
)
async def create_webhook(ctx, params: CreateWebhookParams) -> ActionResult:
    """Create a webhook in Smartsheet."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        wh = await client.create_webhook(
            name=params.name,
            callback_url=params.callback_url,
            scope=params.scope,
            scope_object_id=params.scope_object_id,
            events=params.events
        )
        return ActionResult.success({"data": wh, "id": str(wh.get("id"))}, summary=f"Created webhook '{params.name}'.")
    except Exception as e:
        return ActionResult.error(f"Error creating webhook: {e}")
