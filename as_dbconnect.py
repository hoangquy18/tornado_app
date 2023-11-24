from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import utils
import motor.motor_tornado
from asyncio import create_task,gather,get_event_loop
import asyncio
from pymongo.errors import ServerSelectionTimeoutError
import sys
import utils

class Database:
    def __init__(self, user_name, password,db_name):
        self.url = f"mongodb+srv://{user_name}:{password}@cluster0.vcb5k8u.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NONE"
        self.db_name = db_name

    async def get_database(self):
        """
            GET DATABASE FROM DB_NAME
        """
        client = motor.motor_tornado.MotorClient(self.url,serverSelectionTimeoutMS=2000)
        # try:
        #     print("Connection sucess!!!")
        #     z = client.server_info()
        # except:
        #     print("Unable to connect to the server!!!")
        return client[self.db_name]

    async def get_region_dict(self) -> dict:
        db_collection = await self.get_database()
        
        try:
            print("CONNECTING TO DATABASE...")
            region_dict =  db_collection['region'].find()
            region_dict = await region_dict.to_list(length=100)
            print("CONNECTION SUCCESSFUL!!!")
            print("===========================")

        except ServerSelectionTimeoutError:
            print("CANNOT CONNECT TO DATABASE!!!")
            sys.exit()
        return region_dict

    def get_region_list(self, region_dict) -> list:
        region_list = list(map(lambda x: x['region_name'],region_dict))
        return region_list
    
    async def get_hotel_dict(self) -> dict:
        db_collection = await self.get_database()

        try:
            print("CONNECTING TO DATABASE...")
            hotel_dict = db_collection['hotel'].find()
            hotel_dict = await hotel_dict.to_list(length=1000)
            print("CONNECTION SUCCESSFUL!!!")
            print("===========================")
        except ServerSelectionTimeoutError:
            print("CANNOT CONNECT TO DATABASE!!!")
            sys.exit()

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
        db_collection = await self.get_database()

        hotel_id = utils.find_id_hotel(hotel_dict,hotel_name)
        comments = []

        flag = ""
        if hotel_id == -1:
            flag = "THIS HOTEL NOT EXIST!!!"
            print(flag)
            return comments,flag
        
        print("FINDING COMMENT...")
        comment_hotel = db_collection['comment'].find({"hotel_id": hotel_id})
        comment_hotel = await comment_hotel.to_list(length=1000)
        if len(comment_hotel) == 0 :
            flag = "THIS HOTEL NOT HAVE COMMENT!!!"
            print(flag)
            return comments, flag
        
        for obj in comment_hotel:
            comments.append(obj['comment'])
        print("DONE!!!")
        print("===========================")

        return comments,flag
    
        