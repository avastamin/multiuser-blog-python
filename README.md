#multiuser blog in python
A simple blog created using Bootstrap, jQuery, Python (webapp2, jinja2) hosted on Google App Engine

This is a multiuser blog application where users can read blogs. Signed in users can edit/delete their own posts, write/edit/delete comments and like others' posts. The project structure is as follows:
- app.yaml 
- main.py
- /handlers
     - all of the *handler.py files which provide the server side logic for the features
- /models
     - all of the db.Model classes (Users, BlogPosts, Comments, Likes) which form the database model
- /templates
     - the template html files which get rendered in the browser by the application 
- /static/css
     - the stylesheets for the html files
- /static/js
     - the javascript/jQuery logic that is implemented on the client side

To run this project on your local system:

1. Make sure that you have Google App Engine SDK setup on your system

2. Download the folder structure as is and run the following commands in Terminal.
  - export PATH=$PATH:/path/to/google_appengine
  - dev_appserver.py app.yaml

3. Navigate to http://localhost:[port]

Alternatively, click through to this link: http://blog-144709.appspot.com or http://blog-144709.appspot.com/blog

