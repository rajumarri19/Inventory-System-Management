INventory Management System
----------------------------

Requirements: django-admin version==5.0.4 

After unzipping the file open it in your code editor. Then you can able to see the inventory_management name tap on that and open settings.py file. After opening settings.py file scroll down and find DATABASES = { 'default': { 'ENGINE': 'django.db.backends.mysql', 'NAME': 'inventory_management', 'USER': 'root', 'PASSWORD': '', 'HOST': '127.0.0.1', 'PORT': '3306', } }

copy the database name 'inventory_management'.

Now open your XAMPPP tool, then start Apachce and MySQL servers. If your server starts running then click on 'Admin' of MySQL Press on the +new from the left side bar Paste the database name 'inventory_management' and press create, your database is created successfully

Now go to your code editor and there select the application name 'website', open migrations folder and delete the file name called '0001_initial.py'

Note: "Never ever delete the file "inint.py"

If you done with it now, run the commands shown below

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser : Here give your preferred username, email, password ( username and password will be used to access 'django administration')
python manage.py runserver
Open the url in your browser 127.0.0.1:8000

On the top right cornor Tap on signup and then you can use it.

THANK YOU :)
