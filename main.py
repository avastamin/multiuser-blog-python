
import webapp2
from handlers.handler import Handler
from handlers.mainhandler import MainHandler
from handlers.userhandler import SignupHandler
from handlers.userhandler import LoginHandler
from handlers.userhandler import LogoutHandler
from handlers.bloghandler import BlogPostHandler
from handlers.bloghandler import NewPostHandler
from handlers.bloghandler import EditPostHandler
from handlers.bloghandler import DeletePostHandler
from handlers.postmetahandler import LikeHandler
from handlers.postmetahandler import CommentHandler
from handlers.postmetahandler import EditCommentHandler
from handlers.postmetahandler import DeleteCommentHandler


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', MainHandler),
    ('/blog/([0-9]*)', BlogPostHandler),
    ('/blog/newpost', NewPostHandler),
    ('/blog/editpost/([0-9]*)', EditPostHandler),
    ('/blog/deletepost/([0-9]*)', DeletePostHandler),    
    ('/signup', SignupHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/like', LikeHandler),
    ('/comment', CommentHandler),    
    ('/commentedit', EditCommentHandler),
    ('/commentdelete', DeleteCommentHandler)
    
], debug=True)
