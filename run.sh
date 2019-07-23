rm db.sqlite3
rm -rf company/migrations customuser/migrations contact/migrations
python3 manage.py makemigrations
python3 manage.py makemigrations customuser
python3 manage.py makemigrations company
python3 manage.py makemigrations contact
python3 manage.py migrate
python3 manage.py createsuperuser --email 'test@test.be'
python3 manage.py runserver
