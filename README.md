# HelpVia API

Production-ready ticketing system API built with FastAPI, SQLAlchemy, and UV.

## Quick Start

```bash
chmod +x setup-uv.sh
./setup-uv.sh setup
./setup-uv.sh dev
```

Visit http://localhost:8000/docs

## Features

- FastAPI with async/await
- JWT authentication
- SQLite/MySQL support
- Complete test coverage
- UV for fast dependency management
- Docker support

## Commands

```bash
./setup-uv.sh dev       # Start server
./setup-uv.sh test      # Run tests
./setup-uv.sh format    # Format code
./setup-uv.sh lint      # Lint code
```

## API Endpoints

### Authentication
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me

### Tickets
- GET /api/v1/tickets/
- GET /api/v1/tickets/open
- GET /api/v1/tickets/{id}
- POST /api/v1/tickets/
- PUT /api/v1/tickets/{id}
- POST /api/v1/tickets/{id}/actions
- DELETE /api/v1/tickets/{id}

## Configuration

Copy `.env.template` to `.env` and update:

```bash
SECRET_KEY=your-secret-key  # Use: openssl rand -hex 32
DATABASE_TYPE=sqlite        # or mysql
```

## Docker

```bash
docker-compose up -d
```

## Built by

David Crosby (Bing)

Built with ❤️ using FastAPI and UV
