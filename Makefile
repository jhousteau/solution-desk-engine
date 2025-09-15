.PHONY: help setup install dev test test-cov format lint typecheck quality check-org validate-bootstrap clean build install-cli run-dev worktree-create worktree-list worktree-remove genesis-commit genesis-status genesis-clean sync version version-show version-bump-patch version-bump-minor version-bump-major version-sync

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Run initial project setup
	./scripts/setup.sh

install: ## Install dependencies only
	poetry install

dev: setup ## Alias for setup (install with development dependencies)

test: ## Run tests
	poetry run pytest

test-cov: ## Run tests with coverage
	poetry run pytest --cov --cov-report=html --cov-report=term

format: ## Format code with black and isort
	poetry run black src/ tests/
	poetry run isort src/ tests/

lint: ## Lint code with flake8
	poetry run flake8 src/ tests/

typecheck: ## Type check with mypy
	poetry run mypy src/

quality: format lint typecheck ## Run all quality checks

check-org: ## Check project file organization
	./.genesis/scripts/check-file-organization.sh

validate-bootstrap: ## Validate that bootstrap setup completed successfully
	./.genesis/scripts/validate-bootstrap.sh

clean: ## Clean build artifacts and backup files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -name "*.bak" -type f -delete 2>/dev/null || true
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -type f -delete 2>/dev/null || true
	@echo "Cleaned build artifacts, cache files, and backup files"

build: ## Build the package
	poetry build

install-cli: build ## Install CLI locally
	pip install dist/*.whl

run-dev: ## Run CLI in development mode
	poetry run solution-desk-engine

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

sync: ## Update project support files from Genesis templates
	@if command -v genesis >/dev/null 2>&1; then \
		genesis sync; \
	else \
		echo "❌ Error: Genesis CLI not found. Install with: pip install genesis-cli"; \
	fi

# Version Management Targets
version: version-show ## Show current version (alias for version-show)

version-show: ## Show current project version
	@python .genesis/scripts/version.py show

version-bump-patch: ## Bump patch version (1.0.0 → 1.0.1)
	@./.genesis/scripts/bump-version.sh patch

version-bump-minor: ## Bump minor version (1.0.0 → 1.1.0)
	@./.genesis/scripts/bump-version.sh minor

version-bump-major: ## Bump major version (1.0.0 → 2.0.0)
	@./.genesis/scripts/bump-version.sh major

version-sync: ## Sync current version across all project files
	@python .genesis/scripts/version.py sync
