# API Reference

Base URL: `http://localhost:5000`

## Endpoints

### `GET /health`

Returns the application health status.

**Response 200**
```json
{ "status": "ok" }
```

---

### `POST /login`

Authenticate a user.

**Request body**
```json
{ "username": "string", "password": "string" }
```

**Response 200**
```json
{ "message": "Login successful" }
```

**Response 400** — missing or invalid fields
```json
{ "error": "Invalid input" }
```

**Response 500** — unexpected server error
```json
{ "error": "Internal Server Error" }
```

---

### `POST /data`

Submit data for processing.

**Request body**
```json
{ "input": "any string" }
```

**Response 200**
```json
{ "message": "Data received successfully" }
```

**Response 400** — missing `input` field
```json
{ "error": "Invalid input" }
```

## Authentication

Set the `API_KEY` environment variable.  
Clients must include the key in the `X-API-Key` header (future enhancement).
