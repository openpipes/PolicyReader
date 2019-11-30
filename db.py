"""
@theme: Database
"""
import pymysql
pymysql.install_as_MySQLdb()


class DatabaseException(Exception):
    pass

class Sync(object):
    """ Document Sync function """
    def es_server(self):
        pass
    
    def sql_server(self,host,port,user,pwd,db,table):
        config = {
            'host':host,
            'port':port,
            'user':user,
            'password':pwd,
            'db':db,
            'charset':'',
            'cursorclass':pymysql.cursors.DictCursor,
        }
        db = pymysql.connect(**config)
        cursor = db.cursor()
        # check the tokens if new tokens emerge, update with them
        

    def __init__(self,doc):
        """ Basic sync object: update Document with Database dynamics """
        pass
    
    
