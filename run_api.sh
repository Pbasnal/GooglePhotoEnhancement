export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8

export FLASK_APP=app.py
export FLASK_ENV=development

echo "Google credentials"
echo $GOOGLE_CLIENT_CREDENTIAL
echo "---"
flask run --host=0.0.0.0 --port=8000