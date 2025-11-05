APP_NAME=sentiment
NETWORK_NAME=mlops-net
VOLUME_NAME=mlops-logs

build:
	docker build -t api-service ./api
	docker build -t monitoring-service ./monitoring

run:
	docker network create $(NETWORK_NAME) || true
	docker volume create $(VOLUME_NAME) || true
	docker run -d --name api --network $(NETWORK_NAME) -v $(VOLUME_NAME):/logs -p 8000:8000 api-service
	docker run -d --name monitoring --network $(NETWORK_NAME) -v $(VOLUME_NAME):/logs -v $(PWD)/data:/data -p 8501:8501 monitoring-service

clean:
	docker rm -f api monitoring || true
	docker network rm $(NETWORK_NAME) || true
	docker volume rm $(VOLUME_NAME) || true
