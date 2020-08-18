## TODO app

A simple web app created with django to store and track your tasks. You can easily add a task, mark it as completed, or delete it. You can also see when you added and completed a task. All tasks are stored in your own account.

#### Installation instructions

1. Download and install [Git](https://git-scm.com/downloads).

2. Install [Python 3.8.3](https://www.python.org/downloads/release/python-383/) or greater.

3. Install virtualenv with

		pip install virtualenv

    or

		py -m pip install virtualenv

    or

		python -m pip install virtualenv

4. Create your virtual environment.
	
	- Create the root directory:

			mkdir todo_app
			cd todo_app
	
	- Create and activate your virtual environment:

			virtualenv venv
			venv\Scripts\activate
	
5. Clone the github repository.

		git clone https://github.com/j-millan/todo-app.git

6. Install all the requirements.

		cd todo-app
		pip install -r requirements.txt

7. Add a new secret key.
	
	- Go to [miniwebtool](https://miniwebtool.com/django-secret-key-generator/) and generate a new key.

	- Create a file called `secrets.py` inside *todo-app/project* and add the next line of code:

			SECRET_KEY = 'generated_secret_key_here'

	- Save the file.

8. Run the migration files.
	
		python manage.py migrate

9. Run the tests to make sure everything is working.
		
		python manage.py test

	You should get the next output:

		Creating test database for alias 'default'...
		System check identified no issues (0 silenced).
		....................................
		----------------------------------------------------------------------
		Ran 36 tests in 18.262s

		OK
		Destroying test database for alias 'default'...

***

Now you can run the server using `python manage.py runserver`.

Go to [127.0.0.1:8000/](http://127.0.0.1:8000/) and start using the app!
