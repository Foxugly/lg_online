sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3
sudo apt-get install python3-pip python3-venv
sudo apt-get apache2 libapache2-mod-wsgi-py3 
cd ~
mkdir mlg
cd mlg
git clone https://github.com/Foxugly/lg_online.git
python3 -m venv venv
source venv/bin/activate
cd  lg_online
pip install -r requirements.txt
sudo cp lg_online80.conf /etc/apache2/sites-enabled/mlg.conf
sudo ln /etc/apache2/sites-available/mlg.conf /etc/apache2/sites-enabled/mlg.conf -s
./run.sh
deactivate
sudo chown -R www-data:www-data *
sudo service apache2 restart
