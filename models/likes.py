from google.appengine.ext import db

class Likes(db.Model):
    blogid = db.StringProperty(required = True)
    username = db.StringProperty(required = True)
