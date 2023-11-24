import tornado
import asyncio
from as_dbconnect import *
import os
from pipeline import pipeline as p

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render("index.html")
    
class DataHandler(tornado.web.RequestHandler):
    async def get(self):
        db = self.application.db

        region_hotel_dict = await db.get_region_hotel_dict()
        region_list = list(region_hotel_dict.keys())

        data = {
            "cities": region_list,
            "hotels": region_hotel_dict
        }
        self.write(dict(data))

class SubmitHandler(tornado.web.RequestHandler):
    def post(self):
        hotel = self.get_argument("hotel", "")
        self.redirect(f"/predict?hotel={hotel}")

class PredictHandler(tornado.web.RequestHandler):
    async def get(self):
        db = self.application.db
        selected_hotel = self.get_argument('hotel')
        out, flag = await p.wrapper_predict_from_selected(db,selected_hotel)
        
        if flag != "":
            self.write(str(flag))
        else:
            self.write(dict(out))
            

class Application(tornado.web.Application):
        def __init__(self,user_name, password, db_name):
            handlers = [
                tornado.web.URLSpec(r"/", HomeHandler,name='home'),
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
