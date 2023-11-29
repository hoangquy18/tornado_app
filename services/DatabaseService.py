import json
import utils
from asyncio import create_task,gather,get_event_loop
import asyncio
from pymongo.errors import ServerSelectionTimeoutError
import sys
import utils

class DatabaseService:
    def __init__(self, db):
        self.db_collection = db

    async def get_region_dict(self) -> dict:
        try:
            region_dict =  self.db_collection['region'].find()
            region_dict = await region_dict.to_list(length=100)

        except ServerSelectionTimeoutError:
            raise ConnectionRefusedError("CANNOT CONNECT TO DATABASE!!!")

        return region_dict

    def get_region_list(self, region_dict) -> list:
        region_list = list(map(lambda x: x['region_name'],region_dict))
        return region_list
    
    async def get_hotel_dict(self) -> dict:
        try:
            hotel_dict = self.db_collection['hotel'].find()
            hotel_dict = await hotel_dict.to_list(length=1000)

        except ServerSelectionTimeoutError:
            raise ConnectionRefusedError("CANNOT CONNECT TO DATABASE!!!")

        return hotel_dict

    async def get_region_hotel_dict(self) -> dict:
        region_hotel_dict = {}

        region_dict = await self.get_region_dict()
        hotel_dict = await self.get_hotel_dict()

        region_list = self.get_region_list(region_dict)
        for region in region_list:
            reg_id = utils.find_id_region(region_dict,region)
            region_hotel_dict[region] = utils.find_hotel_in_region(hotel_dict,reg_id)

        return region_hotel_dict

    async def find_comment_hotel(self, hotel_dict, hotel_name):

        hotel_id = utils.find_id_hotel(hotel_dict,hotel_name)
        comments = []

        if hotel_id == -1:
            raise IndexError("THIS HOTEL NOT EXIST!!!")
        
        comment_hotel = self.db_collection['comment'].find({"hotel_id": hotel_id})
        comment_hotel = await comment_hotel.to_list(length=1000)
        
        for obj in comment_hotel:
            comments.append(obj['comment'])

        return comments
    
        