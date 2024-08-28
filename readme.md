run-local = python main.py
run-worker = celery -A src.celery_worker.celery worker --loglevel=info 
run-beat = celery -A src.celery_worker.celery beat --loglevel=info 
run-test = coverage run -m pytest
run-coverage = coverage report
run-coverage-html = coverage html
run-docker = docker-compose up --build