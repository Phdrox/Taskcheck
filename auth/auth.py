from database.config_database import db
from flask import session,redirect,request, url_for,render_template
from werkzeug.security import check_password_hash

#Criado um class de autenticação nela é colocado os nomes que vem no form html o user e password
class Auth:
    def __init__(self,user,password):
        self.user=request.form[user]
        self.password=request.form[password]
        
# Verifica no banco de dados através de uma consulta se o user existe, após isso verifica o hash da senha se são compatíveis, redirecionando para o home com sessão.     
    def verify(self):
        try:
            login=list(db.selectValueAuth('*','users',f'username="{self.user}"'))
            if check_password_hash(login[4],self.password):
                try:
                    session['user']={"id":login[0],"username":login[1],"name":login[2],"email":login[3]}
                    return redirect(url_for('tasks.home'))
                except:
                    return render_template('login.html',error="Coloque as credenciais corretamente")

        except:
            return render_template('login.html',error="Coloque as credenciais corretamente")
        return render_template('login.html',error="Coloque as credenciais corretamente")  