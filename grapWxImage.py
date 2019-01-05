#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
import re
import os
import time
from PIL import Image

def parseImageUrls(wxUrl):
    rsp = requests.get(wxUrl)
    imgs = re.findall(r'<p><img (.*?)></p>', rsp.text)
    imgUrls = []
    for img in imgs:
        data_src = re.search(r'data-src="(.*?)"', img)
        if data_src:
            imgUrls.append(data_src.group(1))

    return imgUrls

def download(imgUrls):
    # 当前目录下建立文件夹
    now_time = int(time.time())
    file_path = 'img_' + str(now_time)

    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        i = 1
        for url in imgUrls:
            rsp = requests.get(url)
            if rsp.status_code == 200:
                f = open(file_path + "/" + str(i) + ".jpeg", "wb")
                f.write(rsp.content)
                f.close()
            i += 1
    except IOError as e:
        print('文件操作错误', e)
    except Exception as e:
        print('错误', e)

    return file_path

def cropImgs(file_path):
    imgs = os.listdir(file_path)
    for img in imgs:
        path = file_path + "/" + img
        temp_img = Image.open(path)
        w, h = temp_img.size

        region = temp_img.crop((0, 52, w, h-65))
        region.save(path)

imgUrls = parseImageUrls('https://mp.weixin.qq.com/s/xND6fgbnEwjabu7KDYiiFg')
file_path = download(imgUrls)
cropImgs(file_path)

print('Images are saved in ' + file_path)
