import sqlite3

class DataBase:
    def __init__(self):
        self.con = None 
        self.cur = None 
        self.connectDataBase()
        self.createTable()
        self.userColumns = ["id","pw","name","age","phoneNum"]
        
    def connectDataBase(self): 
        self.con = sqlite3.connect("UserDataBase.db")
        self.cur = self.con.cursor() 

    #묶기
    def createTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS user (id TEXT, pw TEXT, name TEXT, age INTEGER, phonenumber TEXT, usercode INTEGER PRIMARY KEY AUTOINCREMENT)") #대소문자 구분하기
        self.cur.execute("CREATE TABLE IF NOT EXISTS winrate (usercode INTEGER, win INTEGER, draw INTEGER, lose INTEGER, FOREIGN KEY(usercode) REFERENCES user(usercode))") #대소문자 구분하기
        self.cur.execute("PRAGMA foreign_keys = 1")

    def dataCreate(self,tableName,columnList,dataList):
        sentence = "INSERT INTO "
        sentence += tableName
        sentence += "("
        for i in range(0,len(columnList)-1):
            sentence += columnList[i]
            sentence += ", "
        sentence += columnList[len(columnList)-1]
        sentence += ") VALUES("
        for i in range(0,len(columnList)-1):
            sentence += "?"
            sentence += ", "
        sentence += "?"
        sentence += ")"
        data = dataList
        self.cur.execute(sentence,data) 
        self.con.commit()
        
    def dataRead(self,tableName,dataCol,data):
        sentence = "SELECT * FROM "
        sentence += str(tableName)
        sentence += " WHERE "
        sentence += str(dataCol)
        sentence += "=?"
        dataArr = [data]
        self.cur.execute(sentence,dataArr) 
        result = self.cur.fetchall() 
        return result

    def dataUpdate(self,tableName,colType,newData,usercode): #중복체크
        sentence = "UPDATE "
        sentence += tableName
        sentence += " SET "
        sentence += colType
        sentence += "=? WHERE usercode=?"
        data = [newData,usercode]
        self.cur.execute(sentence,data) 
        self.con.commit()
    
    def dataDelete(self,id): #아이디 로그인 체크
        data = [id]
        self.cur.execute("DELETE FROM user WHERE id=?",data) 
        self.con.commit()