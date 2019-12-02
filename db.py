"""
@theme: Database
"""
import psycopg2

class DatabaseException(Exception):
    pass

class Sync(object):
    """ Document Sync function """
    def es_server(self):
        pass
    
    def postgres_server(self,db,user,password,tablename,host="localhost",port="5432"):
        conn = psycopg2.connect(
                database=db, 
                user=user, 
                password=password, 
                host=host, 
                port=port)
        """
        cur = conn.cursor()
        cur.execute(
                "INSERT INTO {} (token,token_md5) VALUES('{}','{}');".format(
                tablename,
                token,
                token_md5
                )
        )
        
        conn.commit()
        conn.close()"""
        # check the tokens if new tokens emerge, update with them
        

    def __init__(self,doc):
        """ Basic sync object: update Document with Database dynamics """
        pass
    
    
