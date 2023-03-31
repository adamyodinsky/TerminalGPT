.PHONY: install build publish run format lint

format:
	poetry run black .

lint:
	poetry run pylint terminalgpt tests

install:
	poetry install

build: install
	poetry build

test: build lint
	poetry run pytest -v 

publish: test
	poetry publish

run-new:
	LOG_LEVEL=DEBUG poetry run terminalgpt new

run-load:
	LOG_LEVEL=DEBUG poetry run terminalgpt load

run-delete:
	LOG_LEVEL=DEBUG poetry run terminalgpt delete
