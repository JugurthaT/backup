import sqlite3
import os
#import start_job
class job():
    global BASEPATH
    BASEPATH='/opt/python/chat'

    def __init__(self):
        con = sqlite3.connect('/opt/python/chat/db.sqlite3', isolation_level=None)
        cur= con.cursor()
        QUERY="insert into jobs (path,status) values('/opt/python/chat/repo','active')" 
        print("the query to insert",QUERY)
        cur.execute(QUERY)
        QUERYJOB="SELECT last_insert_rowid()" 
        cur.execute(QUERYJOB)
        jobid=cur.fetchall()
        self.JOBID=jobid[0][0]
        print("self.jobid=",self.JOBID)
        self.create_job_path(self.JOBID)
    def get_jobid(self):
        return self.JOBID
    

    def create_job_path(self,jobid):
        path=os.path.join(BASEPATH,str(self.JOBID))
        try:
            os.mkdir(path)
        except FileExistsError:
            pass 


    def update_catalog(self,jid,sfname,tfname):
        con = sqlite3.connect('/opt/python/chat/db.sqlite3', isolation_level=None)
        cur= con.cursor()
        jobid=int(jid)
        cur.execute('insert into index_table values (?,?,?)', (jobid,sfname,tfname))
        #cur.execute(QUERY)
        print("index cache updated")
"""
def create_job_folder(self,jobid):
    return none
def add_catalog_entry(self,jobid):
    return none
"""
