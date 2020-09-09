BUILD_IMAGE_NAME=project
DOCKER_COMP_EXEC_CMD=docker-compose exec -T $(BUILD_IMAGE_NAME)
DOCKER_EXEC_CMD=docker exec -it $(BUILD_IMAGE_NAME)
DOCKER_COMP_CMD=docker-compose -T $(BUILD_IMAGE_NAME)

raise-infrastructure:
	$(info Raising Infrastructure)
	docker-compose up -d

test:
	#make pipeline/db_to_start
	$(DOCKER_COMP_EXEC_CMD) python -m pytest --cov-report=term-missing:skip-covered --cov=project test/ --no-cov-on-fail

mypy:
	$(DOCKER_COMP_EXEC_CMD) python -m mypy .

test-single:
	$(DOCKER_COMP_EXEC_CMD) python -m pytest $(test)

black:
	$(DOCKER_COMP_EXEC_CMD) black --check .

flake8:
	$(DOCKER_COMP_EXEC_CMD) flake8 ./project --extend-ignore=C901 --max-line-length=88

pipeline/qa:
	make mypy
	make black
	make flake8
	make test

pipeline/db_to_start:
	counter=0
	while [ ! "$$(docker logs mysql 2>&1 | grep "MySQL init process done. Ready for start up.")" ]; do \
		counter=$$((counter+1)); \
		sleep 5; \
		echo "Rechecking if image is up"; \
		if [ "$$counter" -eq 50 ]; then \
			echo "Too many retries"; \
			exit 1; \
		fi \
	done

shell:
	$(info Connecting container)
	docker exec -it ${BUILD_IMAGE_NAME} /bin/sh

.PHONY: test lint