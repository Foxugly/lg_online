#rm db.sqlite3
#rm -rf company/migrations customuser/migrations accountant/migrations simulation/migrations company/migrations agenda/migrations address/migrations
python3 manage.py makemigrations address
python3 manage.py makemigrations customuser
python3 manage.py makemigrations company
python3 manage.py makemigrations agenda
python3 manage.py makemigrations simulation
python3 manage.py makemigrations accountant
python3 manage.py migrate
python3 manage.py createsuperuser --email 'test@test.be'
python3 manage.py shell < create_accountant.py
python3 manage.py shell < create_slots.py
python3 manage.py runserver
