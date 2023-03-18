.PHONY: install build publish run

install:
	poetry install

build: install
	poetry build

test: install
	poetry run pytest -v 

publish: build
	poetry publish

run:
	poetry run terminalgpt
