# Universal Hardened Development Container for Genesis Projects
# Combines security best practices with full development freedom in /workspace
# Supports Python, Node.js, and other development tools

FROM --platform=$BUILDPLATFORM python:3.13-slim-bookworm

SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="/opt/poetry/bin:/usr/local/bin:/usr/bin:/bin" \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Versions (pin for reproducibility)
ARG NODE_MAJOR=20
ARG POETRY_VERSION=1.8.3
# NOTE: Do NOT ARG/ENV secrets. Use BuildKit --secret instead for GitHub token.

# Base tools + tini (init) + user management in one layer
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates curl wget git openssh-client jq unzip tree \
      build-essential gcc make procps htop vim nano direnv tini gnupg \
      passwd adduser && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user (user commands are in /usr/sbin)
RUN /usr/sbin/groupadd -r -g 1000 developer && \
    /usr/sbin/useradd -r -g developer -u 1000 -m -d /home/developer -s /bin/bash developer

# GitHub CLI (gh) for version control
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
      | gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
      > /etc/apt/sources.list.d/github-cli.list && \
    apt-get update && apt-get install -y --no-install-recommends gh && \
    rm -rf /var/lib/apt/lists/*

# Node.js + Corepack (Yarn/PNPM managed per-project)
RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_MAJOR}.x | bash - && \
    apt-get update && apt-get install -y --no-install-recommends nodejs && \
    corepack enable && \
    npm config set fund false && \
    npm config set audit false && \
    npm config set update-notifier false && \
    npm install -g typescript "@anthropic-ai/claude-code" && \
    rm -rf /var/lib/apt/lists/*

# Poetry with cache optimization
RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install --upgrade pip setuptools wheel && \
    curl -fsSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION} && \
    chmod -R 755 /opt/poetry
ENV PATH="/opt/poetry/bin:${PATH}"

# Optional Genesis CLI from GitHub Releases using BuildKit secret
#   docker build --secret id=github_token,env=GITHUB_TOKEN ...
# Avoids caching/leaking token.
RUN --mount=type=secret,id=github_token \
    if [ -f /run/secrets/github_token ]; then \
      echo "Installing Genesis CLI from GitHub Releases..."; \
      export GITHUB_TOKEN="$(cat /run/secrets/github_token)"; \
      urls=$(curl -sH "Authorization: token ${GITHUB_TOKEN}" \
        https://api.github.com/repos/jhousteau/genesis/releases/latest \
        | jq -r '.assets[] | select(.name|endswith(".whl")) | .browser_download_url'); \
      for url in $urls; do curl -sSLH "Authorization: token ${GITHUB_TOKEN}" -O "$url"; done; \
      python3 -m pip install ./genesis_shared_core-*.whl ./genesis_cli-*.whl || \
        echo "No Genesis packages yet."; \
      rm -f *.whl; \
    else \
      echo "Skipping Genesis CLI installation (no secret provided)"; \
    fi

# Workspace
RUN mkdir -p /workspace/{projects,scripts,data,logs,temp} && \
    chown -R developer:developer /workspace /home/developer

# Shell/direnv
RUN echo 'eval "$(direnv hook bash)"' >> /home/developer/.bashrc && \
    install -d -m 755 /home/developer/.config/direnv && \
    printf '[whitelist]\nprefix = ["/workspace"]\n' > /home/developer/.config/direnv/direnv.toml && \
    chown -R developer:developer /home/developer

# Git defaults
RUN su developer -c 'git config --global user.name "Developer"' && \
    su developer -c 'git config --global user.email "developer@solution-desk-engine.local"' && \
    su developer -c 'git config --global init.defaultBranch main'

# --- Workspace cd-guard (toggle via JAIL_MODE=cd-guard) ---
RUN install -m 0644 /dev/stdin /etc/profile.d/workspace_jail.sh <<'EOS'
# Enforce staying under /workspace (interactive shells)
cd() {
  local dest="${1:-$HOME}"
  if [[ "$dest" == /* && "$dest" != /workspace* ]]; then
    echo "Access denied: outside /workspace" >&2
    return 1
  fi
  builtin cd "$@"
}
readonly -f cd
# Bounce back if some tool teleports us out
export PROMPT_COMMAND='[[ "$PWD" != /workspace* ]] && builtin cd /workspace || true'
EOS
# Apply to non-interactive shells (bash -c)
RUN install -m 0644 /dev/stdin /etc/bash_workspace_jail <<'EOS'
source /etc/profile.d/workspace_jail.sh
EOS

# Setup script (mounted path safe)
COPY scripts/container-setup.sh /usr/local/bin/container-setup.sh
RUN chmod +x /usr/local/bin/container-setup.sh || true

# Minimal entry script
RUN install -m 0755 /dev/stdin /usr/local/bin/entrypoint.sh <<'EOF'
#!/bin/bash
set -euo pipefail

# Colors for clean output
GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo -e "${BLUE}🚀 solution-desk-engine Development Container${NC}"
echo "🔧 User: $(whoami) | Project: ${PROJECT_TYPE:-generic}"
echo "🐍 $(python --version 2>&1) | 📦 $(node --version 2>&1)"
echo -e "${GREEN}🔒 Hardened container ready${NC}"
echo ""

# Copy setup script to workspace if needed
if [ -f /usr/local/bin/container-setup.sh ] && [ ! -f /workspace/scripts/container-setup.sh ]; then
  mkdir -p /workspace/scripts && cp /usr/local/bin/container-setup.sh /workspace/scripts/container-setup.sh || true
fi

# Auto-setup if requested
if [ "${AUTO_SETUP:-false}" = "true" ] && [ -x /workspace/scripts/container-setup.sh ]; then
  echo -e "${YELLOW}🚀 Running automated setup...${NC}"
  /workspace/scripts/container-setup.sh || true
fi

echo -e "${BLUE}💡 Quick Start:${NC}"
echo "   ./scripts/container-setup.sh    # Run setup"
echo "   poetry run python -m genesis.cli --help"
echo ""

# Set reasonable ulimits
ulimit -c 0 || true
ulimit -n 4096 || true
ulimit -u 1024 || true

# Enable cd-guard for both interactive and non-interactive shells
if [[ "${JAIL_MODE:-}" == "cd-guard" ]]; then
  export BASH_ENV=/etc/bash_workspace_jail
fi

exec "$@"
EOF

# Environment (keep HOME sane)
ENV PYTHONPATH=/workspace \
    PYTHONUNBUFFERED=1 \
    HOME=/home/developer \
    USER=developer \
    SHELL=/bin/bash \
    PROJECT_NAME=solution-desk-engine \
    PROJECT_TYPE=cli-tool \
    PROJECT_MODE=development \
    LOG_LEVEL=info \
    ENABLE_GIT=false

USER developer
WORKDIR /workspace

ENTRYPOINT ["/usr/bin/tini","--","/usr/local/bin/entrypoint.sh"]
CMD ["bash", "-lc", "tail -f /dev/null"]

# Honest healthcheck—only checks the basics
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD bash -lc 'command -v python >/dev/null && command -v node >/dev/null && [ -d /workspace ] || exit 1'

LABEL org.opencontainers.image.title="solution-desk-engine Development Container" \
      org.opencontainers.image.description="Hardened dev container for Genesis projects" \
      org.opencontainers.image.source="https://github.com/jhousteau/solution-desk-engine" \
      security.user="developer" \
      security.no-new-privileges="true" \
      genesis.template="shared" \
      genesis.version="1.1"
