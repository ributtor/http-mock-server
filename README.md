# http-mock-server

Lightweight mock server for API testing with record/replay support.

## Features
- Define mock responses in JSON/YAML
- Record real API calls for replay
- Latency simulation
- Request logging and assertions
- Proxy mode with recording

## Usage
```bash
# Start mock server
mock-server start --config mocks.json --port 8080

# Record mode
mock-server record --target https://api.example.com --port 8080
```

## Config Example
```json
{
  "routes": [
    {
      "method": "GET",
      "path": "/api/users",
      "status": 200,
      "body": [{"id": 1, "name": "Alice"}]
    }
  ]
}
```

## License
MIT
