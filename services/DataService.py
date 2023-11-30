from services.lib import *

class DataService:
    def __init__(self,db_service ) -> None:
        self.db_service = db_service
    
    async def get_data(self):
        cities_hotels_dict = await self.db_service.get_region_hotel_dict()
        cities_list = list(cities_hotels_dict.keys())

        data = {
            "cities": cities_list,
            "hotels": cities_hotels_dict
        }

        return data

    
