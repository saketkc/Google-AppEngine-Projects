import cgi
import datetime
import time
import sha
import sys
import urllib
import wsgiref.handlers
import urllib2
import datetime
from google.appengine.api import urlfetch
from BeautifulSoup.BeautifulSoup import BeautifulSoup as BS
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail
def send_mail(send_to="saketkc@gmail.com",body="test",slideshow_id="1213"):
    message = mail.EmailMessage(sender="Connexions OERPUB <saketkc@gmail.com>",
                            subject="Slideshow Converted")
    message.to = send_to
    #message.cc = "saketkc@gmail.com"
    message.html = body
    message.send()
    #mail.send_mail(sender="Connexions <saketkc@gmail.com>",
     #                    to="saketkc@gmail.com",
     #                    subject="Your SlideShow Conversion is now Completed ",
     #                    body="""Your slideshow id """+ slideshow_id+""" has been upladed""")
    
class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('<script language="JavaScript" src="/js/thumbs.js">')
        self.response.out.write('</script>');
        self.response.out.write(""" <html>
            <body>
              <form action="/search" method="get">
              <table>
                <tr>
					<td><label>Date</label></td>
					<td><input type="text" name="date"></td>
				</tr>
				<tr> 
					<td><label>From </label></td>
					<td><input type="text" name="from"></td>
				</tr>
				
				<tr> 
					<td><label>To </label></td>
					<td><input type="text" name="to"></td>
				</tr>
                
                </table>
                <div><input type="submit" value="Fire"></div>
              </form>
            </body>
          </html>""")
         
        
        
        
        

class SlideSharePage(webapp.RequestHandler):
    def get(self):
        dates = self.request.get('date')
        froms = self.request.get("from")
        to = self.request.get("to")
        #froms= "BOM"
        #to = "CBJ"
        resp=urlfetch.fetch("http://www.cleartrip.com/flights/results?from="+froms+"&to="+to+"&depart_date="+dates+"&adults=1&childs=0&infants=0&dep_time=0&class=Economy&airline=&carrier=&x=57&y=16&flexi_search=no&tb=n")
        soup = BS(resp.content)
        my_content = soup.find("script",{"id":"json"})
        string_resp = str(my_content).strip()
        #self.response.out.write(str(string_resp))
        resp_splitted = string_resp.split(';')
        #self.response.out.write(str(resp_splitted))
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('<html><body><table>')
        a = 2-len(resp_splitted)
        
        
        
        #self.response.out.write(string_resp)
        #query2 = resp_splitted[-10].split('=')
        #self.response.out.write(query2[1])
        """content = eval(query2[1])
        self.response.out.write('<tr><td>Price</td>')
        self.response.out.write('<td>'+content['pr']+'</td></tr>')
        legs = content['legs']
        i = 0
        for leg in legs:
			self.response.out.write('<tr><td>Way '+str(i)+':</td></tr>')
			self.response.out.write('<td>'+leg['fr'] + "to "+ leg['to'] +'</td>')
			self.response.out.write('<tr><td>Arrival '+str(i)+':</td></tr>')
			self.response.out.write ('<td>'+leg['a']+'</td>')
			self.response.out.write('<tr><td>Departure '+str(i)+':</td></tr>')
			self.response.out.write ('<td>'+leg['dp']+'</td>')
			i+=1"""
	
        
        for query in range(a,-9):
			query2 = resp_splitted[query].strip().split('=')
			
			
			try:
				content = eval(query2[1])
				self.response.out.write("<tr><td>******************</td></tr>")
				self.response.out.write('<tr><td>Price</td>')
				self.response.out.write('<td>'+str(content.get('pr'))+'</td></tr>')
				legs = content.get('legs')
				i = 0
				for leg in legs:
					i+=1
					self.response.out.write('<tr><td>Way '+str(i)+':</td>')
					self.response.out.write('<td>'+leg.get('fr') + " => "+ leg['to'] +'</td></tr>')
					self.response.out.write('<tr><td>Arrival '+str(i)+':</td>')
					self.response.out.write ('<td>'+str(leg.get('a'))+'</td></tr>')
					self.response.out.write('<tr><td>Departure '+str(i)+':</td>')
					self.response.out.write ('<td>'+str(leg.get('dp'))+'</td></tr>')
					
				
			except:
				pass
				
				
				
				
			
		#self.response.out.write('</table>')	
			#self.response.write('<td>'+content['a']+'</td></tr>')
			#self.response.wrter('<tr><td>Departure</td>')
			#self.response.write('<td>'+content['pr']+'</td></tr>')
			
			
		
    
		
		
		
		


        
application = webapp.WSGIApplication(
                                     [('/', MainPage),('/search',SlideSharePage),],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
