from google.appengine.ext import db
import logging
import json
from utilities import Utilities
from handler import Handler
from models.blogposts import BlogPosts

class BlogPostHandler(Handler):
    """Get all blog posts and relevent comments and likes/dislikes"""
    def get(self, bpid):        
        username = ""
        user_id = self.request.cookies.get("user_id")
        if user_id:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                username = l[0]
        bp = BlogPosts.get_by_id(long(bpid))
        likedposts = []
        if username and len(username) > 0:
            #self.response.headers.add_header('set-cookie', str('user_id=%s' % make_cookie_val(username)))
            gql = db.GqlQuery("select * from Likes where blogid = :1 and username = :2" , bpid, username)
            if gql.fetch(1):
                likedposts.append(bpid)
        # Get all comments for this blog post
        comments = db.GqlQuery("Select * from Comments where blogid = :1 order by added desc", bpid)

        self.render("blogpost.html", username = username, blogpost = bp, likedposts = likedposts, comments = comments)

    #6333186975989760
    def post(self):
        self.response.out.write(self.request)


class NewPostHandler(Handler):
    """Create New blog post"""
    def get(self):
        username = ""
        user_id = self.request.cookies.get("user_id")
        if user_id > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                username = l[0]
                # self.response.headers.add_header('set-cookie', str('user_id=%s' % make_cookie_val(username)))
                self.render("newpost.html", username=username)
            else:
                self.redirect("/blog")
        else:
            self.redirect("/blog")

    def post(self):
        user_id = self.request.cookies.get("user_id")
        if user_id:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                username = l[0]
                subject = self.request.get("subject")
                content = self.request.get("content")
                if not subject or not content:
                    error_msg = "Both Subject and Content are required."
                    self.render("newpost.html", username=username, error_msg=error_msg, content=content,
                                subject=subject)
                else:
                    # Add a new blog post to data store and publish the permalink with /blog/[NUMBER] where NUMBER is obj.key().id()
                    bp = BlogPosts(subject=subject, content=content, author=username)  # , permalink = "/blog/")
                    # bpkey = bp.put()
                    # bp = db.get(bpkey)
                    # # bp.permalink = "/blog/"+str(bpkey.id())
                    bp.put()
                    self.redirect("/blog/" + str(bp.key().id()))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')


class EditPostHandler(Handler):
    """Edit single blog post"""
    def get(self, bpid):
        username = ""
        user_id = self.request.cookies.get("user_id")
        if user_id:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                username = l[0]
                # self.response.headers.add_header('set-cookie', str('user_id=%s' % make_cookie_val(username)))
                bp = BlogPosts.get_by_id(long(bpid))

                self.render("editpost.html", username=username, subject=bp.subject, contents=bp.content,
                            blogid=str(bpid))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
            self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
            self.redirect('/blog')

    def post(self, bpid):
        user_id = self.request.cookies.get("user_id")
        if user_id:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                username = l[0]
                subject = self.request.get("subject")
                content = self.request.get("content")
                if not subject or not content:
                    error_msg = "Both Subject and Content are required."
                    self.render("newpost.html", username=username, error_msg=error_msg, content=content,
                                subject=subject)
                else:
                    # Update the blog post in data store and publish the permalink with /blog/[NUMBER] where NUMBER is obj.key().id()
                    bp = BlogPosts.get_by_id(long(bpid))
                    bp.subject = subject
                    bp.content = content
                    bp.put()
                    self.redirect("/blog/" + str(bp.key().id()))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
            self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
            self.redirect('/blog')
class DeletePostHandler(Handler):
    """Delete single blog post"""
    @db.transactional(xg=True)
    def deletePostInDB(self, c, l, bp):
        logging.info("in deletePostInDB")
        if c:
            db.delete(c)
            logging.info("in deletePostInDB del c")

        if l:
            db.delete(l)
            logging.info("in deletePostInDB del l")

        db.delete(bp)
        logging.info("in deletePostInDB del bp")
        return True

    def post(self, blogid):
        logging.info("post del")
        user_id = self.request.cookies.get("user_id")
        if user_id:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                # Get the comments from data store
                cq = db.GqlQuery("select * from Comments where blogid = :1", blogid)
                c = cq.get()
                # and the likes
                lq = db.GqlQuery("select * from Likes where blogid = :1", blogid)
                l = lq.get()
                # and the blogpost itself
                bp = BlogPosts.get_by_id(long(blogid))
                if self.deletePostInDB(c, l, bp):
                    self.response.out.write(json.dumps(({'delete': "success"})))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
