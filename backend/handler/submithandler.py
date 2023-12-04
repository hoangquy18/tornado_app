from handler.lib import *

class SubmitHandler(tornado.web.RequestHandler):
    def post(self):
        hotel = self.get_argument("hotel", "")
        self.redirect(f"/predict?hotel={hotel}")
