# Smartsheet Connector — Discovery & Feature Matrix

## 1. Classification of Capabilities

| Capability | Inbound (Imperal -> Smartsheet) | Outbound (Smartsheet -> Imperal) | Coverage |
| :--- | :---: | :---: | :---: |
| Sheets | Write (Create, Delete) | Read (List, Get) | Both |
| Rows & Cells | Write (Add Rows, Update Rows, Delete Rows) | Read (Included in Get Sheet) | Both |
| Workspaces | - | Read (List, Get) | Read-only |
| Webhooks | Write (Create) | Receive (Events) | Both |
| Health Audit | Analytical (Inspect Sheets, Rows, Token) | - | Internal |

---

## 2. Feature Tiers

### Tier 1 — Core Essentials
- `connect_smartsheet`: Сохранение Access Token с проверкой прав через `GET /users/me`.
- `list_sheets`: Список таблиц пользователя.
- `get_sheet`: Полная структура таблицы (колонки и строки).
- `create_sheet`: Создание новой таблицы с заданными колонками.
- `delete_sheet`: Удаление таблицы.
- `add_rows`: Пакетное добавление строк в таблицу.
- `update_rows`: Обновление ячеек существующих строк.
- `delete_rows`: Удаление строк по их ID.

### Tier 2 — Extended Capabilities
- `list_workspaces`: Список рабочих пространств.
- `get_workspace`: Детали рабочего пространства.
- `create_webhook`: Регистрация подписки на события таблицы.
- `audit_smartsheet_health`: Value-add аудит доступности таблиц и прав доступа.
