import schedule
from .settings import EMAIL_HOST_USER, BASE_DIR, EMAIL_HOST_PASSWORD
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase 
from email import encoders


from jinja2 import Environment, FileSystemLoader
import os
import datetime
import requests
import pytz

base_dir = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
image_dir = os.path.join(BASE_DIR,'static/images')


env = Environment(loader=FileSystemLoader('{0}'.format(os.path.dirname(__file__))))


# users = [
#     {
#         'mail': 'om181299@gmail.com',
#     },
#     {
#         'mail': 'ozx1812@gmail.com',
#     }
# ]


class Reminder:

    def __init__(self):
        self.data = []

    def call_url_api(self, URL):
        '''
                this function will call API request
        '''
        data = requests.get(url=URL)
        data = data.json()
        return data

    def if_in_next_one_hour(self, date_time_obj):
        '''
                this function is for checking if contest will be with in one hour
        '''
        cur_time = datetime.datetime.now()      
        date_time_obj = self.time_formatter(date_time_obj)
        diff = (cur_time - date_time_obj)
        duration_in_s = diff.total_seconds()+19800 # .now() give utc time but api give Asia/kolkata time 
        # so add 5hr 30min = 19800 sec difference. 
        hrs = divmod(duration_in_s, 3600)[0]
        print(hrs)
        if abs(hrs) < 9.0: # number of hours
            return True
        else:
            return False

    def date_formatter(self, temp_time):
        '''
        return date from datetime obj
        '''
        return datetime.datetime.strptime(temp_time, "%a, %d %b %Y %H:%M")
        # return datetime.datetime.strftime(temp_time, "%d %b %Y")

    def time_formatter(self, temp_time):
        '''
                this function will return datetime object from string base time by formatting
        '''
        return datetime.datetime.strptime(temp_time, "%a, %d %b %Y %H:%M")
        
        # return datetime.datetime.strftime(temp_time, "%H:%M")

    def collect_data(self):
        '''
                this function will call API and then process data 
                and store to self.contests which has all contests details each as dictnory
                and also self.with_in_an_hour will have all the contests that will be in 
                next hour.
        '''
        self.data = self.call_url_api(
            "https://www.stopstalk.com/contests.json")

        self.upcoming = self.data['upcoming']

        # cur_time = datetime.datetime.now()

        self.contests = []
        for contest in self.upcoming:
            contest_details = {
                'Name': contest['Name'],
                'StartTime': datetime.datetime.strftime(self.time_formatter(contest['StartTime']), "%H:%M"),
                'EndTime': datetime.datetime.strftime(self.time_formatter(contest['EndTime']), "%H:%M"),
                'StartDate': datetime.datetime.strftime(self.date_formatter(contest['StartTime']), "%d %b %Y"),
                'Duration': contest['Duration'],
                'Host': contest['Platform'],
                'contestLink': contest['url'],
                'with_in_an_hour': self.if_in_next_one_hour(contest['StartTime']),
            }
            self.contests.append(contest_details)

        self.with_in_hr = []
        for idx, item in enumerate(self.contests):
            # print('#{}..{}'.format(idx, item))
            if item['with_in_an_hour'] == True:
                self.with_in_hr.append(item)
                print('#{}..{}'.format(idx, item))

        # for idx, item in enumerate(self.contests):
        #     print('#{}..{}'.format(idx, item))
        # print('contests len {}'.format(len(self.contests)))

    
    def get_template(self,contest):
        env = Environment(loader=FileSystemLoader('{0}'.format(TEMPLATE_DIR)))
        template = env.get_template('mail2.html')
        output = template.render(contest=contest)
        return output

    def send_mail(self, user, contest, server, from_mail):
        subject = 'ContestReminder'

        message = MIMEMultipart('related')

        message['Subject'] = subject
        message['From'] = from_mail
        to_mail = str(user.email)
        message['To'] = to_mail

        message.preamble = 'This is a multi-part message in MIME format.'

        msgAlternative = MIMEMultipart('alternative')
        message.attach(msgAlternative)

        msgText = MIMEText('Hello coders! Are you all set for upcoming contest?')
        msgAlternative.attach(msgText)

        bodyContent = self.get_template(contest)
        
        msgText = MIMEText(bodyContent, 'html')
        msgAlternative.attach(msgText)

        img_path = image_dir
        if(contest['Host'] == "CODEFORCES"):
            img_path += '/CODEFORCES.png'
        elif(contest['Host'] == "CODECHEF"):
            img_path += '/CODECHEF.png'
        elif(contest['Host'] == "HACKEREARTH"):
            img_path += '/HACKEREARTH.png'
        elif(contest['Host'] == "HACKERRANK"):
            img_path += '/HACKERRANK.png'
        elif(contest['Host'] == "SPOJ"):
            img_path += '/SPOJ.png'

        fp = open(img_path, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()

        msgImage.add_header('Content-ID', '<image1>')
        message.attach(msgImage)
        
        msgBody = message.as_string()
        try:
            server.sendmail(from_mail, to_mail, msgBody)
        except:
            print('ERROR: mail sending error occured...')
        else:
            print('mail sent successfully...')
        


    def send_mails(self,users,contest):
        from_mail = EMAIL_HOST_USER
        server = SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_mail, EMAIL_HOST_PASSWORD)
        for user in users:
            self.send_mail(user,contest,server,from_mail)
        server.quit()

    def reminder(self, users):
        self.collect_data()
        if not len(self.with_in_hr) == 0:
            print('{0} contest are in next hr...'.format(len(self.with_in_hr)))
            for contest in self.with_in_hr:
                self.send_mails(users,contest)  
        else:
            print('no contests in next hr...',len(self.with_in_hr))


# rem = Reminder()
# rem.reminder(users)

# schedule.every().hour.do(rem.reminder(users))


# while True:
#     schedule.run_pending()
#     time.sleep(1)
