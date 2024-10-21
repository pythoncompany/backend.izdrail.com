#!/bin/sh
build:
	docker image rm -f izdrail/intel.izdrail.com:latest && docker build -t izdrail/intel.izdrail.com:latest --no-cache --progress=plain . --build-arg CACHEBUST=$(date +%s)
dev:
	docker-compose -f docker-compose.yml up  --remove-orphans
down:
	docker-compose down
ssh:
	docker exec -it intel.izdrail.com /bin/zsh
publish:
	docker push izdrail/intel.izdrail.com:latest
