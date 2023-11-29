from handler.lib import *

class DataHandler(tornado.web.RequestHandler):
    async def get(self):
        db = self.application.db

        region_hotel_dict = await db.get_region_hotel_dict()
        region_list = list(region_hotel_dict.keys())

        data = {
            "cities": region_list,
            "hotels": region_hotel_dict
        }
        self.write(dict(data))
