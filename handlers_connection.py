"""Connection lifecycle handlers for Smartsheet Connector."""
from __future__ import annotations
import json, uuid
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ConnectSmartsheetParams, DisconnectSmartsheetParams, NoParams,
    ConnectionList, SmartsheetConnection, ConnectResult, DisconnectResult
)
from smartsheet_client import SmartsheetClient

SECRET_KEY = "smartsheet_connections"

async def _load_connections(ctx) -> list[dict]:
    raw = await ctx.secrets.get(SECRET_KEY)
    if not raw:
        return []
    try:
        return json.loads(raw)
    except Exception:
        return []

async def _save_connections(ctx, connections: list[dict]) -> None:
    await ctx.secrets.set(SECRET_KEY, json.dumps(connections))

async def resolve_client(ctx, connection_id: str = "") -> SmartsheetClient:
    connections = await _load_connections(ctx)
    if not connections:
        raise ValueError("No Smartsheet connections found. Please connect an account first.")
    if connection_id:
        for c in connections:
            if c.get("id") == connection_id:
                return SmartsheetClient(access_token=c["access_token"])
        raise ValueError(f"Connection ID {connection_id} not found.")
    c = connections[0]
    return SmartsheetClient(access_token=c["access_token"])

@chat.function(
    "connect_smartsheet",
    "Connect your own Smartsheet account by saving your API Access Token.",
    action_type="write",
    chain_callable=True,
    event="smartsheet-connector.connect_smartsheet",
    effects=["create:connection"],
    data_model=ConnectResult
)
async def connect_smartsheet(ctx, params: ConnectSmartsheetParams) -> ActionResult:
    """Connect a Smartsheet account after verifying access token."""
    client = SmartsheetClient(access_token=params.access_token)
    try:
        user_info = await client.get_current_user()
    except Exception as e:
        return ActionResult.error(f"Failed to authenticate with Smartsheet: {e}")

    email = user_info.get("email", "unknown")
    conn_id = f"conn_{uuid.uuid4().hex[:8]}"
    label = params.label or f"Smartsheet ({email})"

    conns = await _load_connections(ctx)
    conns.append({
        "id": conn_id,
        "label": label,
        "email": email,
        "access_token": params.access_token
    })
    await _save_connections(ctx, conns)
    return ActionResult.ok(
        {"id": conn_id, "label": label, "status": "connected"},
        summary=f"Successfully connected Smartsheet account '{label}'."
    )

@chat.function(
    "list_connections",
    "List connected Smartsheet accounts without exposing credentials.",
    action_type="read",
    chain_callable=True,
    data_model=ConnectionList
)
async def list_connections(ctx, params: NoParams) -> ActionResult:
    """List all connected Smartsheet accounts."""
    conns = await _load_connections(ctx)
    items = [
        {"id": c.get("id"), "label": c.get("label", "Smartsheet"), "status": "connected"}
        for c in conns
    ]
    return ActionResult.ok(
        {"connections": items, "count": len(items)},
        summary=f"Found {len(items)} Smartsheet connection(s)."
    )

@chat.function(
    "disconnect_smartsheet",
    "Disconnect a Smartsheet account.",
    action_type="write",
    chain_callable=True,
    event="smartsheet-connector.disconnect_smartsheet",
    effects=["delete:connection"],
    data_model=DisconnectResult
)
async def disconnect_smartsheet(ctx, params: DisconnectSmartsheetParams) -> ActionResult:
    """Disconnect and remove a saved Smartsheet account."""
    conns = await _load_connections(ctx)
    updated = [c for c in conns if c.get("id") != params.connection_id]
    if len(updated) == len(conns):
        return ActionResult.error(f"Connection {params.connection_id} not found.")
    await _save_connections(ctx, updated)
    return ActionResult.ok(
        {"success": True, "message": f"Connection {params.connection_id} removed."},
        summary=f"Disconnected Smartsheet connection {params.connection_id}."
    )
