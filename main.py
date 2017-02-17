import webapp2
import re

def end(tag):
    ret = "</" + tag[1:]
    return ret

def bd(tag,br,typ):
    ret = tag[:(len(tag) - 1)] + " " + br + "='" + typ + "'/>"
    return ret

def pg(un,em,fb1,fb2,fb3,fb4):

    i = "<input>"
    iny = end(i)
    t = "<td>"
    tn = end(t)
    r = "<tr>"
    rn = end(r)
    l = "<label>"
    ln = end(l)

    tb = r + t
    tm = tn + t
    te = tn + rn
    lr = iny + bd(l,"style","color:red")

    content = ("<body>" +
               "<p style='font-size:40'>Signup</p>" +
               "<form method='post'>" +
               "<table>" +
               tb + "Username: " + tm + "<input name='usnm' value='" + un + "'/>" + lr + fb1 + ln + te +
               tb + "Password: " + tm + bd(i, "name", "pswd' type='password") + lr + fb2 + ln + te +
               tb + "Verify Password: " + tm + bd(i, "name", "vrfy' type='password") + lr + fb3 + ln + te +
               tb + "Email (Optional): " + tm + "<input name='eml' value='" + em + "'/>" + lr + fb4 + ln + te +
               tb + bd(i, "type", "submit") +
               "</table>" +
               "</form>" +
               "</body>")

    return content


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_pass(password):
    return PASS_RE.match(password)

def valid_email(eml):
    return PASS_RE.match(eml)


class MainHandler(webapp2.RequestHandler):
    def get(self):

        content = pg("","","","","","")

        self.response.write(content)

    def post(self):
        username = self.request.get("usnm")
        password = self.request.get("pswd")
        verif = self.request.get("vrfy")
        emaily = self.request.get("eml")

        error = False
        fb1 = ""
        fb2 = ""
        fb3 = ""
        fb4 = ""

        if not valid_username(username):
            error = True
            fb1 = "Not a valid username!"

        if not valid_pass(password):
            error = True
            fb2 = "Not a valid password"

        if verif != password:
            error = True
            fb3 = "Passwords do not match"

        if emaily != "" and not valid_email(emaily):
            error = True
            fb4 = "Not a valid email"

        if error:
            content = pg(username,emaily,fb1,fb2,fb3,fb4)
            self.response.write(content)
        else:
            self.redirect("welcome?usernm=" + str(username))

class welcompage(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("usernm")
        self.response.write("Welcome " + username + "!")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome',welcompage)
], debug=True)
