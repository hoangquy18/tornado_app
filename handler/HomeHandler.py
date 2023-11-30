from handler.lib import *

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render("index.html")
