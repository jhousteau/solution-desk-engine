.PHONY: help install dev test test-cov test-watch format lint typecheck security quality clean run build worktree-create worktree-list worktree-remove genesis-commit genesis-status genesis-clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	poetry install

dev: install ## Install with development dependencies
	poetry run pre-commit install

test: ## Run tests
	poetry run pytest

test-cov: ## Run tests with coverage
	poetry run pytest --cov --cov-report=html --cov-report=term

test-watch: ## Run tests in watch mode
	poetry run pytest-watch

format: ## Format code with black and isort
	poetry run black src/ tests/
	poetry run isort src/ tests/

lint: ## Lint code with flake8, ruff, and pylint
	poetry run flake8 src/ tests/
	poetry run ruff check src/ tests/
	poetry run pylint src/ tests/ --disable=all --enable=unused-import,unused-variable

typecheck: ## Type check with mypy
	poetry run mypy src/

security: ## Run security scans
	poetry run bandit -r src/ -c .bandit || true
	poetry run gitleaks detect --verbose --no-banner || true

quality: format lint typecheck security ## Run all quality checks

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

run: ## Run the development server
	poetry run uvicorn solution_desk_engine.main:app --reload

build: ## Build the package
	poetry build

# Genesis AI-Safe Development Targets
worktree-create: ## Create AI-safe worktree (usage: make worktree-create NAME=feature-name FOCUS=src/)
	@if [ -z "$(NAME)" ]; then echo "❌ Error: NAME is required. Usage: make worktree-create NAME=feature-name"; exit 1; fi
	@if command -v genesis >/dev/null 2>&1; then \
		if [ -n "$(FOCUS)" ]; then \
			genesis worktree create $(NAME) --focus $(FOCUS); \
		else \
			genesis worktree create $(NAME) --focus src/; \
		fi \
	else \
		echo "❌ Error: Genesis CLI not found. Install with: pip install genesis-cli"; \
	fi

worktree-list: ## List existing AI-safe worktrees
	@if command -v genesis >/dev/null 2>&1; then \
		genesis worktree list; \
	else \
		echo "❌ Error: Genesis CLI not found. Install with: pip install genesis-cli"; \
	fi

worktree-remove: ## Remove AI-safe worktree (usage: make worktree-remove NAME=feature-name)
	@if [ -z "$(NAME)" ]; then echo "❌ Error: NAME is required. Usage: make worktree-remove NAME=feature-name"; exit 1; fi
	@if command -v genesis >/dev/null 2>&1; then \
		genesis worktree remove $(NAME); \
	else \
		echo "❌ Error: Genesis CLI not found. Install with: pip install genesis-cli"; \
	fi

genesis-commit: ## Smart commit with quality gates (usage: make genesis-commit MSG="your message")
	@if command -v genesis >/dev/null 2>&1; then \
		if [ -n "$(MSG)" ]; then \
			genesis commit --message "$(MSG)"; \
		else \
			genesis commit; \
		fi \
	else \
		echo "❌ Error: Genesis CLI not found. Install with: pip install genesis-cli"; \
	fi

genesis-status: ## Check Genesis project health and component status
	@if command -v genesis >/dev/null 2>&1; then \
		genesis status; \
	else \
		echo "❌ Error: Genesis CLI not found. Install with: pip install genesis-cli"; \
	fi

genesis-clean: ## Clean Genesis workspace (remove old worktrees and build artifacts)
	@if command -v genesis >/dev/null 2>&1; then \
		genesis clean; \
	else \
		echo "❌ Error: Genesis CLI not found. Install with: pip install genesis-cli"; \
	fi
