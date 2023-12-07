from handler.lib import *
from pipeline import pipeline as p
from utils.dbconnection import DatabaseConnection

class PredictHandler(tornado.web.RequestHandler):
    def initialize(self,path):
        self.path = os.path.join(path,"./backend/text_model.pth")
        self.db_collection = DatabaseConnection.get_connection()

    def write_error(self, status_code, **kwargs):
        self.write(f"Error {status_code}: Something went wrong.")

    async def get(self):
        selected_hotel = self.get_argument('hotel')
        out = await p.wrapper_predict_from_selected(self.path,self.db_collection,selected_hotel)
        self.write(dict(out))
