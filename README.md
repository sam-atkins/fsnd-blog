# Build a Blog Project

## About this project
This project is part of my **Udacity FullStack NanoDegree**. The scope is to build a blog that meets the following:

### User Requirements

* Front page that lists entries [v1]
* Form to submit new entries [v1]
* Permalink page for entries [v1]
* User sign-up [v2]
* User log-in [v2]
* User log-out [v2]
* Users can comment on posts [v3]
* Users can edit/delete their own comments [v3]
* Users can like/unlike posts [v3]
* Authors can edit/delete their own posts [v3]

### Build Requirements

* Python
* Framework: Google App Engine and Datastore
* Jinja2 templates

### Status

* Version 1 and 2: Complete
* Version 3: Live and submitted for Udacity review (see demo link below)

### Demo
Live at [app.spot](https://cubiio-blog.appspot.com/).

## How to install and run

**macOS instructions:**

* `cd` to the project folder e.g. `projects/fsnd-blog`
* In the command line run `$ dev_appserver.py .` (Or run my ohmyzsh alias = `dev`)
* The app will load in http://localhost:8080
* To view the local datastore: http://localhost:8000/datastore
* To deploy, use the command line: `gcloud app deploy`

Prerequisites are: Python (2.7) and Google Cloud SDK. 

**Google Cloud links:**
* [SDK Documentation](https://cloud.google.com/sdk/docs/) 
* [Quickstart for Python App Engine Standard Environment](https://cloud.google.com/appengine/docs/python/quickstart)


## Project Structure
A few words on the project/repo structure. The structure is based on best practices (source: several articles on Python best practices [link](https://airbrake.io/blog/python/python-best-practices), [link](https://stackoverflow.com/questions/48458/project-structure-for-google-app-engine), [link](https://sites.google.com/site/io/rapid-development-with-python-django-and-google-app-engine) and [link](https://vladcalin.github.io/what-every-python-project-should-have.html)).

To recap (remind myself when coming back to this later on), here's what it means:

```
/project_root
	/env 
	/myapp
		/handlers
		/models
		/tools
	/static
	/templates
	.gitignore
	LICENSE.txt
	README.md
	app.yaml
	main.py
	requirements.txt
```

Let's look at each of these in detail.

**/env**

Virtual environment for managing Python packages and dependencies. Include `env` in your gitignore file.

**/myapp**

Includes the following:

* `__init__.py` - This file can be empty and basically enables files to be importred. For a more detailed and techical explanation, read [this](https://stackoverflow.com/questions/448271/what-is-init-py-for#448279) and [this](https://docs.python.org/3/tutorial/modules.html#packages).
* `/models` - This includes Model classes i.e. all database related stuff split into modules e.g. `user.py`.
* `/views` - This includes all the handlers, split into modules e.g. `basehandler.py` and `editpost.py`.
* `/tools` - This includes decorators and all helper functions.
* I also include other helper function files in this folder.

**/static**

This includes all static files, for this project it is only CSS style sheets but for other projects separate sub-folders for images and javascript could be included.

**/templates**

All Jinja HTML templates are included in here.

**Project files in the root directory**

* `app.yaml` - This is needed for Google App Engine (GAE).
* `main.py` - In the case of GAE, this file includes the app start info, i.e. `webapp2.WSGIApplication` and the routing info for page to view handler.

**Documentation**

All good projects should include a license and a readme.

**Chore files**

* The `.gitignore` helps to manage git and so only the files you want are pushed to your remote (Github in this case).
* A `requirements.txt` allows someone else to quickly understand what packages (and versions) are required to install/run the project on a different machine.

