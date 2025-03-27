#!/bin/bash

cd ../

.venv/bin/poetry run ruff check .
# .venv/bin/poetry run ruff format .
.venv/bin/poetry run pytest
