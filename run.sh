rm db.sqlite3
rm -rf company/migrations customuser/migrations accountant/migrations simulation/migrations company/migrations agenda/migrations address/migrations
python3 manage.py makemigrations address
python3 manage.py makemigrations customuser
python3 manage.py makemigrations company
python3 manage.py makemigrations agenda
python3 manage.py makemigrations simulation
echo "in accountant.models : comment weektemplate and slot"
read -p "Press any key to continue... " -n1
python3 manage.py makemigrations accountant
python3 manage.py migrate
echo "in accountant.models : uncomment weektemplate and slot"
read -p "Press any key to continue... " -n1
python3 manage.py makemigrations accountant
python3 manage.py migrate
echo "create superuser"
python3 manage.py createsuperuser
echo "Create accountant"
python3 manage.py shell < create_accountant.py
echo "Create slots"
# python3 manage.py shell < create_slots.py
echo "END - runserver"
python3 manage.py runserver
