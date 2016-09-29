from google.appengine.ext import db


class Comments(db.Model):
    blogid = db.StringProperty(required = True)
    comment = db.TextProperty(required = True)
    commenter = db.StringProperty(required = True)
    added = db.DateTimeProperty(auto_now = True)
