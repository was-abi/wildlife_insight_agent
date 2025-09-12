# Project Structure

## Organization Principles
- Keep related files together in logical directories
- Separate source code, tests, documentation, and configuration
- Use clear, descriptive folder and file names
- Maintain consistent naming conventions throughout the project

## Common Directory Structure
```
/
├── src/                 # Source code
├── tests/              # Test files
├── docs/               # Documentation
├── config/             # Configuration files
├── scripts/            # Build and utility scripts
├── assets/             # Static assets (images, fonts, etc.)
├── .kiro/              # Kiro configuration and steering
│   └── steering/       # AI assistant guidance files
├── README.md           # Project overview and setup instructions
├── .gitignore          # Git ignore patterns
└── [package files]     # package.json, Cargo.toml, requirements.txt, etc.
```

## File Naming Conventions
- Use lowercase with hyphens for directories: `user-management/`
- Use appropriate extensions for file types
- Keep file names descriptive but concise
- Group related files with consistent prefixes when beneficial

## Code Organization
- Separate concerns into different modules/files
- Keep public interfaces clean and well-documented
- Place utility functions in dedicated utility modules
- Organize imports/dependencies logically at the top of files

## Documentation Structure
- README.md in root for project overview
- API documentation alongside code when possible
- Separate docs/ folder for comprehensive documentation
- Include examples and usage patterns in documentation