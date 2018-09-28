from flask import Flask, request, render_template, redirect, url_for
import re

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template("signup.html")

def is_empty(val):
  if val == "":
      return True
  else:
    return False

def has_whitespace(val):
  if " " in val:
    return True
  else:
    return False

def validate_email(val):
    valid_email = re.compile("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$")
    if valid_email.match(val):
        return True
    else:
        return False


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form['username']  # grabs user data from form field "username"
    password = request.form['password']  # grabs user data from form field "password"
    verify_password = request.form['verify_password']  # grabs user data from form field "verify"
    email = request.form['email'] # grabs user data from form field "email"

    # create variable(s) to hold error message for the following fields
    username_error = "" 
    password_error = ""  
    verify_error = ""  
    email_error = "" 

    # username error checking
    if is_empty(username):
        username_error = "This field cannot be empty"
        username = ""
    else:
        username_len = len(username)
        if username_len > 20 or username_len < 3:
           username_error = "Username must be between 3 and 20 characters"
           username = ""
        else:
          if has_whitespace(username):
             username_error = "Spaces are not allowed"
             username = ""

    # password error checking
    if is_empty(password):
        password_error = "This field cannot be empty"
        password = ""
    else:
        password_len = len(password)
        if password_len > 20 or password_len < 3:
          password_error = "Password must be between 3 and 20 characters"
          password = ""
        else:
          if has_whitespace(password):
            password_error = "Spaces are not allowed"
            password = ""

    # verify password error checking
    if is_empty(verify_password):
        verify_error = "This field cannot be empty"
        verify_password = ""
    else:
        if verify_password != password:
            verify_error = "Passwords must match"
            verify_password = ""

    # email error checking
    if not is_empty(email):
        email_len = len(email)
        if  email_len > 20 or email_len < 3:
            email_error = "Email must be between 3 and 20 characters"
            email = ""
        else:
          if not validate_email(email):
            email_error = "Not a valid email"
            email = ""

    if not username_error and not password_error and not verify_error and not email_error: # no error msgs, return welcome page
            return render_template("welcome.html", username=username)
    else:
        return render_template ("signup.html",
        username_input=username,
        email_input=email,
        username_error=username_error, password_error=password_error, verify_error=verify_error, email_error=email_error)

app.run()