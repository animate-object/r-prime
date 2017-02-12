# Setting up your environment for local dev
This document is for members of the P.W.A. project team. 
It outlines how to set up your development environment on windows.

## Getting Python 3.5 64-bit
You will need python 3.5. TensorFlow doesn't officially support higher (or lower)
versions of python at this time. It is ***very important*** that you have the **64 bit package**.
* [Download](https://www.python.org/downloads/release/python-352/) -- you'll want one of the x86-64 installers for windows.

## Adding python to your PATH (environment variable)
In order to run python from the command line, windows has to know where to look.
This process will vary slightly depending on what version of windows you are running.
Look for 'system' on your control panel (you may have to change the sorting option to icons).
From system look for advanced system properties. 

That should open a dialogue box with an option for environment variables. Click that. This should open an additional dialog box with 
User variables and System variables. On System variables, look for `Path`

If you are running windows 8 or earlier, your path variable will look like a list of file paths 
separated by semicolons `;`. You will need to add the following to the end of your path variable. Be
careful not to delete what's already there:
```
C:\<path to your python install>\Python\Python35;C:\<path to your python install>\Python\Python35\Lib\site-packages\;C:\<path to your python install>\Python\Python35\Scripts\
```

Where <path to your python install> is replaced by -- you guessed it, the path to your python install.

If you're on windows 10 this is a little easier. Press the windows key and type `environment variables`.
Select the option to 'edit system and environment variables'. Similarly, find the `Path` variable under System 
variables and edit it. Instead of separating the three directories above by `;`, simply enter them on separate lines:

```
C:\<path to your python install>\Python\Python35
C:\<path to your python install>\Python\Python35\Lib\site-packages\
C:\<path to your python install>\Python\Python35\Scripts\
```

Again replacing the text in <> with the path to your python install.

Now you can run python scripts and commands from CMD prompt!

## Upgrading some python utilities
The easiest way to install python libraries is with `pip`. It comes with your python install.
Unfortunately the version that came packaged with python might be a little out of date. Not a problem.

Open command prompt **running as administrator** and run this command:
`python -m pip install --upgrade pip`

(python -m says "this is a python script")

While we're upgrading, let's also upgrade setuptools

`python -m pip install --upgrade setuptools`

And virtualenv (we'll want it later)

`python -m pip install virtualenv`

These packages will now be upgraded/installed globally across your entire system.

## Getting Git
[Install git for windows](https://git-scm.com/download/win). There are lots of ways to use git, but the command line gives you the most control
and the clearest read out. This is a prerequisite for checking out the project from github.

## Getting PyCharm Community Edition
[Install PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/#section=windows).
PyCharm is a great IDE with all sorts of useful stuff in it -- for us, git integration and support of
python virtual environments are probably the most important. If you have another IDE you want to use
that's up to you, but for the rest of this set up guide I'll assume you're using PyCharm.

## Setting up the project
Run PyCharm. From the start up dialog box, select `check out from version control`, and select github.
Enter your github credentials. On the next screen, use the project git URL (`https://github.com/animate-object/r-prime.git`)
for the 'repository url' field.

## Setting up a python virtual environment and getting tensorflow
A virtual environment is a way to easily and quickly install project specific dependencies (libraries we use 
in our project). A side benefit is that if you are working on multiple projects that use different versions
of the same library, you can run them both without a problem. Lots of reasons to use virtual environments. Trust me.

In case you don't have it yet, open up command prompt (as administrator) and run these commands:

`> python -m pip install virtualenv`

(if it's already installed, make sure you have the newest version)

`> python -m pip install --upgrade virtualenv`

Now navigate to your project directory in command prompt. When you're at the root of the project (`\r-prime`),
run the following commands:

`> virtualenv venv` -- sets up a virtualenv in a folder called `venv`

`> venv\Scripts\activate.bat` -- starts running the virtual environment

Your prompt should now have `(venv)` in front of it. Run:

`pip install -r requirements.txt` 
Requirements.txt is a file that specifies project requirements. You can see it in the project root directory.

Pip should start installing all of the project dependencies including numpy and tensorflow.

### Tell PyCharm about your virtual environment
One last step to make it easy to run python files in the app.

With the project open in PyCharm, go to file > settings > Project > Project Interpreter

From there selec the drop down menu and set the project interpreter to 
`3.5.2 virtualenv at C:\<your project path>\r-prime\venv`. You should see the list of installed
packages update to include, among other things TensorFlow and NumPy.

That's it. You're done! Hopefully
