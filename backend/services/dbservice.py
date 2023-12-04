from pymongo.errors import ServerSelectionTimeoutError
from utils.dbconnection import DatabaseConnection
from repos import comment_repos, hotel_repos, region_repos

class DatabaseService:
    def __init__(self):
        self.db_collection = DatabaseConnection.get_connection()

    async def get_region(self) -> dict:
        region_dict = await region_repos.get_region_dict(self.db_collection)
        return region_dict
    
    async def get_hotel(self) -> dict:
        hotel_dict = await hotel_repos.get_hotel_dict(self.db_collection)
        return hotel_dict

    async def get_region_hotel(self) -> dict:
        region_hotel_dict = await region_repos.get_region_hotel_dict(self.db_collection)
        return region_hotel_dict

    async def get_comment_hotel(self, hotel_dict, hotel_name):
        comments = await comment_repos.find_comment_hotel(self.db_collection, hotel_dict,hotel_name)
        return comments
    
        