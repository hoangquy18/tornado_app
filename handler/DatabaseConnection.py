import json
import utils
import motor.motor_tornado
from asyncio import create_task,gather,get_event_loop
import asyncio
import sys
import utils

class DatabaseConnection:
    _instance = None
    _url = None
    db_name = None
    
    def __new__(self,user_name, password,db_name, *arg, **kwargs):
        if self._instance is None:
            self._instance = super(DatabaseConnection,self).__new__(self, *arg, **kwargs)
            self._url = f"mongodb+srv://{user_name}:{password}@cluster0.vcb5k8u.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NONE"
            self.db_name = db_name
            self._instance.connection = self.get_database()
        return self._instance

    @classmethod
    async def get_database(self):
        """
            GET DATABASE FROM DB_NAME
        """
        client = motor.motor_tornado.MotorClient(self._url,serverSelectionTimeoutMS=2000)
        try:
            db = client[self.db_name]
            _ = db['region'].find()
        except:
            raise ConnectionRefusedError("Unable to connect to the server!!!")
        return client[self.db_name]
