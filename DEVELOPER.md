# Developer Guide

TODO: Switch to Zensical or ProperDocs.

## Documentation

The project documentation is located in the [`docs/`](docs) directory and is built using [MkDocs](https://www.mkdocs.org/) with the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme (configured in [`mkdocs.yml`](mkdocs.yml)). This doc is about how to locally build and test. The actual deployment is handled via a [GitHub CI](.github/workflows/mkdocs_deploy.yml).

### Environment Setup & Prerequisites

Set up and activate a Python virtual environment in `.venv`, then install MkDocs and the Material theme:

```bash
# Create the virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install MkDocs dependencies
pip install mkdocs mkdocs-material
```

### Live Preview

With `.venv` activated, start the local development server with auto-reloading. The link to view the local website will be shown in the output.

```bash
mkdocs serve
```

### Build Site

(Not typically needed; GitHub CI does this.) With `.venv` activated, build the static HTML site (output will be generated in `site/`):

```bash
mkdocs build
```
