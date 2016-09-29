from google.appengine.ext import db
import logging

from utilities import Utilities
from handler import Handler
from models.blogposts import BlogPosts

class MainHandler(Handler):
    """Get all blog posts and relevent comments and likes/dislikes"""
    def get(self, bpid = None):
        
        username = ""
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                username = l[0]
            
        if bpid:
            bp = BlogPosts.get_by_id(long(bpid))
            blogposts = list()
            blogposts.append(bp)
            # self.response.out.write(blogposts)
        else:
            blogposts = db.GqlQuery("select * from BlogPosts order by published desc")
        likes = []
        if username and len(username) > 0:
            # get all the posts that this user has liked
            userlikes = db.GqlQuery("select * from Likes where username = :1", username)
            for userlike in userlikes:
                likes.append(str(userlike.blogid))
            logging.info("likes: " + str(likes))
            #self.response.headers.add_header('set-cookie', str('user_id=%s' % make_cookie_val(username)))
        self.render("blogs.html", username = username, blogposts = blogposts, likedposts = likes)

    #6333186975989760
    def post(self):
        self.response.out.write(self.request)
