build:
	docker build -t nginix_rpw:1.0.0 -f test_created_container/Dockerfile .

test_created_container: build
	python3 test_created_container/test.py

compose_test:
	docker-compose -f test_docker_compose_service/docker-compose.yml up -d
	python3 test_docker_compose_service/test.py
	docker-compose -f test_docker_compose_service/docker-compose.yml down
