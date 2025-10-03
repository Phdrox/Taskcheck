import sqlite3 

class Database:
 def __init__(self):   
  self.database=sqlite3.connect('taskcheck.db',check_same_thread=False)
  self.cursor=self.database.cursor()
 
 def databaseActive(self):
   return self.database
 
 def createTable(self,nameTable,nameColumns):
  self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {nameTable}({nameColumns});")
  self.database.commit()
 
 def createValue(self,nameTable,nameColumns,valuesColumns):
   query=f"""INSERT INTO {nameTable} ({nameColumns}) VALUES ({valuesColumns})"""
   self.cursor.execute(query)
   self.database.commit()

 def createValueIA(self,nameTable,nameColumns,valuesColumns):
   placeholders=",".join("?" for _ in valuesColumns)
   query=f"INSERT INTO {nameTable} ({nameColumns}) VALUES ({placeholders})" 
   self.cursor.execute(query,valuesColumns)
   self.database.commit()
 
 def updateValue(self,nameTable,columns,value,id_column,id):
   query=f"""UPDATE {nameTable} SET {columns}=? WHERE {id_column}=? ;"""
   self.cursor.execute(query,(value,id))
   self.database.commit()
 
 def deleteValue(self, nameTable,id_column,id):
    query=f"""DELETE FROM {nameTable} WHERE {id_column}=? ;"""
    self.cursor.execute(query,(id,))
    self.database.commit()
 
 def selectValue(self, nameColumns,nameTable,condition):
    return self.cursor.execute(f"SELECT {nameColumns} FROM {nameTable} WHERE {condition} ;").fetchall()
 
 def selectValueAuth(self, nameColumns,nameTable,condition):
    return self.cursor.execute(f"SELECT {nameColumns} FROM {nameTable} WHERE {condition};").fetchone()
 
 def selectAllValues(self,nameTable):
   search=self.cursor.execute(f"SELECT * FROM {nameTable};")
   return search.fetchall()
 
db=Database()

def createTables():
    db.createTable("tasks","id_tasks integer primary key AUTOINCREMENT not null,name varchar(150),description longtext,important boolean, hour time, id_tasksuser integer ,week varchar(20)")
    db.createTable("users","id_user integer primary key AUTOINCREMENT not null unique ,username varchar(100) UNIQUE not null, name varchar(150) not null, email varchar(150) UNIQUE not null, password varchar(100),token varchar(16) null")
    db.createTable("chat","id_chat integer primary key AUTOINCREMENT not null, user_id integer not null, question longtext,response longtext, name_user varchar(250) not null, foreign key (user_id) references users(id_user)")
    