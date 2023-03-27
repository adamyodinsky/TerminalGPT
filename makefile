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
	poetry run terminalgpt --debug new

run-load:
	poetry run terminalgpt --debug load

run-delete:
	poetry run terminalgpt delete
