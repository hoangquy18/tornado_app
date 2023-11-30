from pipeline import pmodel, process_text
import utils
from transformers import AutoTokenizer,AutoModel
import torch
from underthesea import word_tokenize
import numpy as np

ASPECT = ["Facilities", "Service", "Public_area", "Location", "Food", "Room"]
POLARITY = ['None','Negative', "Neutral", "Positive"]
PRETRAINED_PATH = "vinai/phobert-base"

def load_model():
    try:
        checkpoint = torch.load("./text_model.pth",map_location=torch.device('cpu'))
        model = pmodel.MyModel(PRETRAINED_PATH,len(ASPECT),4)
        model.load_state_dict(checkpoint['model_state_dict'])
    except FileNotFoundError:
        raise FileNotFoundError("FILE NOT FOUND!!!")
    except:
        raise NotImplementedError("CANNOT LOAD MODEL!!!")
    return model

def preprocess_comments(comments):
    tnormalize = process_text.TextNormalize()

    comments = list(map(lambda x: "" if x == None else x,comments))
    comments = list(map(lambda x: process_text.convert_unicode(x),comments))
    comments = list(map(lambda x: tnormalize.normalize(x),comments)) 
    comments =  list(map(lambda x: " ".join(word_tokenize(x)),comments))  

    return comments

def predict(model, comments):
    output = []
    n_sample = len(comments)
    tokenizer = AutoTokenizer.from_pretrained(PRETRAINED_PATH)
    for i in range(n_sample):
        comment_tokenize = tokenizer(comments[i],padding='max_length', max_length = 150,truncation=True,return_tensors='pt')

        model_output = model(comment_tokenize)
        model_output = model(comment_tokenize)
        _, y_pred = torch.max(torch.nn.functional.softmax(model_output,dim=-1),dim=-1)
        y_pred = y_pred[0].detach().cpu()

        text_y_pred = []

        for i in range(len(y_pred)):
            if y_pred[i] != 0:
                asp = ASPECT[i]
                pol = POLARITY[y_pred[i]]
                text_y_pred.append(f"{asp}#{pol}")
        # print(text_y_pred)
        output.extend(text_y_pred)

    output = np.array(output)
    unique, counts = np.unique(output, return_counts=True)
    summary_dict = dict(zip(unique, counts))
    
    for k, v in summary_dict.items():
        summary_dict[k] = int(v)
    return summary_dict
    
async def wrapper_predict_from_selected(db,selected_hotel):
    hotel_dict = await db.get_hotel_dict()
    comments = await db.find_comment_hotel(hotel_dict,selected_hotel)
    
    
    model = load_model()
    out = predict(model, comments)
    return out
