# project-python-flask
This project is in support of efforts to hire python engineers.


# Getting Started

Ensure you can run the application locally by cloning it.

These directions assume you will use `poetry` for dependency and environment management.


## Install dependencies
```sh
poetry install
```

## Building the software

### Linting

You many need to install the [pre-commit project](https://pre-commit.com/#install)

Then run

```sh
pre-commit run --all-files
```

You should get output showing "Passed" or (for json files) "Skipped"

```
trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
check yaml...............................................................Passed
check json...........................................(no files to check)Skipped
black....................................................................Passed
```

### Automated tests

There are a couple of automated tests to run.

```sh
poetry run pytest --verbose
```

You should see something similar to:

```
============================================================================================= test session starts ==============================================================================================
platform darwin -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0 -- /Users/boyd.hemphill/Library/Caches/pypoetry/virtualenvs/project-python-flask-mx59eYov-py3.12/bin/python
cachedir: .pytest_cache
rootdir: /Users/boyd.hemphill/code/project-python-flask
configfile: pyproject.toml
testpaths: tests
collected 3 items

tests/test_auth.py::test_register_user PASSED                                                                                                                                                            [ 33%]
tests/test_auth.py::test_login_user PASSED                                                                                                                                                               [ 66%]
tests/test_auth.py::test_login_invalid_user PASSED                                                                                                                                                       [100%]

============================================================================================== 3 passed in 0.03s ===============================================================================================

```

## Starting the application

```sh
export FLASK_ENV=development # use the development settings
poetry run python app.py
```

You should see something like this:

```
/code/project-python-flask >poetry run python run.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 413-423-614
 ```

### Implementaion

- Starting with creating roles which we will assign to users. I added super and admin user roles that can make other users active or inactive. Super user is active by default so they dont have login restrictions so they can make other users active or inactive to get into the site.
- Then Registering a user and assigning that Role to the user.
- Next I made an API that will assign roles to the users, The role id against user id with proper error handling.
- Then I have made an API that will make a user Admin so They can toggle the status of any user.
- Then I made toggle statis APi endpoint that will make a user active or inactive. and Only admins or super users can do it. For this after login, the API will return a token, which we will have to copy and send as request body to toggle the status for permission purposes.
- Then I added acces report aPI, that will make a csv file in you directory will all the users data. separately for active and inactive users.

### Creating a Role

```sh
curl -X POST http://127.0.0.1:5000/roles \
  -H "Content-Type: application/json" \
  -d '{
    "role_name": "super",
    "department_name": "all"
  }'
```
### Creating a user

Create a user that will allow you to authenticate. For ease of using the project you submit, please do not change the credentials.

```sh
curl \
  -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"Dev Userson", "email":"dev.userson@example.com", "password":"sosecure"}'
```

### Assign Role to a user

Assign a role to a user. The IDs you can get from the response for creating these roles.

```sh
curl -X POST http://127.0.0.1:5000/roles/assign -H "Content-Type: application/json" -d '{"user_id": 1, "role_id": 1}'
```

### Login user

Show that the user can log in:

```sh
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"email":"dev.userson@example.com", "password":"sosecure"}'
```

### Making a simple user an admin

```sh
curl -X PUT http://127.0.0.1:5000/make_admin \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'
```

### Toggle user active status

```sh
curl -X PUT http://127.0.0.1:5000/toggle_user_status \
    -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlcyI6WyJBZG1pbiIsInN1cGVyIl0sImV4cCI6MTcyOTE2ODc2Mn0.UP5_5Ean_hE72O4_G3KzDWdFnxeNdhkxoMliCvaN0k0" \
    -H "Content-Type: application/json" \
    -d '{"user_id": 2, "activate": true}'
```
You can get and replace the token with the one you will get when loging in. It will return a bearer token  in the response body.
So not every one can change the status of the user.

### Toggle user active status
To see the csv in which all users data is present, I made an endpoint that will return user information but not anything that will breach security and provide personal information of the user like password.

```sh
curl -s -X GET http://127.0.0.1:5000/user_report -o user_report.csv
```
