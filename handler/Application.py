from handler import *
import tornado

class Application(tornado.web.Application):
        def __init__(self,db_service, data_service):
            handlers = [
                tornado.web.URLSpec(r"/", HomeHandler,name='home'),
                tornado.web.URLSpec(r"/predict", PredictHandler, dict(db_service = db_service), name="predict"),
                tornado.web.URLSpec(r"/get_data", DataHandler, dict(data_service = data_service) ,name="data"),
                tornado.web.URLSpec(r"/submit", SubmitHandler, name="submit"),
            ]

            super(Application, self).__init__(handlers)

