from handler.lib import *
from pipeline import pipeline as p
from utils.dbconnection import DatabaseConnection
from repos import prediction_repos
from logger import LoggerMixin

class PredictHandler(tornado.web.RequestHandler,LoggerMixin):
    def initialize(self,path):
        self.path = os.path.join(path,"./backend/text_model.pth")
        self.db_collection = DatabaseConnection.get_connection()

    def write_error(self, status_code, **kwargs):
        self.write(f"Error {status_code}: Something went wrong.")

    async def get(self):
        selected_hotel = self.get_argument('hotel')
        self.logger.info("Get predicted data from DB")
        out = await prediction_repos.find_hotel_prediction(self.db_collection,selected_hotel)
        self.write(dict(out))
