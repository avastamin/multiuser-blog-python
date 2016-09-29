from handlers.utilities import Utilities
from handlers.handler import Handler
from models.users import Users

class SignupHandler(Handler):
    """Signup handler to create new user to the site"""
    def get(self):
        self.render("register.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
 
        if not Utilities.valid_username(username):
            username_error = "That isn't a valid username."
            self.render("register.html", username = username, email = email, error_message = username_error)
 
        # Add code here to check for pre-existing username
        # and give message that User already exists.
        elif Utilities.existing_user(username):
            username_error = "That user already exists."
            self.render("register.html", username = username,  email = email,error_message = username_error)
        
        elif not Utilities.valid_password(password) or password == "":
            pwd_error = "That wasn't a valid password."
            self.render("register.html", username = username,  email = email,error_message = pwd_error)
        
        elif password <> verify:
            verify_error = "Passwords didn't match."
            self.render("register.html", username = username,  email = email,error_message = verify_error)

        elif email <> "" and not Utilities.valid_email(email):
            email_error = "That isn't a valid email."
            self.render("register.html", username = username,  email = email,error_message = email_error)
        

        # else, store username, hash of pwd, email, signupdate in DataStore
        # and redirect user to welcome page 
        else:
            
            user = Users(username = username, password_hash = Utilities.make_pwd_hash(username, password), email = email)
            user.put()
            self.response.headers.add_header('set-cookie', str('user_id=%s' % Utilities.make_cookie_val(username)))
            self.redirect('/blog')

class LoginHandler(Handler):
    """Login handler to login"""
    def get(self):
        self.render("login.html")

    def post(self):
        # verify login name and password from datastore.
        username = self.request.get("username")
        password = self.request.get("password")
        if username and password and Utilities.valid_username(username) and Utilities.valid_password(password) and Utilities.valid_user(username, password):
            self.response.headers.add_header('set-cookie', str('user_id=%s' % Utilities.make_cookie_val(username)))
            self.redirect('/blog')
        else:
            self.render("login.html", error_message = "Invalid login.")

class LogoutHandler(Handler):
    """logout handler to logout from the site"""
    def get(self):
        self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
        self.redirect('/blog')
