from handler.lib import *
from services.dataservice import DataService
class DataHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.data_service = DataService()
        
    async def get(self):
        try:
            data = await self.data_service.get_data()
            self.write(dict(data))
        except:
            self.write_error("Cannot get data from Database!")
            raise tornado.web.HTTPError()