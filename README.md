# first cd to main 

build docker

` docker-compose build `

run project by

` make up `

migrate db

` docker-compose exec web python workorders/manage.py migrate `

run test case

` docker-compose exec web python workorders/manage.py test workorders.tests `
