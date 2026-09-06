# Smartsheet Connector — Preparation & Architecture

**Service**: Smartsheet  
**Target API**: Smartsheet REST API v2.0  
**Endpoint**: `https://api.smartsheet.com/2.0`  
**Auth Endpoint**: `https://app.smartsheet.com/b/authorize` & `https://api.smartsheet.com/2.0/token`  
**Official Docs**: `https://developers.smartsheet.com/api-docs/`

---

## 1. Executive Summary & Market Position
Smartsheet — лидирующая в мире корпоративная Work Execution платформа (~10% CWM рынка).
Коннектор Imperal Cloud предоставляет:
- Подключение по Personal API Access Token (Bearer) и OAuth 2.0;
- Просмотр и управление рабочими пространствами (Workspaces);
- Управление таблицами (Sheets): создание, чтение структуры, удаление;
- Манипуляции со строками (Rows): пакетное добавление, обновление ячеек, удаление строк;
- Регистрацию вебхуков на изменения в таблицах;
- Value-add аудит здоровья структуры таблиц и строк.

---

## 2. Ключевые архитектурные особенности API
1. **Sheet-scoped row operations**: Все операции со строками (`POST /sheets/{sheetId}/rows`, `PUT /sheets/{sheetId}/rows`, `DELETE /sheets/{sheetId}/rows?ids=...`) требуют ID таблицы.
2. **Column ID & Cell Value**: Обновление ячеек требует знания `columnId`.
3. **Webhooks Validation**: При создании вебхука Smartsheet ожидает верификацию через callback или API verification.
4. **Rate Limits**: До 300 запросов в минуту на пользователя.
