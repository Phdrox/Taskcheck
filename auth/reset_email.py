from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask import current_app
from flask import url_for
from auth.mail import mail
from database.config_database import db

app=current_app

class ResetPass:
    def __init__(self,email):
        self.email=email

    def createToken(self):
        serialized=URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serialized.dumps(self.email,salt='pass_reset')
    
    def verifyToken(self,token,expire_token=3600):
        serialized=URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
           email=serialized.loads(token,salt='pass_reset',max_age=expire_token)
           return email
        except Exception as e:
            return None
    
    def sendEmail(self):
      token=self.createToken()
      reset_link=url_for('tasks.reset',token=token, _external=True)
      db.updateValue("users","token",token,"email",self.email)
      msg=Message('Reset sua senha',sender=self.email,recipients=[self.email])
      msg.body=f'Reset link Password: {reset_link}'
      mail.send(msg)
      
        
    

        