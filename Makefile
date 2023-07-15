.PHONY: build

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down --remove-orphans

clean:
	docker compose down --remove-orphans -v

all: build up
