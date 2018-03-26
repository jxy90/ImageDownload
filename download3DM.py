import os
import aiohttp
import asyncio
import urllib.request
from bs4 import BeautifulSoup

URL = "http://www.3dmgame.com/zt/201803/3724664.html"
STRATPAGE = 2
ENDPAGE = 60
FLODER =  URL.split("/")[-1].split(".")[0]
PATH = "C:\\Users\\jiang.xiaoyu\\Desktop\\"
FLODERPATH = PATH+FLODER+"\\"


def getHtml(url):
    html = ""
    try:
        page = urllib.request.urlopen(url)
        html = page.read().decode('utf-8')
    except Exception as err:
        print(err)
    finally:
        return html

def getAllHtml(url):
    if os.path.exists(FLODERPATH) == False:
        os.makedirs(FLODERPATH)
    htmlList = []
    html = getHtml(url)
    htmlList.append(html)
    for index in range(STRATPAGE, ENDPAGE):
        urltemp = url.split(".html")[0] + "_" + str(index) + ".html"
        print(urltemp)
        html = getHtml(urltemp)
        if html != "":
            htmlList.append(html)
        else:
            break
    return htmlList

async def getImg(html,pageIndex):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    async with aiohttp.ClientSession() as session:
        soup = BeautifulSoup(html)
        imgTagList = soup.select(".con img")
        # floder = imgTagList[0].get('src').split("/")[-2]
        imageindex = 1
        for imgTag in imgTagList:
            imageUrl = imgTag.get('src')
            imageName = imgTag.parent.parent.next_sibling.next_sibling.text
            ext = imageUrl[len(imageUrl)-3:]
            fileName = '%s_%s_%s.%s' % (pageIndex,imageindex, imageName, ext)
            # filePath = 'E:\Project\Python\IntelPython\%s' % fileName
            if os.path.exists(FLODERPATH+fileName):
                if os.path.getsize(FLODERPATH+fileName) != 0:
                    print(fileName)
                    imageindex += 1
                    continue
            
            async with session.get(imageUrl, headers=headers) as r:
                path = os.path.join(FLODERPATH, fileName)
                fp = open(path, 'wb')
                fp.write(await r.read())
                fp.close()
            print(fileName)
            imageindex += 1

def get_many(urls):

    loop = asyncio.get_event_loop()
    tasks = []
    pageIndex = 1
    for htmlitem in getAllHtml(URL):
        tasks.append(getImg(htmlitem, pageIndex))
        pageIndex = pageIndex + 1
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

get_many("3DM")