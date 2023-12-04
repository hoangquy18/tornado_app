from handler.lib import *

class HomeHandler(tornado.web.RequestHandler):
    def initialize(self,path):
        self.path = path
    def get(self):
        try:
            return self.render(os.path.join(self.path,"./fontend/index.html"))
        except FileNotFoundError:
            raise FileNotFoundError("File Not Found!!!")
