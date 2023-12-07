from handler.lib import *
from services.dataservice import DataService

class HomeHandler(tornado.web.RequestHandler):
    def initialize(self,path):
        self.path = path
        self.data_service = DataService()

    def write_error(self, status_code, **kwargs):
        # self.write(f"Error {status_code}: Something went wrong.")
        self.write("CANNOT CONNECT TO DATABASE!!!")

    async def get(self):
        data = await self.data_service.get_data()
        try:
            return self.render(os.path.join(self.path,"./fontend/index.html"))
        except FileNotFoundError as fn:
            raise tornado.web.HTTPError(log_message = str(fn))
        except Exception as e:
            raise tornado.web.HTTPError(log_message = str(e))
