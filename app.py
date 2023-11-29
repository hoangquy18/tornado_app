import tornado
import asyncio
from as_dbconnect import *
import os
from pipeline import pipeline as p            
from handler import datahandler, homehandler, predicthandler, submithandler

class Application(tornado.web.Application):
        def __init__(self,user_name, password, db_name):
            handlers = [
                tornado.web.URLSpec(r"/", datahandler,name='home'),
                tornado.web.URLSpec(r"/predict", PredictHandler, name="predict"),
                tornado.web.URLSpec(r"/get_data", DataHandler, name="data"),
                tornado.web.URLSpec(r"/submit", SubmitHandler, name="submit"),
            ]

            super(Application, self).__init__(handlers)
            self.db = Database(user_name, password, db_name)

def make_app(**kwargs):
    return Application(**kwargs)

async def main():
    db_atr = {
        "user_name": "nhq188",
        "password": "fiora123",
        "db_name": 'User'
    }
    
    app = make_app(**db_atr)

    app.listen(8888)
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()

if __name__ == "__main__":
    os.environ['CURL_CA_BUNDLE'] = ''

    asyncio.run(main())
