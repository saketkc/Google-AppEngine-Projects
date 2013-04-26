import datetime
import wsgiref.handlers
import httplib2
from google.appengine.api import xmpp
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import xmpp_handlers
import urllib2
from google.appengine.api import urlfetch



from apiclient.discovery import build
from google.appengine.api import memcache
#from google.appengine.ext.webapp import template
#from google.appengine.ext.webapp.util import run_wsgi_app
from oauth2client.appengine import AppAssertionCredentials
def get_calendar_events(start=None):
    if not start:
        now = datetime.datetime.now()
        future = now+datetime.timedelta(1)
        start = now.strftime("%Y-%m-%d")
        end = future.strftime("%Y-%m-%d")
    else:
        now = start
        future = now+datetime.timedelta(1)
        start = now.strftime("%Y-%m-%d")
        end = future.strftime("%Y-%m-%d")

    url = "http://ugacads-calendar.appspot.com/fetch?start="+start+"&end="+end
    req = urlfetch.fetch(url=url)
    events = req.content

    return events
def courses_command(text):
    url = "http://home.iitb.ac.in/~saket.kumar/2.php?param1=courses"
    url+="&param2="+str(text)
    req=urlfetch.fetch(url=url)
    return req.content

def user_exists(email):
    users = db.GqlQuery("SELECT * FROM Users ")
    i=0
    for user in users:
        i=i+1
    if (i>1):
        return True
    else:
        return False

def ask_for_registration(message,gmail_username):
    message.reply("Enter /register <ldap_id> <ldap_password> for registering")
    message.reply("Enter /skip to skip it for now. LDAP registration can be done later")

class ShortLink(db.Model):
    url = db.TextProperty(required=True)


class Users(db.Model):
    email = db.StringProperty()
    #datejoined = db.DateTimeProperty(auto_now_add=True)
    #ldap_id = db.TextProperty()
    #ldap_password = db.TextProperty()
    #should_be_asked_for_registration = db.BooleanProperty(default=True)
    #@property
    #def name(self):
     #   return self.key().name()


class UpdatePage(webapp.RequestHandler):
    def get(self):
        #tt= str(datetime.time(datetime.now()))
        status = get_calendar_events()
	xmpp.send_message("aardvark@jabber.org", "updatestatus @@"+str(status))

        #sender = self.request.get('from'.)split('/')[0]
        #xmpp.send_presence()
        #users = db.GqlQuery("SELECT * FROM Users ")
        #for user in users:
        #    xmpp.send_presence(user.email, status=status)


class PingMessage(webapp.RequestHandler):
    def post(self):
        status = get_calendar_events()
        #xmpp.send_presence("saketkc@gmail.com", status=tt)
        sender = self.request.get('from').split('/')[0]
        xmpp.send_presence(sender, status=status)

class Subscription(webapp.RequestHandler):
    def post(self):
        #sender = self.request.get('from').split('/')[0]
        status = get_calendar_events()
        #xmpp.send_presence("saketkc@gmail.com", status=tt)
        sender = self.request.get('from').split('/')[0]
        xmpp.send_presence(sender, status=status)
        user = Users()
        user.email = sender
        user.put()

class XmppHandler(xmpp_handlers.CommandHandler):
    def events_command(self,message=None):
        now=datetime.datetime.now()
        events = get_calendar_events(start=now)
        message.reply(events)
    def search_command(self,message=None):
        credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/urlshortener')
        http = credentials.authorize(httplib2.Http(memcache))
        service = build("urlshortener", "v1", http=http)
        credentials.refresh(http)
        long_url = message.arg
        url="http://gymkhana.iitb.ac.in/~ugacademics/wiki/index.php?search="+long_url+"&go=Go&title=Special%3ASearch"



        shortened = service.url().insert(body={"longUrl": url}).execute()
        shortened1 = service.url().list().execute()

        message.reply( str(shortened1["items"][0]['id']))




    def gstats_command(self,message=None):
        user = message.sender.split('/')[0]
        gmail_username = user.split('@')[0]
        exists = user_exists(gmail_username)
        if not (user_exists):
            ask_for_registration(message,gmail_username)
        else:
            msg = message.arg

	split_msg = msg.split(" ")
	if len(split_msg)<3:
		message.reply("Insufficient parameters")
	else:

		dept = split_msg[0]
		year = split_msg[1]
		code = split_msg[2]
		url = "http://home.iitb.ac.in/~pushkar.godbole/2.php?param1="
		url+="gstats"+"&param2="+dept+"&param3="+year+ "&param4="+code
		response = urllib2.urlopen(url)
		the_page = response.read()
	        message.reply(the_page)
        	#mail.send_mail(sender="UG Acads IIT Bombay <saketkc@gmail.com>",
			 #            to="saketkc@gmail.com",
			  #           subject="UG Acads",
			   #          body="""Test Messge""")

    def text_message(self,message=None):
        user = message.sender.split('/')[0]
	#jids="saketkc@gmail.com"
	#xmpp.send_message(jids, "body")
        #message.reply(message.sender)

def main():
    app = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XmppHandler),('/_ah/xmpp/presence/available/', PingMessage),('/update',UpdatePage)], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__== '__main__':
    main()



