import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail
class Users(db.Model):
    username = db.StringProperty()
    useremail = db.StringProperty(multiline=True)
    slideshow_id = db.IntegerProperty()
    slideshow_uploaded_at = db.DateTimeProperty()
    last_checked_at = db.DateTimeProperty(auto_now_add=True)
    to_be_scanned = db.BooleanProperty()
    

def api_key(api_key=None):
    return db.Key.from_path('Api', api_key or 'default_api')

def send_mail(addresses,query):
    mail.send_mail(sender="UG Acads IIT Bombay <ugacads.iitb@gmail.com>",
                         to="saketkc@gmail.com",
                         subject="UG Acads",
                         body="""Test Messge""")
    
class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')
        users = db.GqlQuery("SELECT * FROM Users ")
        self.response.out.write('Hello, webapp Worldsdfsssssss!')
        for user in users:
            if user.username:
                self.response.out.write('<b>%s</b> wrote:' % user.username)
            else:
                self.response.out.write('An anonymous person wrote:')
                self.response.out.write('<blockquote>%s</blockquote>' % cgi.escape(user.useremail))
        
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(self.request.get('testparam'))
        users = Users()
        users.username = "test"
        users.useremail = "DE"
        users.put()
        print self.request.get('testparam')


class SendMail(webapp.RequestHandler):
    def get(self):
        send_to = str(self.request.get('ldap_id'))+"@iitb.ac.in"
        subject = str("[UG-ACADS]: Request ID #")+ str(self.request.get('request_id'))
        fullname = str(self.request.get('fullname'))
        department = str(self.request.get('department'))
        request_type = str(self.request.get('request_type'))
        query_text = str(self.request.get('query_text'))
        body = """Dear """+ fullname +""", \r\n <br/>
 <br/>       Your request has been received. \r\n <br/><br/> The details are as follows:
        <br/><br/><strong>Department:</strong> """+ department +"""\r\n <br/><br/><strong>Request Type: </strong>""" + request_type +"""\n<br/><br/> <strong>Query:</strong> """+ str(self.request.get('query_text'))
        htmlbody = """<html>Dear <strong> """+ fullname +"""</strong>, \r\n<br/><br/>
        <br/><br/>Your request has been received. \r\n<br/><br/>The details are as follows:
        <br/><br/><strong>Department:</strong> """+ department +"""\n<br/><br/> <strong>Request Type:</strong>""" + request_type +"""\n<br/><br/><strong>Query:</strong> """+ str(self.request.get('query_text'))+"""</html>"""
        message = mail.EmailMessage(sender="IITB UG Academic Council <ugacads.iitb@gmail.com>",
                            subject=subject)
        message.to = send_to
        if department=="AERO":
			message.cc = "amitmangtani.iitb@gmail.com"
        elif department=="CHEM":
            message.cc="annuganeriwala@gmail.com"
        elif department=="MET":
            message.cc="siddharth.bhandari02@gmail.com"
        elif department=="PHY":
            message.cc ="souvik.iitb09@gmail.com"
        elif deparment=="ME":
            message.cc="ajinkya.latkar@gmail.com"
        elif department=="CHE":
            message.cc="himanshu.malhotra1990@gmail.com"
        elif department=="CSE":
            message.cc="gagrani.vinayak@gmail.com"
        elif department=="CIVIL":
            message.cc="jaymin.k.iitian@gmail.com"
        elif department=="ESE":
            message.cc="neeraj2791@gmail.com"
        elif department=="EE":
            message.cc="amit.iitb.17@gmail.com"
        else:
            message.cc = "gsecaaug@iitb.ac.in"
        message.bcc = "ishanshrivastava1@gmail.com"
        
        
        message.body = body
        message.html = htmlbody
        message.send()
        #send_mail("test","query")
        
        
application = webapp.WSGIApplication(
                                     [('/', MainPage),('/mail',SendMail),],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
