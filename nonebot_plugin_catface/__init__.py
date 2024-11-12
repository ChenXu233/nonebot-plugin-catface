from nonebot import on_command,require
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
require("nonebot_plugin_saa")
import nonebot_plugin_saa as saa

import os
import io
import base64
from PIL import Image

from pathlib import Path
from ultralytics import YOLO

MODEL_PATH = Path(os.path.dirname(__file__)) / "./models/last.pt"
CAT_NAMES = ["其他","英俊","黑巧","话梅","希特勒","丸子","奥利奥","咖喱","阿狸","斑比"]

MODEL = YOLO(MODEL_PATH.absolute())

which_cat = on_command("猫谱")

@which_cat.handle()
async def _(bot:Bot, event:MessageEvent):
    if not event.reply:
        await which_cat.finish("请回复猫猫照片来判断是不是有猫猫")
    message = event.reply.message
    msg = saa.Text("识别结果：")
    n = 0
    c = 0
    for i in message:
        if i.type == "image":
            img = await bot.get_image(file=i.data.get('file'))
            image_bytes = base64.b64decode(img['base64'])
            image_stream = io.BytesIO(image_bytes)
            image = Image.open(image_stream)
            results = MODEL.predict(image)
            result = results[0]
            result.save(os.path.dirname(__file__) + "/results.jpg")
            names_index = result.boxes.cls.tolist()
            for i in names_index:
                c += 1
                msg += saa.Text(CAT_NAMES[int(i)]+"\n")
            msg += saa.Image(os.path.dirname(__file__) + "/results.jpg")
            n += 1
    if n == 0:
        await which_cat.finish("没有找到图片")
    if c == 0:
        msg+= saa.Text("没有找到猫猫")
    await msg.finish()