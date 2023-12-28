from handler.lib import *
from services.dataservice import DataService
from logger import LoggerMixin

class HomeHandler(tornado.web.RequestHandler,LoggerMixin):
    def initialize(self,path):
        self.path = path
        self.data_service = DataService()

    def write_error(self, status_code, **kwargs):
        # self.write(f"Error {status_code}: Something went wrong.")
        self.write("CANNOT CONNECT TO DATABASE!!!")

    async def get(self):
        data = await self.data_service.get_data()
        try:
            self.logger.info("UI loaded successfully")
            return self.render(os.path.join(self.path,"./fontend/index.html"))
        except FileNotFoundError as fn:
            self.logger.error("Index file not found")
            raise tornado.web.HTTPError(log_message = str(fn))
        except Exception as e:
            self.logger.error("Something wrong",exc_info=True)
            raise tornado.web.HTTPError(log_message = str(e))
