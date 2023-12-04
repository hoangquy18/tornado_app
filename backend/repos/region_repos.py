from pymongo.errors import ServerSelectionTimeoutError
from utils import db_utils
from repos.hotel_repos import get_hotel_dict

async def get_region_dict(db_collection) -> dict:
    try:
        region_dict =  db_collection['region'].find()
        region_dict = await region_dict.to_list(length=100)
        
    except ServerSelectionTimeoutError:
        raise ConnectionRefusedError("CANNOT CONNECT TO DATABASE!!!")

    return region_dict


async def get_region_hotel_dict(db_collection) -> dict:
    region_hotel_dict = {}

    region_dict = await get_region_dict(db_collection)
    hotel_dict = await get_hotel_dict(db_collection)
    region_list = list(map(lambda x: x['region_name'],region_dict))
    
    for region in region_list:
        reg_id = db_utils.find_id_region(region_dict,region)
        region_hotel_dict[region] = db_utils.find_hotel_in_region(hotel_dict,reg_id)

    return region_hotel_dict
