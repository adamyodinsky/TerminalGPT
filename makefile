.PHONY: install build publish run format lint test \
				test-e2e test-inte test-unit run-install \
				run-new run-load run-delete run-version

format:
	poetry run black .
	poetry run isort .

lint:
	poetry run pylint terminalgpt tests

install:
	poetry install

build: install
	poetry build

test:
	poetry run pytest -v --disable-warnings --cov=terminalgpt

test-unit:
	poetry run pytest -v --disable-warnings --cov=terminalgpt tests/unit/test_conversations.py

test-inte:
	poetry run pytest -v --disable-warnings --cov=terminalgpt tests/integration

test-e2e:
	poetry run pytest -v --disable-warnings --cov=terminalgpt tests/e2e

publish: build test-unit test-inte
	poetry publish

run-install:
	LOG_LEVEL=DEBUG poetry run terminalgpt install

run-new:
	LOG_LEVEL=DEBUG poetry run terminalgpt new

run-load:
	LOG_LEVEL=DEBUG poetry run terminalgpt load

run-delete:
	LOG_LEVEL=DEBUG poetry run terminalgpt delete

run-version:
	poetry run terminalgpt --version
