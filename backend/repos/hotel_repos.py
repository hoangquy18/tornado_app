from pymongo.errors import ServerSelectionTimeoutError

async def get_hotel_dict(db_collection) -> dict:
    try:
        hotel_dict = db_collection['hotel'].find()
        hotel_dict = await hotel_dict.to_list(length=1000)

    except ServerSelectionTimeoutError:
        raise ConnectionRefusedError("CANNOT CONNECT TO DATABASE!!!")

    return hotel_dict
