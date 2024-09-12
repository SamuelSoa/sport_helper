from cgitb import reset
import psycopg2
from business_object.particulier import Particulier
from dao.dbconnection import DBConnection
from outil.singleton import Singleton
from psycopg2.extras import RealDictCursor
from outil.singleton import Singleton
from outil import message

class MessageDao():

    def add_message(self,message,id_user):
        rq = "INSERT INTO message(message , id_user) VALUES(%(message)s , %(id_user)s)"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(rq,{"message" : message
                , "id_user" : id_user})
    def get_all_message(self) -> list[message]:
        sql = f"SELECT * FROM message "
        connection = DBConnection().connection
        with connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        return res

   
    def get_message_by_id_user(self,id_user): #afficher les messages selon l'id 
        sql = 'SELECT message FROM message WHERE id_user=%(id_user)s'
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql,{"id_user": id_user})
                res = cursor.fetchone()
                return res[0]
    def get_id(self):
        sql = 'SELECT id_user FROM message'
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                res = cursor.fetchall()
                id = []
                for i in range(len(res)):
                    id.append(res[i][0])
                return id
                    

