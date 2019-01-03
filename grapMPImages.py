#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import requests

import re
def getImageUrls(webUrl):
    rsp = requests.get(webUrl)
    divs = re.findall(r'<div class="img-box well img-box-bg offline-preview">(\s*.*\s*?)</div>', rsp.text)
    imgs = []
    for div in divs:
        img = re.search(r'<img show-img="(.*?)" src=', div).group(1)
        imgs.append(img)
    return imgs

import time
import os
def downloadImgs(imgUrls):
    # 创建保存目录
    nowTime = int(time.time())
    dir = 'image_' + str(nowTime)
    if os.path.exists(dir) == False:
        os.makedirs(dir)

    i = 1
    for url in imgUrls:
        rsp = requests.get(url)
        f = open(dir + '/' + str(i) + '.jpg', 'wb')
        f.write(rsp.content)
        f.close()
        i = i + 1







imgUrls = getImageUrls('https://www.meipian.cn/ppppkgg?share_from=others&share_user_mpuuid=75c41d07a03f47872132618707c6c4fe&v=4.8.0')
downloadImgs(imgUrls)
