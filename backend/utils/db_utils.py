import torch
import yaml

def load_db_config(config_path):
    with open(config_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded['database']

def load_model(path):
    check_point = torch.load(path,map_location=torch.device('cpu'))
    return check_point
