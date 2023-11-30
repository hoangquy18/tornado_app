from services.lib import *

class DataHandler(tornado.web.RequestHandler):
    def initialize(self, data_service):
        self.data_service = data_service
        
    async def get(self):

        data = await self.data_service.get_data()

        self.write(dict(data))
