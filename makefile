.PHONY: install build publish run

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
