# Smartsheet Connector — Authentication & Credentials Standard

## 1. Supported Authentication Mechanisms
1. **Personal Access Token (PAT)**:
   - Генерируется в Smartsheet: Account -> Personal Settings -> API Access.
   - Передается в заголовке `Authorization: Bearer <access_token>`.
2. **OAuth 2.0 Web Flow**:
   - Авторизация через `https://app.smartsheet.com/b/authorize`.
   - Обмен кода на токен через `POST https://api.smartsheet.com/2.0/token`.
3. **Client Credentials / M2M**:
   - Серверная интеграция через Client ID и Client Secret.

## 2. Token Storage & Security
- Токены хранятся строго в `ctx.secrets` под ключом `smartsheet_connections`.
- Маскируются в UI (`_mask()`).
