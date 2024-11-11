#!/bin/sh
.PHONY: build dev down ssh publish
build:
	docker image rm -f izdrail/backend.izdrail.com:latest && docker build -t izdrail/backend.izdrail.com:latest --no-cache --progress=plain . --build-arg CACHEBUST=$(date +%s)
dev:
	docker-compose -f docker-compose.yml up  --remove-orphans
down:
	docker-compose down
ssh:
	docker exec -it backend.izdrail.com /bin/zsh
publish:
	docker push izdrail/backend.izdrail.com:latest
