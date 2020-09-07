import schedule
import time
import datetime
import requests
from .settings import EMAIL_HOST_USER, BASE_DIR
from django.core.mail import EmailMultiAlternatives
import codecs
import os
from jinja2 import Template
# from BASE import CustomUser,Profile
# users = CustomUser.objects.all()
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


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
        if abs(cur_time - date_time_obj).seconds <= 36000:
            return True
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
                'with_in_an_hour': self.if_in_next_one_hour(self.time_formatter(contest['StartTime'])),
            }
            self.contests.append(contest_details)

        self.with_in_hr = []
        for item in self.contests:
            if item['with_in_an_hour']:
                self.with_in_hr.append(item)

    def generate_body(self, contests, mail_html_path):
        '''
                this function will generate html message for mail body by using jinja2 templating
                this function gets contests(list) as arg and use for generating html
                and return html_text message
        '''
        body = ""
        with open(mail_html_path, 'r', encoding="utf-8") as file:
            body = file.read()
        template = Template(body)
        # print(template.render(contests=contests))

        html_text = template.render(contests=contests)
        return html_text

    def mail_user(self, message, from_mail, to_mail):
        '''
                this function mail one user at time but we can do with multiple at time
                by passing list of mail(type=str) instead [to_mail] change according
                this function uses django.core.mail.EmailMultiAlternatives class which is 
                wrapper around smptp server so pass argmunts accordingly.
                here msg.attach_alternative is used specificly for html mail istead is can use 
                plain text for not supported client.
        '''
        subject = message["subject"]
        text_content = message["text"]
        html_content = message["html"]

        msg = EmailMultiAlternatives(
            subject, text_content, from_mail, [to_mail])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print('mail sent success...')

    def send_mail(self, users):
        '''
                this function is sending reminder mail to each user passed in arg.
                here from_mail = EMAIL_HOST_USER can be set from .settings 
                see django.core.mail documentation for that.
        '''
        subject = 'Contest Reminder'
        # mail_html_path = "########"  # fill this path relative path
        mail_html_path = TEMPLATE_DIR + '/new_mail.html'  # fill this path relative path

        html_text = self.generate_body(self.with_in_hr, mail_html_path)
        message = {
            "subject": subject,
            "text": "Your browser doesn't support html mail.",
            "html": html_text,
        }

        from_mail = EMAIL_HOST_USER

        for user in users:
            to_mail = str(user.email)
            self.mail_user(message, from_mail, to_mail)

    def reminder(self, users):
        '''
                this is main calling function for all the above methods.
                we get users data as list of mail and send_mail to them.
        '''
        self.collect_data()
        print('in reminder')
        if not len(self.with_in_hr) == 0:
            print('in reminder')
            self.send_mail(users)


# rem = Reminder()
# rem.reminder(users)

# schedule.every().hour.do(rem.reminder(users))


# while True:
#     schedule.run_pending()
#     time.sleep(1)
