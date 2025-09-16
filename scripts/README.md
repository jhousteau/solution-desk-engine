# Scripts Directory

## Available Scripts

### Main Scripts
- **container-rebuild.sh**: Complete container rebuild workflow: clean, sync, rebuild, and enter shell
- **setup.sh**: Project setup and configuration script
- **container-setup.sh**: Container environment setup

### Genesis Scripts (`.genesis/scripts/`)
Development and quality assurance utilities:

- **audit-agent.sh**: Security audit for agent container
- **bump-version.sh**: Version management and release automation
- **check-ai-signatures.sh**: Validate AI-generated code signatures
- **check-file-organization.sh**: Enforce Genesis file organization standards
- **check-genesis-components.sh**: Validate Genesis component structure
- **check-variable-defaults.sh**: Check configuration variable defaults
- **find-hardcoded-values.sh**: Detect hardcoded values in configuration
- **setup-agent.sh**: Agent container setup and configuration
- **validate-bootstrap.sh**: Validate project bootstrap configuration
- **validate-components.sh**: Component validation checks
- **version.py**: Python version management utilities

## Usage

### Development Workflow
```bash
# Setup project
./scripts/setup.sh

# Rebuild containers
./scripts/container-rebuild.sh

# Run quality checks
./.genesis/scripts/check-file-organization.sh
./.genesis/scripts/audit-agent.sh
```

### Version Management
```bash
# Bump version
./.genesis/scripts/bump-version.sh

# Validate configuration
./.genesis/scripts/validate-bootstrap.sh
```

## Integration

These scripts integrate with:
- **Make targets**: Called by Makefile commands
- **Pre-commit hooks**: Quality validation
- **Genesis framework**: Development standards enforcement
- **Docker workflow**: Container management and deployment
