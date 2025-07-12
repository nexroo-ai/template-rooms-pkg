# Template Rooms Package

A template Python package for the AI rooms script addon system.

## Overview

This package provides a basic template implementation for creating addon packages that can be loaded by the AI rooms script. It includes a simple `test()` function that returns `True` when called.

## Installation

```bash
pip install -e .
```

## Usage

This package is designed to be imported by the AI rooms script's `loadAddons` functionality:

```python
import template_rooms_pkg
result = template_rooms_pkg.test()
```

## Development

The project uses semantic release for automated versioning. Releases are triggered automatically on pushes to the main branch.

## License

MIT