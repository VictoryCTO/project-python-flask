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

### Exercising the API

Create a user that will allow you to authenticate. For ease of using the project you submit, please do not change the credentials.

```sh
curl \
  -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"Dev Userson", "email":"dev.userson@example.com", "password":"sosecure"}'
```

Show that the user can log in:

```sh
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"email":"dev.userson@example.com", "password":"sosecure"}'
```


# Tasks

For each task please follow this process:
1. Create an issue in your Github project, you are welcome to copy the text of the task provided or write your own, but _please_ use the title here as the title of your GH issue.
1. Add at least one test to your code showing your solution works and ensuring it will continue to work as expected.
1. Make a PR to your code.
1. Merge your PR when you are happy.

:information_source: - All input and response should be assumed to be via `curl`. There is no expectation of a front end being created for this project.

:warning: - Please manage your time. We expect between three and four hours of effort and the associated quality. If you would like to take more time you are welcome to do so, but it is in no way required.

Most importantly, _have fun_.  Show off a bit. Push an opinion or two forward to spark a discussion.

## Required

The following are "required."  We recommend working these first and expect they will take between 2 and 3 hours to complete. If you do not have time to complete them all that is fine.  Ensure you have a priority list and are able to discuss why you prioritized them as you did.

### Github Action

Create a Github action that runs the linting and automated tests. It is a Victory goal that humans don't look at code that is not linted to standard and passing tests unless there is a specfic reason (e.g. a draft pull request).

### Active users

As an application administrator I want to be able to mark a user as "inactive" so that they cannot log in or perform any actions on the system.

Acceptance Criteria
- User can be active or inactive
- An inactive user cannot log in to the system
- New users are created as Inactive by default
- There is a route to hit to toggle active/inactive
- The date a user is made inactive is recorded

### Access Report

As a compliance officer I want to be able to check a report that tells me who my users are and what their access level is so that I can conduct the monthly reviews and drive remediation as required by SOC 2 Type 2.

Accpetance Criteria
- Return a list of users, email and their role(s)
- Be able to get the report for all users, inactive users and/or active users

###  Add the role entity to the model

As an application admin I need to assign each user one or more roles so that they have a clear and predictable set of permissions.  I do not need to override roles at this time.

Acceptance Criteria
- Allow for the creation of one or more roles with attributes role_id, role_name and department_name
  - the combination of role_name and department_name is unique
- Allow for a user to be assigned one or more roles
- Allow for a role to be assigned to one or more users.
- Update the README.md to include how to create a role and assign a user to it in the "Getting Started" section.

### Fix our secrets in code issue

As a compliance officer I want our credentials and other sensitive information removed from source control and stored according to OWASP best practices so that our operations are hardened against external and internal attacks.

In `config.py` there are secrets stored in plain text.
1. Write a Github issue in your project describing the problem in a way you'd like to get it from a product manager/owner.
1. Implement your solution and make a PR.

### Implement the profile route

:information_source: - See `app/routes/user_routes.py`

Write a detailed Github issue explaining your understanding of the requirements as _you_ infer them. Write them as if you will _not_ be the one to work on the task.
- Implement per your requirements
- Be sure to leave directions for how to test your solution in the PR.

## Optional Tasks

If you have some extra time and would like to show off a bit, the following are some suggestions to feed your creativity.  You are _encouraged_ to come up with, document and solve your own problem. Victory places a high value on engineers who work to ensure team efficiency.

Think outside the box for all of this. For example maybe instead of fixing something you'd rather write out a list of several tickets and prioritize them. In this case we will discuss what you are suggesting, approaches and the like.

Alternatively you could find one thing that shows off a particular passion and dive as deep as you like.

Or, you could come up approach we have not thought of. Think of this as a way to shape your interiew towards your interests and passion.

:information_source: - If you decide to tackle something and run out of time, simply make a PR but don't merge it.  Note this in your email telling us where to find your project and it becomes a conversation piece for the final interview.

### Find and fix a security issue

There are many issues of security with our application. You've seen above how we like to communicate tasks, so:
- Write a ticket describing the problem from an end users perspective (As a ..., I want to ..., so that ...), then a list of acceptance criteria.
- Implement the solution in the same way as the other tasks (PR, test, etc)
- Be sure to include anything in the README to your fellow developers if you feel documenting any changes in their behavior would be helpful.

### Improve the build

Our build does some linting with `pre-commit` and runs our tests. If this is a project you are responsible for what would you add?
- Write a ticket describing the gap in the build and the value prop for addressing it.
- Implement the solution.
- Be sure to include anything in the README to help your fellow developers with set up if you feel documentation is warranted.

Remember that writing the ticket is 60% of what we are looking for here. Only implement if this is something you are passionate about.

### Move us to Postgresql

SQLlite is great for something like an interview project. Most Victory projects are backed by Postgres or MySQL.
- Write a ticket describing the work in detail.  Can you write something so technical from an end user perspective?
- Implement your solution.
- Be sure to include anything in the README to help your fellow developers with set up if you feel documentation is warranted.

### Show off your use of a debugger and its integration with your IDE

Show us the lack of print statements in your code and how you go about tracking down values of variables and the like when looking for defects in the code.

# Evaluation Criteria

The people evaluating your submission will do the following before we schedule the final interview.

On a global level, we are evaluating you on your ability
- to communicate in writing (both code and general documentation)
- to infer assumptions in the tasks
- to prioritize tasks and effectively communicate why during the interview.

We will do the following:
1. Clone and run your fork following the instructions in the README under "Getting Started".  We are simply checking to ensure the application functions as expected.
   - We expect there to be instructions for testing the creation of roles and assigning users for us to use. (remember that we prize solid communication)
2. Read each PR
   - Be sure you have a good commit message that describes why the work is done like it is (not what was done, we can see that in the code)
     - this is a chance to show off written communication skills
   - Be sure your code has passed all checks in the build
3. Attempt to run each PR to show that the code is in the expected functional state
4. Attempt to run the test suite
5. Read each Github issue you created and note if/how you tracked your progress.

## Next Step - In Person Technical

Within five business days we will respond to you to schedule a 90 minute in-person interview with Victory staff or a note to let you know we are going in a different direction.

To prepare for the interview be ready to
- demo a working project.
  - Some candidates keep going because they are having fun.  That is just fine, but be sure you have a working project to demo
- discuss your overall approach around priority, documentation, etc.
- discuss specifics of implementing requirements

Please note that folks on the team are often taking a position counter to your own. It is of primary importance that members of Victory teams can disagree, discuss and come to a common understanding and path forward.

You should walk away with a solid understanding of what it is like to work on a Victory team on a daily basis. We understand that you may not want to work the way we do.  Better for all concerned if we figure that out as early as possible.

# Thank you

We are going to make six figure bet on you. You are going to put your career in our hands and expect us to help you grow professionally.

We deeply appreciate the time you are taking to ensure joining Victory is of benefit to all concerned (yourself, Victory and our clients).

# 01 Added this comment for testing purposes.
# 02 Post-pull of action workflow to sync local with remote.
# 03 Error in workflow from Poetry version. Changed from 1.5.1 to 1.8.3.
# 04 Pyproject.toml changed significantly since poetry.lock was last generated.
# 05 04 push did not activate action because of md extension in paths-ignore.
# 06 More changes, including removal of poetry caching from workflow to help find the bug.
# 07 That worked. Warnings for trim trailing spaces and fix end of files. Pulled origin to sync local.
# 08 Issue 01 resolved.
# 09 Text to provide change to this file.
