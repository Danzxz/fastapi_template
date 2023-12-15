stop-docker:
	docker compose down

run-docker: stop-docker
	docker compose up -d

test-docker: stop-docker
	docker compose docker-compose.test.yaml do up -d