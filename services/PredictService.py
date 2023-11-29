from pipeline.pipeline import *

class PredictService:
    def __init__(self,db_service,selected_hotel):
        self.db_service = db_service
        self.selected_hotel = selected_hotel

    async def wrapper_predict_from_selected(self,):
        hotel_dict = await self.db_service.get_hotel_dict()
        comments,flag = await self.db_service.find_comment_hotel(hotel_dict,self.selected_hotel)
        
        if flag != "":
            return None, flag
        else:
            model = load_model()
            out = predict(model, comments)
            return out, ""
