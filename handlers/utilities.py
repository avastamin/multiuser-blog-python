import hashlib
import re
import random
import string

from google.appengine.ext import db


class Utilities:
    # write pwd hashing functions
    @staticmethod
    def make_salt():
        return ''.join(random.choice(string.letters) for x in xrange(5))

    @staticmethod
    def make_pwd_hash(username, pwd, salt=None):
        if not salt:
            salt = Utilities.make_salt()
        h = hashlib.sha256(username + pwd + salt).hexdigest()
        return "%s|%s" % (h, salt)

    @staticmethod
    def is_valid_hash(username, pwd, h):
        l = h.split("|")
        if Utilities.make_pwd_hash(username, pwd, l[1]) == h:
            return True

    @staticmethod
    def make_cookie_val(username):
        SECRET = "iamsosecret"
        h = hashlib.sha256(SECRET + username).hexdigest()
        return "%s|%s" % (username, h)
    
    @staticmethod
    def valid_username(username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(username)

    @staticmethod
    def valid_password(password):
        PWD_RE = re.compile(r"^.{3,20}$")
        return PWD_RE.match(password)
        
    @staticmethod
    def valid_email(email):
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        return EMAIL_RE.match(email)
    
    @staticmethod
    def existing_user(username):
        # get all registered users from datastore
        users = db.GqlQuery("select * from Users")
        for user in users:
            if user.username == username:
                return True

    @staticmethod
    def valid_user(username, password):
        users = db.GqlQuery("select * from Users")
        for user in users:
            if user.username == username and Utilities.is_valid_hash(username, password, user.password_hash):
                return True
