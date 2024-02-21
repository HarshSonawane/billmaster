<h1>Bill Master Services</h1>

https://www.codingforentrepreneurs.com/blog/install-python-django-on-windows


1. Check out this project.
2. Change directory into project -> cd project
3. Create virtualenv -> 
	For Windows -> python -m virtualenv env (It should create new folder called env inside it)
	For Linux/Unix/Mac -> python -m virtualenv env (It should create new folder called env inside it)
4. Acticate environment -> 
	For Windows -> env\Scripts\activate
	For Linux/Unix/Mac -> env/Scripts/activate
5. Run command to install dependecies -> pip install -r requirements.txt
6. To create the super user run -> python manage.py createsuperuser (to create the user)
7. To up the server run -> python manage.py runserver (to up the server)