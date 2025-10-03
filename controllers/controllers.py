from flask import Blueprint,render_template,request,redirect,url_for,session,Response
from werkzeug.security import generate_password_hash
from database.config_database import db,createTables
from flask_cors import CORS
from auth.auth import Auth
from json import dumps
import os
from google import genai
from auth.reset_email import ResetPass
db.databaseActive()
createTables()
appTask=Blueprint("tasks",__name__,template_folder='templates',static_folder='static')
CORS(appTask)

# Tudo referente a autenticação, registro, login e sessão.
@appTask.route('/')
def login():
 return render_template('login.html')

@appTask.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
       try:
         user=request.form['user']
         name=request.form['name']
         email=request.form['email']
         password_register=request.form['password']
         confirm_register=request.form['confirmpassword']
         if password_register==confirm_register:
            password=generate_password_hash(password_register)
            db.createValue('users','username,name,email,password',f'"{user}","{name}","{email}","{password}"')
            return render_template('register.html', sucess="Realizado com sucesso")
         else:
            return render_template('register.html',warning='As senhas não estão iguais')
       except :
         return render_template('register.html',error='Usuário ou email já existente')
    return render_template('register.html')
    
@appTask.route('/auth',methods=["POST"])
def auth():
    if request.method=="POST":
     return Auth("loginname","loginpassword").verify()
    
    
@appTask.route('/logout',methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('tasks.login'))
   

#Tudo referente a página inicial das atividades. 
@appTask.route('/home')
def home():
   redirect(url_for('tasks.home'))

   return render_template('home.html')

@appTask.route('/registertask',methods=['POST'])
def registerTasks():
   if request.method=="POST":
         hour=request.form['hour_task']
         nameTask=request.form['nametask']
         descriptionTask=request.form['descriptiontask']
         week=request.form['week']
         db.createValue('tasks','name,description,hour,id_tasksuser,week',f'"{nameTask}","{descriptionTask}","{hour}","{session['user']['id']}","{week}"')
       
     
   return redirect(url_for('tasks.tasks'))

@appTask.route('/alltasks')
def allTasks():
  tasks=db.selectValue('*','tasks',f'id_tasksuser={session['user']['id']} ORDER BY hour ASC')
  if tasks:
    return Response(dumps([{"id":act[0],"name":act[1],"description":act[2],"important":act[3],"hour":act[4],"id_user":act[5],"week":act[6]} for act in tasks]))
  

@appTask.route('/delete',methods=['POST'])
def deleteTask():
   if request.method=='POST':
      id=request.form['id_card']
      db.deleteValue('tasks','id_tasks',id)
   return redirect(url_for('tasks.tasks'))    
      

@appTask.route('/tasks')
def tasks():
  return render_template('tasks.html')

@appTask.route('/updatetask',methods=['POST'])
def updateTask():
   if request.method=='POST':
      data=request.get_json()
      id=data.get('id')
      value=data.get('value')
      db.updateValue("tasks","week",value,"id_tasks",id)
   return redirect(url_for('tasks.tasks'))

@appTask.route('/updatedetail',methods=['POST'])
def updateDetails():
   if request.method=='POST':
       data=request.get_json()
       id=data.get('id')
       hour=data.get('hour')
       textarea=data.get('description')
       db.updateValue("tasks","hour",hour,"id_tasks",id)
       db.updateValue("tasks","description",textarea,"id_tasks",id)
   return redirect(url_for('tasks.tasks'))

@appTask.route('/chat',methods=['POST'])
def chat():
  if request.method=='POST':
      try:
         api_key=os.getenv("GEMINI_API")
         question=request.get_json()
         data=question.get('data')
         db.createValue("chat","user_id,question,name_user",f'"{session['user']['id']}","{data}","You"')
         client= genai.Client(api_key=api_key)
         ia_response=client.models.generate_content(model='gemini-2.5-flash',contents=data + '(max 300 tokens, não inserir isso na resposta)',)
         if ia_response.text:
            db.createValueIA("chat","user_id,response,name_user",[session['user']['id']+1,ia_response.text,"Gemini"])
            return redirect(url_for('tasks.chatia'))
      except:
         return render_template('chat.html')
  return redirect(url_for('tasks.chatia'))

@appTask.route('/allchat')
def allchat():
   history=db.selectAllValues("chat")
   if history :
      return Response(dumps([{"id":itens[0],"user_id":itens[1],"question": itens[2]  if itens[2] else 'none',"response":itens[3] if itens[3] else 'none',"name":itens[4]} for itens in history]))

@appTask.route('/cleanchat',methods=['POST'])
def cleanchat():
    if request.method=='POST':
      db.deleteValue('chat', 'user_id',session['user']['id']+1)
      db.deleteValue('chat', 'user_id',session['user']['id'])
      return redirect(url_for('tasks.chatia'))

@appTask.route('/chatia')
def chatia():
   return render_template('chat.html')

@appTask.route('/resetpass/<token>',methods=['GET'])
def reset(token):
   return render_template('/reset_password.html',token=token)
  

@appTask.route('/sendcode',methods=['POST'])
def code_pass():
   if request.method =="POST":
      try:
         email=request.form['email_password']
         data=db.selectValue('*','users',f"email='{email}'")
         if data:
            reset_pass=ResetPass(email)
            reset_pass.sendEmail()
            return render_template('/login.html',success_mail='Enviado com sucesso')
         else:
            return render_template('/login.html',error_mail='Email informado incorreto, Registre-se antes de tentar resetar senha')
      except Exception as e:
         return render_template('/login.html',error_mail=e)
   return redirect(url_for('task.login'))

@appTask.route('/sendpass',methods=['POST'])
def sendpass():
    if request.method=='POST':
      try:
        password=request.form['pass']
        confirm_pass=request.form['confirm_pass']
        token=request.form['token']
        if password==confirm_pass:
         password_hash=generate_password_hash(password)
         db.updateValue('users','password',password_hash,"token",token)
         return render_template('reset_password.html',success='Senha alterada com sucesso')
        else:
         return render_template('reset_password.html',erro='Nova senha e senha de confirmação estão divergentes')
      except Exception as e:
        return render_template('reset_password.html',erro=e)

@appTask.route('/userconfig',methods=['GET'])
def user():
   return render_template('user.html')

@appTask.route('/deleteuser',methods=["POST"])
def deleteuser():
   if request.method=='POST':
      try:
         db.deleteValue('users','id_user',session['user']['id'])
         return redirect(url_for('tasks.login'))
      except Exception as e:
         return redirect(url_for('tasks.login'))
   pass

@appTask.route('/updateuser',methods=['POST'])
def update():
   if request.method=='POST':
      name=request.form['update-name']
      email=request.form['update-email']
      try:
         db.updateValue("users","name",f"{name}",'id_user',session['user']['id'])
         db.updateValue("users","email",f"{email}",'id_user',session['user']['id'])
         session['user']['name'] = name
         session['user']['email'] = email
         return render_template('user.html',success='Dados atualizados com sucesso')
      except Exception as e:
         print(e)
   return render_template('user.html')

 





    