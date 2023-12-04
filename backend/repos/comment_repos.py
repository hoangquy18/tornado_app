from utils import db_utils 

async def find_comment_hotel(db_collection, hotel_dict, hotel_name):

    hotel_id = db_utils.find_id_hotel(hotel_dict,hotel_name)
    comments = []

    if hotel_id == -1:
        raise IndexError("THIS HOTEL NOT EXIST!!!")
    
    comment_hotel = db_collection['comment'].find({"hotel_id": hotel_id})
    comment_hotel = await comment_hotel.to_list(length=1000)
    
    for obj in comment_hotel:
        comments.append(obj['comment'])

    return comments
