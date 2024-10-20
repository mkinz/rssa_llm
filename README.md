RSSA LLM (no rag)
1. activate virtual env
2. pip3 install -r requirements.txt

To run flask webserver:
python run_dev_server.py

To run prod webserver:
gunicorn --log-level debug --capture-output --enable-stdio-inheritance src.main:app


To build project in Docker and run prod websever in container:
docker-compose up --build

To test webserver is running:
python3 mock_api.py --url http://localhost:8000 --healthz

To test webserver can connect to LLM api:
python3 mock_api.py --url http://localhost:8000 --ready


Some example mock api calls once webserver is running:
python3 mock_api.py --url http://localhost:8000/process --output response.json --input src/client-exports/hall_munster.json
