.PHONY: install build publish run

install:
	poetry install

build: install
	poetry build

publish: build
	poetry publish

run:
	poetry run terminalgpt
