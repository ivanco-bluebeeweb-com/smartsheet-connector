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
                "1. Sign in to your Smartsheet account.\n"
                "2. Go to Account > Personal Settings > API Access.\n"
                "3. Click 'Generate new access token' and copy the token.\n"
                "4. Paste it in the form below and click Connect.",
                variant="body"
            )
        ]
    )

@ext.panel("smartsheet_sidebar", slot="left")
async def smartsheet_sidebar(ctx, **kwargs) -> ui.UINode:
    conns = await h._load_connections(ctx)
    if not conns:
        return ui.Stack(
            direction="v",
            gap=3,
            children=[
                ui.Stack(
                    direction="h",
                    gap=2,
                    children=[
                        ui.Text("Smartsheet", variant="heading"),
                        _settings_button()
                    ]
                ),
                ui.Divider(),
                _help_modal(),
                ui.Form(
                    id="connect_smartsheet_form",
                    action=ui.Call("connect_smartsheet"),
                    children=[
                        ui.Input("label", label="Connection Label", placeholder="e.g. Operations Smartsheet"),
                        ui.Input("access_token", label="API Access Token", type="password", placeholder="Enter Smartsheet token", required=True),
                        ui.Button("Connect Smartsheet", variant="primary", type="submit")
                    ]
                )
            ]
        )
    return ui.Stack(
        direction="v",
        gap=3,
        children=[
            ui.Stack(
                direction="h",
                gap=2,
                children=[
                    ui.Text("Smartsheet Connected", variant="heading"),
                    _settings_button()
                ]
            ),
            ui.Divider(),
            ui.Text(f"Active Account: {conns[0].get('label')}"),
            ui.Button(
                "Audit Health",
                variant="secondary",
                size="sm",
                on_click=ui.Call("audit_smartsheet_health")
            )
        ]
    )
