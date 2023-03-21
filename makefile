.PHONY: install build publish run format lint

format:
	poetry run black .

lint:
	poetry run pylint terminalgpt tests

install:
	poetry install

build: install
	poetry build

test: build
	poetry run pytest -v 

publish: test
	poetry publish

run:
	poetry run terminalgpt
