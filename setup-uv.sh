#!/usr/bin/env zsh
# HelpVia API Setup Script - Fixed Version
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo "${BLUE}ℹ ${1}${NC}"; }
print_success() { echo "${GREEN}✓ ${1}${NC}"; }
print_warning() { echo "${YELLOW}⚠ ${1}${NC}"; }
print_error() { echo "${RED}✗ ${1}${NC}"; }
print_header() {
    echo ""
    echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo "${BLUE}  ${1}${NC}"
    echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

check_uv() {
    if ! command -v uv &> /dev/null; then
        print_warning "UV is not installed"
        return 1
    fi
    print_success "UV is installed"
    return 0
}

install_uv() {
    print_header "Installing UV"
    if check_uv; then
        print_info "UV is already installed"
        return 0
    fi
    print_info "Installing UV via curl..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    if check_uv; then
        print_success "UV installed successfully!"
    else
        print_error "Failed to install UV"
        exit 1
    fi
}

create_venv() {
    print_header "Creating Virtual Environment"
    if [ -d ".venv" ]; then
        print_info "Virtual environment already exists"
    else
        print_info "Creating virtual environment..."
        uv venv
        print_success "Virtual environment created"
    fi
}

install_deps() {
    print_header "Installing Dependencies"
    
    print_info "Installing build tools..."
    uv pip install setuptools wheel
    
    print_info "Installing core dependencies..."
    # Install without editable mode first
    uv pip install .
    
    print_info "Installing dev dependencies..."
    uv pip install pytest pytest-cov pytest-asyncio httpx black ruff mypy
    
    print_success "Dependencies installed!"
}

install_deps_editable() {
    print_header "Installing Dependencies (Editable Mode)"
    
    print_info "Installing build tools..."
    uv pip install setuptools wheel
    
    print_info "Installing project in editable mode..."
    uv pip install -e ".[dev]"
    
    print_success "Dependencies installed!"
}

create_env() {
    print_header "Creating Environment File"
    if [ -f ".env" ]; then
        print_info ".env file already exists"
    else
        if [ -f ".env.template" ]; then
            print_info "Copying .env.template to .env..."
            cp .env.template .env
            print_success ".env file created!"
            print_warning "Remember to update .env with your actual values!"
        else
            print_error ".env.template not found!"
        fi
    fi
}

create_db() {
    print_header "Creating Database Tables"
    print_info "Running database migrations..."
    uv run python -c "
from app.core.database import engine, Base
import asyncio

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

try:
    asyncio.run(create_tables())
    print('✓ Database tables created!')
except Exception as e:
    print(f'✗ Error creating database: {e}')
    exit(1)
"
}

full_setup() {
    print_header "🚀 HelpVia API Setup"
    
    install_uv
    create_venv
    
    # Try editable mode first, fall back to regular install
    print_info "Attempting editable install..."
    if ! install_deps_editable 2>/dev/null; then
        print_warning "Editable install failed, using regular install..."
        install_deps
    fi
    
    create_env
    create_db
    
    print_header "✨ Setup Complete!"
    print_success "HelpVia API is ready to use!"
    print_info "Run './setup-uv.sh dev' to start the development server"
}

run_dev() {
    print_header "Starting Development Server"
    print_info "Starting server at http://localhost:8000"
    print_info "API docs at http://localhost:8000/docs"
    echo ""
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

run_tests() {
    print_header "Running Tests"
    print_info "Running pytest..."
    uv run pytest "$@"
}

run_tests_cov() {
    print_header "Running Tests with Coverage"
    print_info "Running pytest with coverage..."
    uv run pytest --cov=app --cov-report=html --cov-report=term "$@"
    print_success "Coverage report generated in htmlcov/"
}

format_code() {
    print_header "Formatting Code"
    print_info "Running black..."
    uv run black app tests
    print_success "Code formatted!"
}

lint_code() {
    print_header "Linting Code"
    print_info "Running ruff..."
    uv run ruff check app tests
    print_success "Linting complete!"
}

type_check() {
    print_header "Type Checking"
    print_info "Running mypy..."
    uv run mypy app
    print_success "Type checking complete!"
}

clean() {
    print_header "Cleaning Build Artifacts"
    print_info "Removing build directories..."
    rm -rf build/ dist/ *.egg-info htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    print_success "Cleaned!"
}

reset_db() {
    print_header "⚠️  Resetting Database"
    print_warning "This will delete all data!"
    read "?Are you sure? (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Removing database..."
        rm -f helpvia.db helpvia_test.db
        print_info "Recreating tables..."
        create_db
        print_success "Database reset complete!"
    else
        print_info "Cancelled"
    fi
}

show_help() {
    cat << EOF
${BLUE}HelpVia API - UV Setup Script${NC}

${GREEN}Usage:${NC}
  ./setup-uv.sh [command]

${GREEN}Commands:${NC}
  setup           Complete setup (install UV, create venv, install deps, create db)
  dev             Start development server
  test            Run tests
  test-cov        Run tests with coverage report
  format          Format code with black
  lint            Lint code with ruff
  typecheck       Type check with mypy
  clean           Remove build artifacts
  db-create       Create database tables
  db-reset        Reset database (WARNING: deletes all data)
  reinstall       Reinstall all dependencies
  help            Show this help message

${GREEN}Examples:${NC}
  ./setup-uv.sh setup      # First time setup
  ./setup-uv.sh dev        # Start server
  ./setup-uv.sh test       # Run tests

EOF
}

reinstall() {
    print_header "Reinstalling Dependencies"
    print_info "Removing virtual environment..."
    rm -rf .venv
    create_venv
    install_deps
    print_success "Dependencies reinstalled!"
}

case "${1:-help}" in
    setup)
        full_setup
        ;;
    dev)
        run_dev
        ;;
    test)
        shift
        run_tests "$@"
        ;;
    test-cov)
        shift
        run_tests_cov "$@"
        ;;
    format)
        format_code
        ;;
    lint)
        lint_code
        ;;
    typecheck)
        type_check
        ;;
    clean)
        clean
        ;;
    db-create)
        create_db
        ;;
    db-reset)
        reset_db
        ;;
    reinstall)
        reinstall
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac