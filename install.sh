sudo apt-get install python3-pip
sudo pip3 install virtualenv
cd ~/mlg/
virtualenv venv -p python3
source venv/bin/activate
git clone https://github.com/Foxugly/lg_online.git
source venv/bin/activate
cd lg_online
pip install -r requirements.txt
nano lg/settings.py
touch lg/credential_email.py
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
