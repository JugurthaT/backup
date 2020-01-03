import sqlite3
import os
from pathlib import Path
import catalog 

class job():
    BASEPATH='/opt/python/backup'
    DB_BASE_PATH=BASEPATH+'/DB'
    REPO_PATH=BASEPATH+'/REPO'
    DB_FILE_PATH=DB_BASE_PATH+'/catalog.db'
    print('The DB {}  will be open now'.format(DB_BASE_PATH))
    def __init__(self):
       
        try:
            Path(job.DB_BASE_PATH).mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            pass

        con = sqlite3.connect(job.DB_FILE_PATH, isolation_level=None)
        cur= con.cursor()
        QUERY="insert into jobs (path,status) values('-','active')" 
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
        path=os.path.join(job.BASEPATH,'REPO',str(self.JOBID))
        try:
            os.mkdir(path)
        except FileExistsError:
            pass 
        return path


    def get_base_path(self):
        return job.REPO_PATH    


    def update_catalog(self,jid,sfname,tfname):
        con = sqlite3.connect(job.DB_FILE_PATH, isolation_level=None)
        cur= con.cursor()
        jobid=int(jid)
        cur.execute('insert into index_table values (?,?,?)', (jobid,sfname,tfname))
        cur.execute(" UPDATE jobs  SET status = 'completed'  WHERE id =?",(jobid,) )
        print("index cache updated")

"""
def create_job_folder(self,jobid):
    return none
def add_catalog_entry(self,jobid):
    return none
"""
