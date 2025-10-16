# Quick Start (60 seconds)

## Setup

```bash
chmod +x setup-uv.sh
./setup-uv.sh setup
./setup-uv.sh dev
```

## Register & Login

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","email":"admin@helpvia.com","password":"SecurePass123!","full_name":"Admin"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=admin&password=SecurePass123!"
```

## Create Ticket

```bash
curl -X POST http://localhost:8000/api/v1/tickets/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"summary":"Test ticket","priority":"high"}'
```

## Documentation

Visit http://localhost:8000/docs for interactive API docs!
