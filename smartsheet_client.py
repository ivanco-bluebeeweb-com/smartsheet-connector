"""Smartsheet REST API 2.0 client implementation."""
from __future__ import annotations
import httpx
from typing import Any, Dict, List, Optional

class SmartsheetClient:
    def __init__(self, access_token: str):
        self.base_url = "https://api.smartsheet.com/2.0"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    async def get_current_user(self) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.base_url}/users/me", headers=self.headers, timeout=15.0)
            res.raise_for_status()
            return res.json()

    async def list_sheets(self, include_all: bool = True) -> List[Dict[str, Any]]:
        params = {"includeAll": "true" if include_all else "false"}
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.base_url}/sheets", headers=self.headers, params=params, timeout=15.0)
            res.raise_for_status()
            return res.json().get("data", [])

    async def get_sheet(self, sheet_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.base_url}/sheets/{sheet_id}", headers=self.headers, timeout=15.0)
            res.raise_for_status()
            return res.json()

    async def create_sheet(self, name: str, columns: List[Dict[str, Any]]) -> Dict[str, Any]:
        payload = {"name": name, "columns": columns}
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{self.base_url}/sheets", headers=self.headers, json=payload, timeout=15.0)
            res.raise_for_status()
            return res.json().get("result", {})

    async def delete_sheet(self, sheet_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            res = await client.delete(f"{self.base_url}/sheets/{sheet_id}", headers=self.headers, timeout=15.0)
            res.raise_for_status()
            return res.json()

    async def add_rows(self, sheet_id: str, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{self.base_url}/sheets/{sheet_id}/rows", headers=self.headers, json=rows, timeout=15.0)
            res.raise_for_status()
            return res.json().get("result", [])

    async def update_rows(self, sheet_id: str, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            res = await client.put(f"{self.base_url}/sheets/{sheet_id}/rows", headers=self.headers, json=rows, timeout=15.0)
            res.raise_for_status()
            return res.json().get("result", [])

    async def delete_rows(self, sheet_id: str, row_ids: List[int]) -> Dict[str, Any]:
        params = {"ids": ",".join(map(str, row_ids))}
        async with httpx.AsyncClient() as client:
            res = await client.delete(f"{self.base_url}/sheets/{sheet_id}/rows", headers=self.headers, params=params, timeout=15.0)
            res.raise_for_status()
            return res.json()

    async def list_workspaces(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.base_url}/workspaces", headers=self.headers, timeout=15.0)
            res.raise_for_status()
            return res.json().get("data", [])

    async def get_workspace(self, workspace_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.base_url}/workspaces/{workspace_id}", headers=self.headers, timeout=15.0)
            res.raise_for_status()
            return res.json()

    async def create_webhook(self, name: str, callback_url: str, scope: str, scope_object_id: int, events: List[str]) -> Dict[str, Any]:
        payload = {
            "name": name,
            "callbackUrl": callback_url,
            "scope": scope,
            "scopeObjectId": scope_object_id,
            "events": events,
            "version": 1
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{self.base_url}/webhooks", headers=self.headers, json=payload, timeout=15.0)
            res.raise_for_status()
            return res.json().get("result", {})
