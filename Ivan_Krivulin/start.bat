pip install -r req.txt
cd ma_app
python manage.py makemigrations
python manage.py migrate
python manage.py runserver