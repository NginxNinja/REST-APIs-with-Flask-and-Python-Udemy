# Important instructions to do to make the codes work.

### Install the following in the terminal:

1. python3 -m pip install --upgrade pip
2. python3 -m pip install flask
3. sudo apt-get install python3-venv (For Ubuntu)  \
Error messages when trying to run the Step 3 below:
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt-get install python3-venv

You may need to use sudo with that command. After installing the python3-venv
package, recreate your virtual environment.

Failing command: ['/[some_paths_here]/virtualenvironment/bin/python3', '-Im', 'ensurepip', '--upgrade', '--default-pip']

4. python3 -m venv /path/to/new/virtual/environment  \
(Source: https://docs.python.org/3/library/venv.html)  \
(Old virtualenv but still have useful information: https://docs.python-guide.org/dev/virtualenvs/)

### Commands that need to run inside the Python virtual environment:

1. python3 -m pip install --upgrade pip
2. python3 -m pip install flask
3. python3 -m pip install Flask-RESTful

### Commands that are useful during the development:

1. python3 -m pip freeze  \
This will show the Python libraries that are installed on the current development environment, and their respective versions.
2. python3 -m pip freeze > requirement.txt  \
(More info about this command: https://docs.python-guide.org/dev/virtualenvs/#other-notes)
3. Changing a git remote's URL - https://docs.github.com/en/github/using-git/changing-a-remotes-url  \
HTTPS - $ git remote set-url origin https://github.com/USERNAME/REPOSITORY.git  \
SSH - $ git remote set-url origin git@github.com:USERNAME/REPOSITORY.git
4. git commit --amend  \
Rewriting the last commit message or updating a newer staged file/s to the last commit  \
(Source: https://www.atlassian.com/git/tutorials/rewriting-history)
