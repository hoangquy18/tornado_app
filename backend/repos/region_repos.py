from pymongo.errors import ServerSelectionTimeoutError
from utils import db_utils

async def get_region_hotel_dict(db_collection) -> dict:
    region_hotel_dict = {}

    try:
        region_hotel_query = db_collection['region'].aggregate([
                                    {
                                        "$lookup": {
                                            'from': "hotel",       # collection hotel
                                            'localField': "_id",       # key in region
                                            'foreignField': "region_id",  # foreign key in hotel
                                            'as': "hotels"             # saved name
                                        }
                                    },
                                    {
                                        "$project": {
                                            'region_name': 1,         
                                            'hotels.hotel_name': 1               
                                        }
                                    }
                                ])
                                
        region_hotel_query = await region_hotel_query.to_list(length=10000)
    except ServerSelectionTimeoutError:
        raise ConnectionRefusedError("CANNOT CONNECT TO DATABASE!!!")
        
    for i in region_hotel_query:
        region_hotel_dict[i['region_name']] = list(map(lambda x: x['hotel_name'],i['hotels']))

    return region_hotel_dict
