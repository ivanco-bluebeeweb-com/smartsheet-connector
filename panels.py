"""Panel UI for Smartsheet Connector."""
from __future__ import annotations
from imperal_sdk import ui
from app import ext
import handlers_connection as h

def _settings_button() -> ui.UINode:
    return ui.Button(
        "App settings",
        variant="secondary",
        size="sm",
        icon="settings",
        on_click=ui.Call("__smartsheet_settings")
    )

def _help_modal() -> ui.UINode:
    return ui.Modal(
        trigger=ui.Button("How do I set this up?", variant="ghost", size="sm"),
        title="Connecting Smartsheet",
        children=[
            ui.Text(
                "1. Sign in to Smartsheet, go to Account > Personal Settings > API Access.\n"
                "2. Generate a new API access token.\n"
                "3. Enter a label and paste the token below, then click Connect Smartsheet.",
                variant="body"
            )
        ]
    )

@ext.panel("smartsheet_sidebar", slot="left")
async def smartsheet_sidebar(ctx, **kwargs) -> ui.UINode:
    connections = await h._load_connections(ctx)
    conn_items = [
        ui.Text(c.get("label") or "Smartsheet Account", variant="body")
        for c in connections
    ] if connections else [ui.Text("No Smartsheet accounts connected yet.", variant="caption")]

    return ui.Stack(
        direction="v",
        gap=3,
        children=[
            ui.Text("Smartsheet", variant="heading"),
            ui.Stack(direction="v", gap=1, children=conn_items),
            ui.Divider(),
            ui.Form(
                submit_label="Connect Smartsheet",
                action=ui.Call("connect_smartsheet"),
                children=[
                    ui.Stack(
                        direction="v",
                        gap=2,
                        children=[
                            ui.Stack(
                                direction="v",
                                gap=1,
                                children=[
                                    ui.Text("Connection Label", variant="label"),
                                    ui.Input(
                                        param_name="label",
                                        placeholder="e.g. Operations Smartsheet"
                                    ),
                                ]
                            ),
                            ui.Stack(
                                direction="v",
                                gap=1,
                                children=[
                                    ui.Text("API Access Token", variant="label"),
                                    ui.Input(
                                        param_name="access_token",
                                        placeholder="Enter Smartsheet API token"
                                    ),
                                ]
                            ),
                        ]
                    )
                ]
            ),
            _help_modal(),
            ui.Spacer(),
            _settings_button(),
        ]
    )
