from google.appengine.ext import db
import json
import logging
from datetime import datetime

from handler import Handler
from utilities import Utilities
from models.blogposts import BlogPosts
from models.likes import Likes
from models.comments import Comments



class CommentHandler(Handler):
    """Add new Comment"""
    @db.transactional(xg=True)
    def insertCommentAndInc(self, bp, newcomment):
        bp.comments += 1
        bp.put()
        newcomment.put()
        return newcomment.added, bp.comments, newcomment.key().id()

    def post(self):
        logging.info(self.request.body)
        data = json.loads(self.request.body)
        # need blog to increment number of posts
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                logging.info(user_id + " " + l[0])
                bp = BlogPosts.get_by_id(long(data['blogid']))
                # new Comment to add to data store
                newcomment = Comments(blogid = str(data['blogid']), comment = data['comment'], commenter = data['username'])
                added, count, commentid = self.insertCommentAndInc(bp, newcomment)
                addedstr = datetime.strftime(added, '%b %d,  %Y %I:%M %p')
                self.response.out.write(json.dumps(({'added': str(addedstr), 'comments': count, "commentid" : commentid })))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')

class EditCommentHandler(Handler):
    """Edit comment if user has permission to do that"""
    def post(self):
        logging.info(self.request.body)
        data = json.loads(self.request.body)
        # Get the comment from data store
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                c = Comments.get_by_id(long(data['commentid']))
                c.comment = data['updatedcomment']
                c.put()
                self.response.out.write(json.dumps(({"added": datetime.strftime(c.added, '%b %d,  %Y %I:%M %p')})))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')

class DeleteCommentHandler(Handler):
    """Edit comment if user has permission to do that"""
    @db.transactional(xg=True)
    def deleteCommentInDB(self, c, bp):
        bp.comments = bp.comments - 1
        bp.put()
        db.delete(c)
        return bp.comments

    def post(self):
        logging.info(self.request.body)
        data = json.loads(self.request.body)
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                # Get the comment from data store
                c = Comments.get_by_id(long(data['commentid']))
                blogid = c.blogid
                # and the blogpost itself
                bp = BlogPosts.get_by_id(long(blogid))
                commentsnum = self.deleteCommentInDB(c,bp)
                self.response.out.write(json.dumps(({'blogid': str(blogid), 'commentsnum': commentsnum})))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')

class LikeHandler(Handler):
    """Like handler to count/add/remove likes on pages"""
    @db.transactional(xg=True)
    def updateDB(self, bp, blogid, username, change, like=None, deletelikes=None):
        bp.likes = bp.likes + change
        bp.put()
        if change == 1 and like:
            like.put()
        if change == -1 and deletelikes:
            db.delete(deletelikes)

        return bp.likes

    def post(self):
        logging.info(self.request.body)
        data = json.loads(self.request.body)

        # Need blog ID to update # of likes
        # Need username so you don't like a post more than once
        # Like or unlike flag
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                bp = BlogPosts.get_by_id(long(data['blogid']))
                if (data['todo'] == "like"):
                    # Create a row in Likes for this user and blog combo
                    like = Likes(blogid=data['blogid'], username=data['username'])
                    # Add it to datastore and inc like count
                    count = self.updateDB(bp, data['blogid'], data['username'], 1, like=like)
                    # self.response.out.write(json.dumps(({'likes': bp.likes})))

                if (data['todo'] == "unlike"):
                    # Delete the entry  for this user and blog combo from Likes
                    gqd = db.GqlQuery("select * from Likes where blogid = :1 and username = :2", data['blogid'],
                                      data['username'])
                    deletelikes = gqd.get()
                    count = self.updateDB(bp, data['blogid'], data['username'], -1, deletelikes=deletelikes)
                self.response.out.write(json.dumps(({'likes': count})))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
            self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
            self.render("login.html", permission_error_message="You need to login to do this")
