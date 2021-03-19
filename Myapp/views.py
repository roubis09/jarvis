from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
import random
import wolframalpha
import wikipedia
from googlesearch.googlesearch import GoogleSearch
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    
    return render(request, 'Myapp/register.html', {'form': form})

@login_required
def home(request):
    template_name = 'Myapp/home.html'

    return render(request, template_name)

class HomePageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.email
        print(user)
        template_name = 'Myapp/home.html'
        return render(request, template_name)
    
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

@login_required
def send_email(request):
    name = request.GET.get('name')
    message = request.GET.get('message')

    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login('biswasrounik@gmail.com', 'dyzfwezugksgrndd')

    msg = MIMEMultipart()
    message_template = read_template('Myapp/message.txt')
    #message = 'Dear ${PERSON_NAME},Congratulations 🎊🎊🎊🎊,  you have received a email from Mitchell 📧 🥳 🎉 . This is the message ➡ ${MESSAGE}Enjoy your day 😇 Bye.'
    message = message_template.substitute(PERSON_NAME=name,MESSAGE=message)
    msg['From'] = 'biswasrounik@gmail.com'
    msg['To'] = 'biswasrounik@gmail.com'
    msg['Subject'] = "CONFORMATION MAIL"
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    try :
        s.send_message(msg)
        s.quit()
        ans = "Message Sent"
        return render(request, 'Myapp/sendmail.html', {'ans': ans})
    except Exception as e:
        s.quit()
        ans = "Message Not Sent"
        return render(request, 'Myapp/send_mail.html', {'ans': ans})

@login_required
def bot_search(request):
    query = request.GET.get('query')

    text = str(query).lower()

    jarvis_greetings = ['hi this is jarvis...', 'How can i help you?']
    users_greetings = ['hello', 'Hi there']
    exitlist = ['Thank you for using jarvis', 'Bye']

    for words in text.split():
        if words in users_greetings:
            return render(request, "Myapp/chat_view.html", {'ans': random.choice(jarvis_greetings), 'query': query})

        elif words in users_greetings:
            return redirect('home')

    try:
        client = wolframalpha.Client("PYE6H9-XHTK4V29G3")
        res = client.query(query)
        ans= next(res).text
        return render(request, 'Myapp/chat_view.html', {'ans': ans, 'query': query})

    except Exception:
        try:
            ans= wikipedia.summary(query, sentences= 5)
            return render(request, 'Myapp/chat_view.html', {'ans': ans, 'query': query})
        except Exception:
            try:
                response= GoogleSearch().search(query)
                ans = response.results.getText()
                return render(request, 'Myapp/chat_view.html', {'ans': ans, 'query': query})
            except:
                ans= "Answer Not found"
                return render(request, 'Myapp/chat_view.html', {'ans': ans, 'query': query})


