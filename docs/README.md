# PROJECT_NAME Documentation

This directory contains all documentation for the PROJECT_NAME project.

## Structure

- **api/** - API reference documentation and technical specifications
- **guides/** - How-to guides, tutorials, and user documentation  
- **architecture/** - System design documents and architecture decisions

## Contributing to Documentation

When adding documentation:

1. Place API docs in the `api/` directory
2. Place user guides and tutorials in `guides/`  
3. Place architecture decisions and design docs in `architecture/`
4. Use clear, descriptive filenames
5. Follow the existing documentation style

## Building Documentation

For projects that generate documentation:

```bash
# Build API documentation
make docs

# Serve docs locally  
make serve-docs
```