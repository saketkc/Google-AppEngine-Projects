import gdata.calendar.service
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom
import time
import simplejson as json
import datetime
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail
email = "ugacads.iitb@gmail.com"
password = "fedora13"
source = "ugacads-calendar"
academic = "http://www.google.com/calendar/feeds/kq47jpfc8ell2b240i5evuqlio@group.calendar.google.com/private/full"
acad_id = "kq47jpfc8ell2b240i5evuqlio@group.calendar.google.com"

cult = "http://www.google.com/calendar/feeds/ml8manl0cc1lp2d6r867fu74tk@group.calendar.google.com/private/full"
cult_id = "ml8manl0cc1lp2d6r867fu74tk@group.calendar.google.com"
hostel = "http://www.google.com/calendar/feeds/3903h5a6o85l9l84lveg61dvbo@group.calendar.google.com/private/full"
hostel_id = "3903h5a6o85l9l84lveg61dvbo@group.calendar.google.com"
sports = "http://www.google.com/calendar/feeds/4d0c12953h02ur7rkuumhuktu8@group.calendar.google.com/private/full"
sports_id = "4d0c12953h02ur7rkuumhuktu8@group.calendar.google.com"
tech = "http://www.google.com/calendar/feeds/qcisaissdqkbgteubkr0ibgvoc@group.calendar.google.com/private/full"
tech_id = "qcisaissdqkbgteubkr0ibgvoc@group.calendar.google.com"
all_list= {"acad":acad_id,"cult":cult_id,"sports":sports_id,"hostel":hostel_id,"tech":tech_id}
def FetchEvent(start_date,end_date):
	cal_client = gdata.calendar.service.CalendarService()
	cal_client.email = email
	cal_client.password = password
	cal_client.source = 'Google-Calendar_Python_Sample-1.0'
	cal_client.ProgrammaticLogin()
	calfeed = cal_client.GetOwnCalendarsFeed()
	all_events = "Gymkhana Bot | Events in the next 24 hours ......................"
	calurl=[a_calendar.content.src for i, a_calendar in enumerate(calfeed.entry)]
	for key in all_list.keys():
		value = str(all_list[key])
		query = gdata.calendar.service.CalendarEventQuery(str(value), 'private', 'full')
		query.start_min = start_date
		query.start_max = end_date
		feed = cal_client.CalendarQuery(query)
		length = len(feed.entry)
		if length>1:
			all_events  = all_events + " || ["+ str(key).capitalize() +"]: " #  str(calurl[1])
		count=0
	#return try_Try_Except_Finally_events
		for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
			count = count+1

			all_events = all_events + str(i+1) + ". " +  str(an_event.title.text)
			for a_when in an_event.when:
				#2012-10-18T19:00:00.000+05:30
		        	all_events += " :: " + time.strftime("%d %b %Y %H-%M",time.strptime(a_when.start_time,"%Y-%m-%dT%H:%M:%S.000+05:30"))
			        all_events += " - " + time.strftime("%d %b %Y %H-%M",time.strptime(a_when.end_time,"%Y-%m-%dT%H:%M:%S.000+05:30"))  
		#all_events+= "[/"+str(key).capitalize()+"]"
		if count ==0:
			all_events +="- "
	all_events+="Details: http://gymkhana.iitb.ac.in/"
	return all_events

def InsertEvent(title='Tennis with Beth', content='Meet for a quick lesson', where='On the courts', start_time=None, end_time=None,category=None, recurrence_data=None):
    event = gdata.calendar.data.CalendarEventEntry()
    event.title = atom.data.Title(text=title)
    event.content = atom.data.Content(text=content)
    event.where.append(gdata.data.Where(value=where))
    if recurrence_data is not None:
        # Set a recurring event
        event.recurrence = gdata.data.Recurrence(text=recurrence_data)
    else:
        if start_time is None:
            start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
            end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',time.gmtime(time.time() + 3600))

        event.when.append(gdata.data.When(start=start_time, end=end_time))
    cal_client = gdata.calendar.client.CalendarClient(source='Google-Calendar_Python_Sample-1.0')
    cal_client.ClientLogin(email, password, source)
    if category=="acads":
		new_event = cal_client.InsertEvent(event,academic)
    elif category =="sports":
		new_event = cal_client.InsertEvent(event,sports)
    elif category == "tech":
		new_event = cal_client.InsertEvent(event,tech)
    elif category == "hostel":
		new_event = cal_client.InsertEvent(event,hostel)
    elif category == "cult":
		new_event = cal_client.InsertEvent(event,cult)
    else :
		new_event = cal_client.InsertEvent(event)



    return new_event
def send_mail(addresses,query):
    mail.send_mail(sender="UG Acads IIT Bombay <ugacads.iitb@gmail.com>",
                         to="saketkc@gmail.com",
                         subject="UG Acads",
                         body="""Test Messge""")

class MainPage(webapp.RequestHandler):
    def get(self):
        category = self.request.get("category")
        start_date = self.request.get('start_date')
        start_date_split = start_date.split('-')
        start_year = int(start_date_split[2])
        start_month = int(start_date_split[1])
        start_date_date = int(start_date_split[0])

        end_date = self.request.get('end_date')
        end_date_split = end_date.split('-')
        end_year = int(end_date_split[2])
        end_month = int(end_date_split[1])
        end_date_date = int(end_date_split[0])

        end_time = self.request.get('end_time')
        end_time_split = end_time.split('-')
        end_hour = int(end_time_split[0])
        end_minute = int(end_time_split[1])
        end_second = 00 #int(end_time_split[2])


        start_time = self.request.get('start_time')
        start_time_split = start_time.split('-')
        start_hour = int(start_time_split[0])
        start_minute = int(start_time_split[1])
        start_second = 00#int(start_time_split[2])
        event_start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000+05:30', datetime.datetime(start_year,start_month,start_date_date,start_hour,start_minute,start_second).timetuple())
        event_end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000+05:30', datetime.datetime(end_year,end_month,end_date_date,end_hour,end_minute,end_second).timetuple())

        title = self.request.get('title')
        description = self.request.get('description')
        location = self.request.get('location')
        cal_event = InsertEvent(title=title, content=description, where=location,start_time=event_start_time,end_time=event_end_time,category=category)
        edit_event=cal_event.GetEditLink()
        my_response = {"edit_event":edit_event.href,"type":"success"}
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(my_response))



    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(self.request.get('testparam'))
class DeleteCalEvent(webapp.RequestHandler):
	def post(self):
		event_link = self.request.get('event_link')
    		cal_client = gdata.calendar.client.CalendarClient(source='Google-Calendar_Python_Sample-1.0')
		cal_client.ClientLogin(email, password, source)
		cal_client.Delete(event_link,force=True)
		self.response.headers['Content-Type']='text/plain'
		self.response.out.write("dsadAS")


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
        message = mail.EmailMessage(sender="IITB UG Academic Council <saketkc@gmail.com>",
                            subject=subject)
        message.to = send_to
        message.cc = "gsecaaug@iitb.ac.in"
        message.bcc = "ishanshrivastava1@gmail.com"


        message.body = body
        message.html = htmlbody
        message.send()
        #send_mail("test","query")

class FetchCalendar(webapp.RequestHandler):
	def get(self):
		start_date = self.request.get('start')
		end_date = self.request.get('end')
		events = FetchEvent(start_date,end_date)
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write(events)

application = webapp.WSGIApplication(
                                     [('/', MainPage),('/mail',SendMail),('/fetch',FetchCalendar),('/delete',DeleteCalEvent)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()