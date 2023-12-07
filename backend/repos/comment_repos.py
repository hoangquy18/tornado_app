from utils import db_utils 

async def find_comment_hotel(db_collection, hotel_name):
    
    try:
        hotel_comment_query = db_collection.hotel.aggregate([
                {
                    "$match": {
                        "hotel_name": f"{hotel_name}"
                    }
                },
                {
                    "$lookup": {
                        "from": "comment",          
                        "localField": "_id",       
                        "foreignField": "hotel_id",  
                        "as": "comments"             
                    }
                },
                {
                    "$project": {
                        "hotel_name": 1,         
                        "comments.comment": 1               
                    }
                }
            ])
        
        hotel_comment_query = await hotel_comment_query.to_list(length=10000)
    except:
        pass

    comments = list(map(lambda x: x['comment'],hotel_comment_query[0]['comments']))

    return comments
