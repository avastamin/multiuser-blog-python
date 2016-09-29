from google.appengine.ext import db


class BlogPosts(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    author = db.StringProperty(required = True)
    published = db.DateTimeProperty(auto_now_add = True)
    # permalink = db.StringProperty(required = True)
    likes = db.IntegerProperty(default=0)
    comments = db.IntegerProperty(default=0)