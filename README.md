Create an virtual env

virtualenv --version
mkdir ~/env
run virtualenv ~/env/my_new_app
cd ~/env/my_new_app/bin
source activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
