import torch
import yaml

def load_db_config(config_path):
    with open(config_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded['database']

def find_id_region(region_dict,region_name):
    for i in range(len(region_dict)):
        if region_dict[i]['region_name'] == region_name:
            return region_dict[i]['id']
    return -1

def find_hotel_in_region(hotel_dict, region_id):
    rs = []
    for obj in hotel_dict:
        if obj['region_id'] == region_id:
            rs.append(obj['hotel_name'])
    return rs

def find_id_hotel(hotel_dict,hotel_name):
    for i in range(len(hotel_dict)):
        if hotel_dict[i]['hotel_name'].strip(" ") == hotel_name:
            return hotel_dict[i]['id']
    return -1

def load_model(path):
    check_point = torch.load(path,map_location=torch.device('cpu'))
    return check_point

async def find_comment_hotel(db_collection, hotel_dict, hotel_name):
    hotel_id = find_id_hotel(hotel_dict,hotel_name)
    
    comment_hotel = db_collection['comment'].find({"hotel_id": hotel_id})
    comment_hotel = await comment_hotel.to_list(length=1000)
    comments = []
    for obj in comment_hotel:
        comments.append(obj['comment'])
    return comments