from flask import Flask
from controllers.controllers import appTask
from flask_session import Session
from auth.mail import mail
import os 
from dotenv import load_dotenv
import webview
load_dotenv()

app=Flask(__name__)
app.register_blueprint(appTask)
app.config['SESSION_TYPE']="filesystem"
app.secret_key='1234'
window=webview.create_window('TaskCheck',app,confirm_close=True,min_size=(982,1512),minimized=False, maximized=False)

# Configuração de Email 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.getenv('EMAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.getenv('PASSWORD_USER')

Session(app)
mail.init_app(app)

if __name__ == '__main__':
  webview.start(lambda: window.maximize())