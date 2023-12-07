import asyncio
import os
from utils import db_utils
from utils.dbconnection import DatabaseConnection
from services import *
from handler import *
import tornado

class Application(tornado.web.Application):
        def __init__(self):
            handlers = [
                tornado.web.URLSpec(r"/", HomeHandler,{"path": os.path.dirname(os.path.abspath(__name__))},name='home'),
                tornado.web.URLSpec(r"/predict", PredictHandler,{"path": os.path.dirname(os.path.abspath(__name__))}, name="predict"),
                tornado.web.URLSpec(r"/get_data", DataHandler ,name="data"),
                tornado.web.URLSpec(r"/submit", SubmitHandler, name="submit"),
            ]

            super(Application, self).__init__(handlers, debug = True)

def make_app(*args,**kwargs):
    return Application(*args,**kwargs)

async def main():
    db_atr = db_utils.load_db_config("./backend/config.yaml")
    db_connect = await DatabaseConnection(**db_atr)
    dbase = db_connect.get_connection()

    app = make_app()

    app.listen(8888)
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()

if __name__ == "__main__":
    os.environ['CURL_CA_BUNDLE'] = ''

    asyncio.run(main())
