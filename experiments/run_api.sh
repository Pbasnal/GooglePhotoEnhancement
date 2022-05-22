export OAUTHLIB_INSECURE_TRANSPORT=1
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8

export FLASK_APP=app.py
export FLASK_ENV=development

docker run -d --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
flask run --port=8080 --host=0.0.0.0