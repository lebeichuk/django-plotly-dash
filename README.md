Create virtual environment 

-virtualenv --version  
-mkdir ~/env  
-virtualenv ~/env/my_new_app  
-cd ~/env/my_new_app/bin  
-source activate  
-pip install -r requirements.txt  
-python manage.py runserver  

Actions needed for stripe subscriptions  
-pip install --upgrade stripe  
-pip install dj-stripe  
-create weebhook at https://dashboard.stripe.com/webhooks with your url  
after adding weebhook endpoint (publicly accessible URL) run following commands:  
-py manage.py migrate  
-py manage.py djstripe_sync_plans_from_stripe  