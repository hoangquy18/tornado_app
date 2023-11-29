

class DataService:
    def __init__(self,db_service) -> None:
        self.db_service = db_service
    async def get_data(self):
        region_hotel_dict = await self.db_service.get_region_hotel_dict()
        region_list = list(region_hotel_dict.keys())

        data = {
            "cities": region_list,
            "hotels": region_hotel_dict
        }
        
        return data
