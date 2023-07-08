up:
	docker-compose up

run-db:
	docker-compose up -d db

run-backend:
	docker-compose up web
	docker-compose exec web sh -c "pip install -r requirements.txt && python3 workorders/manage.py migrate"

drop-create-db: run-db
	docker-compose exec db dropdb -U admin --if-exists workorders
	docker-compose exec db createdb -U admin workorders
	docker-compose up -d web

