from services.lib import *
from utils.dbconnection import DatabaseConnection
from repos.region_repos import get_region_hotel_dict

class DataService:
    def __init__(self ) -> None:
        self.db_collection = DatabaseConnection.get_connection()

    async def get_data(self):
        cities_hotels_dict = await get_region_hotel_dict(self.db_collection)
        cities_list = list(cities_hotels_dict.keys())

        data = {
            "cities": cities_list,
            "hotels": cities_hotels_dict
        }

        return data

    
