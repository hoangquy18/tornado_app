from handler.lib import *
from pipeline import pipeline as p

class PredictHandler(tornado.web.RequestHandler):
    def initialize(self, db_service):
        self.db_service = db_service
        
    async def get(self):
        selected_hotel = self.get_argument('hotel')
        out = await p.wrapper_predict_from_selected(self.db_service,selected_hotel)
        
        self.write(dict(out))
