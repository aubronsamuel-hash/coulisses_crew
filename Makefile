.RECIPEPREFIX = >
.PHONY: fmt lint

fmt:
> black .

lint:
> ruff check .
> black --check .
