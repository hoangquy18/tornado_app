import asyncio
import os
import utils
from handler import DatabaseConnection
from handler.Application import Application
from services import *

def make_app(*args,**kwargs):
    return Application(*args,**kwargs)

async def main():
    db_atr = utils.load_db_config("./config.yaml")
    db_connect = await DatabaseConnection(**db_atr)
    dbase = db_connect.connection
    
    db_service = DatabaseService(db = dbase)
    data_service = DataService(db_service=db_service)

    app = make_app(db_service = db_service, data_service = data_service)

    app.listen(8888)
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()

if __name__ == "__main__":
    os.environ['CURL_CA_BUNDLE'] = ''

    asyncio.run(main())
