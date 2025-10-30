## Environments
IMAGE_NAME = litera.corp/frontend
IMAGE_VERSION = 1.0
CONTAINER_NAME = litera_corp-frontend
APP_PORT = 7700
VITE_PORT = 5173


build:
	docker build -t $(IMAGE_NAME):$(IMAGE_VERSION) .

run:
	docker run \
		-p 0.0.0.0:$(APP_PORT):$(VITE_PORT) \
		--name $(CONTAINER_NAME) \
		$(IMAGE_NAME):$(IMAGE_VERSION)

dev:
	docker run -dit \
		-p 0.0.0.0:$(APP_PORT):$(VITE_PORT) \
		-v "$(PWD):/app" \
		--name $(CONTAINER_NAME) \
		$(IMAGE_NAME):$(IMAGE_VERSION)
