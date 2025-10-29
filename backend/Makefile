run:
	uvicorn app.main:app --reload

test:
	pytest -v

lint:
	ruff check .

docker-build:
	docker build -t rag-api .

docker-run:
	docker run -p 8000:8000 rag-api
