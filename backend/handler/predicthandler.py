from handler.lib import *
from pipeline import pipeline as p
from services import DatabaseService
class PredictHandler(tornado.web.RequestHandler):
    def initialize(self,path):
        self.db_service = DatabaseService()
        self.path = os.path.join(path,"./backend/text_model.pth")
    async def get(self):
        selected_hotel = self.get_argument('hotel')
        out = await p.wrapper_predict_from_selected(self.path,self.db_service,selected_hotel)
        self.write(dict(out))
