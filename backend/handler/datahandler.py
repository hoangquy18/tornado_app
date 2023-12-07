from handler.lib import *
from services.dataservice import DataService
class DataHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.data_service = DataService()

    def write_error(self, status_code, **kwargs):
        # Custom error handling code goes here
        self.write(f"Error {status_code}: Something went wrong.")
        
    async def get(self):
        try:
            data = await self.data_service.get_data()
            self.write(dict(data))
        except Exception as ex:
            self.write("Cannot get data from Database!")
            
            raise tornado.web.HTTPError(log_message = str(ex))
    
