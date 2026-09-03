"""Pydantic schemas for Smartsheet Connector (Smartsheet API 2.0)."""
from __future__ import annotations
from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameter model."""
    pass

class ConnectSmartsheetParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Operations Smartsheet.")
    access_token: str = Field(..., description="Smartsheet generated API access token (Bearer).")

class DisconnectSmartsheetParams(BaseModel):
    connection_id: str = Field(..., description="Connection ID to remove.")

class ListSheetsParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    include_all: bool = Field(default=True, description="Whether to include all sheets without paging.")

class GetSheetParams(BaseModel):
    sheet_id: str = Field(..., description="Smartsheet sheet ID.")
    connection_id: str = Field(default="", description="Optional connection ID.")

class CreateSheetParams(BaseModel):
    name: str = Field(..., description="Sheet name.")
    columns: List[Dict[str, Any]] = Field(..., description="List of columns definitions (title, type: TEXT_NUMBER, DATE, CHECKBOX, etc.).")
    connection_id: str = Field(default="", description="Optional connection ID.")

class DeleteSheetParams(BaseModel):
    sheet_id: str = Field(..., description="Smartsheet sheet ID to delete.")
    connection_id: str = Field(default="", description="Optional connection ID.")

class AddRowsParams(BaseModel):
    sheet_id: str = Field(..., description="Target sheet ID.")
    rows: List[Dict[str, Any]] = Field(..., description="List of rows to add. Each row contains 'cells': [{'columnId': ..., 'value': ...}].")
    connection_id: str = Field(default="", description="Optional connection ID.")

class UpdateRowsParams(BaseModel):
    sheet_id: str = Field(..., description="Target sheet ID.")
    rows: List[Dict[str, Any]] = Field(..., description="List of rows to update with their row ID and cell updates.")
    connection_id: str = Field(default="", description="Optional connection ID.")

class DeleteRowsParams(BaseModel):
    sheet_id: str = Field(..., description="Target sheet ID.")
    row_ids: List[int] = Field(..., description="List of numeric row IDs to delete.")
    connection_id: str = Field(default="", description="Optional connection ID.")

class ListWorkspacesParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")

class GetWorkspaceParams(BaseModel):
    workspace_id: str = Field(..., description="Workspace ID.")
    connection_id: str = Field(default="", description="Optional connection ID.")

class CreateWebhookParams(BaseModel):
    name: str = Field(..., description="Webhook name.")
    callback_url: str = Field(..., description="HTTPS callback URL.")
    scope: str = Field(default="sheet", description="Scope: sheet or workspace.")
    scope_object_id: int = Field(..., description="Target sheet or workspace ID.")
    events: List[str] = Field(default_factory=lambda: ["*.*"], description="Events to subscribe to, e.g. ['*.*'].")
    connection_id: str = Field(default="", description="Optional connection ID.")

class AuditHealthParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")

# Return models
class SmartsheetConnection(BaseModel):
    id: str = Field(..., description="Connection ID")
    label: str = Field(..., description="Connection label")
    status: str = Field(default="connected", description="Connection status")

class ConnectionList(BaseModel):
    connections: List[SmartsheetConnection] = Field(default_factory=list)
    count: int = Field(default=0)

class ConnectResult(BaseModel):
    id: str = Field(..., description="Connection ID")
    label: str = Field(..., description="Connection label")
    status: str = Field(default="connected", description="Status")

class DisconnectResult(BaseModel):
    success: bool = Field(default=True)
    message: str = Field(...)

class GenericListResult(BaseModel):
    items: List[Dict[str, Any]] = Field(default_factory=list)
    count: int = Field(default=0)

class GenericRecordResult(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)
    id: Optional[str] = None

class DeleteResult(BaseModel):
    success: bool = Field(default=True)
    message: str = Field(...)

class HealthAuditResult(BaseModel):
    status: str = Field(..., description="Audit status: healthy, degraded, or error")
    user: str = Field(default="Unknown", description="User or organization")
    sheets_count: int = Field(default=0, description="Accessible sheets count")
    summary: str = Field(..., description="Human-readable summary")
