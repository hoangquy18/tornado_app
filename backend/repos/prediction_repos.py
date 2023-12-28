from utils import db_utils 
from pymongo.errors import ServerSelectionTimeoutError


async def find_hotel_prediction(db_collection, hotel_name):
    
    try:
        hotel_prediction =  db_collection.hotel.aggregate([
                            {
                                "$match": {
                                    "hotel_name": f"{hotel_name}"
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "prediction",          
                                    "localField": "_id",       
                                    "foreignField": "hotel_id",  
                                    "as": "prediction"             
                                }
                            },
                            {
                                "$project": {
                                    "hotel_name": 1,         
                                    "prediction.label": 1               
                                }
                            }
                        ])
                    
        hotel_prediction = await hotel_prediction.to_list(length=10000)
    except ServerSelectionTimeoutError:
        raise ConnectionRefusedError("CANNOT CONNECT TO DATABASE!!!")

    try:
        hotel_name, hotel_label = hotel_prediction[0]['hotel_name'], hotel_prediction[0]['prediction'][0]['label']
    except:
        hotel_label = {}
    return hotel_label
