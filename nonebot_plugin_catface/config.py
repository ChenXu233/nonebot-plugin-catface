from pydantic import BaseModel
from nonebot import get_driver, get_plugin_config

class ScopedConfig(BaseModel):
    cat_names = ['name']

class Config(BaseModel):
    cat_face: ScopedConfig
    

global_config = get_driver().config
plugin_config = get_plugin_config(Config).cat_face
