# ShopSherpa

A minimal FastAPI service with health check endpoint.

## Quickstart

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ShopSherpa
```

2. Install dependencies:
```bash
make install
```

3. Copy environment file:
```bash
cp .env.example .env
```

4. Run the development server:
```bash
make dev
```

The API will be available at `http://localhost:8000`

### API Documentation

- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

### Available Endpoints

- `GET /healthz` - Health check endpoint returning `{"status": "ok"}`

### Development

#### Running Tests
```bash
make test
```

#### Linting and Formatting
```bash
make lint    # Check code style
make fmt     # Format code
```

#### Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install
```

### Project Structure

```
ShopSherpa/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── api/
│   │   ├── __init__.py
│   │   └── health.py        # Health endpoint
│   └── core/
│       ├── __init__.py
│       └── config.py        # Configuration
├── tests/
│   ├── __init__.py
│   └── test_health.py       # Health endpoint tests
├── pyproject.toml           # Dependencies and config
├── Makefile                 # Development commands
├── .ruff.toml              # Ruff configuration
├── .pre-commit-config.yaml # Pre-commit hooks
├── .env.example            # Environment variables template
└── README.md               # This file
```
