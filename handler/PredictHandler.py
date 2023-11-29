from handler.lib import *
from pipeline import pipeline as p

class PredictHandler(tornado.web.RequestHandler):
    async def get(self):
        db = self.application.db
        selected_hotel = self.get_argument('hotel')
        out, flag = await p.wrapper_predict_from_selected(db,selected_hotel)
        
        if flag != "":
            self.write(str(flag))
        else:
            self.write(dict(out))
