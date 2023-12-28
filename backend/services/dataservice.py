from services.lib import *
from utils.dbconnection import DatabaseConnection
from repos.region_repos import get_region_hotel_dict
from logger import LoggerMixin

class Base(object):
    pass


class DataService(LoggerMixin):
    def __init__(self ) :
        self.db_collection = DatabaseConnection.get_connection()
        super(DataService,self).__init__()

    async def get_data(self):
        try:
            cities_hotels_dict = await get_region_hotel_dict(self.db_collection)
            cities_list = list(cities_hotels_dict.keys())

            data = {
                "cities": cities_list,
                "hotels": cities_hotels_dict
            }

        except Exception as e:
            self.logger.error("ServerSelectionTimeoutError - Cannot connect to Database")
            raise tornado.web.HTTPError(log_message = str(e))
        
        return data
    
    
    
