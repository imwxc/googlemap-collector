from urllib import request
import re
import urllib.request
import os
import random
import math

agents = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1']


# 经纬度反算切片行列号 3857坐标系
def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


# 下载图片
def getimg(Tpath, Spath, x, y):
    a = 0
    for a in range(0, 7):
        try:
            f = open(Spath, 'wb')
            req = urllib.request.Request(Tpath)
            req.add_header('User-Agent', agents[a])  # 换用随机的请求头
            pic = urllib.request.urlopen(req, timeout=60)
            f.write(pic.read())
            f.close()
            print(str(x) + '_' + str(y) + 'downloading success')
            break
        except Exception:
            print(str(x) + '_' + str(y) + 'downloading fail,retrying')
            print('retrying' + str(a + 1))
            continue



if __name__ == "__main__":
    for zoom in [17]:
        path = r"/home/machine/code/dataset/sateliteimageNY" + str(zoom)
        if not os.path.exists(path):
            os.mkdir(path)

    # 下载切片的zoom
        lefttop = deg2num(40.839593, -74.116635, zoom)  # 下载切片的左上角角点
        rightbottom = deg2num(40.600591, -73.769079, zoom)

        print(str(lefttop[0]))
        print(str(rightbottom[0]))
        print(str(lefttop[1]))
        print(str(rightbottom[1]))
        print("共" + str(lefttop[0] - rightbottom[0]))
        print("共" + str(lefttop[1] - rightbottom[1]))

        for x in range(lefttop[0], rightbottom[0]):
            for y in range(lefttop[1], rightbottom[1]):
                c = os.path.join(path, str(x) + "_" + str(y) + ".png")
                if os.access(c, os.F_OK) == True:
                    print ( str(c) + 'has been downloaded')
                    continue
                else:
                    tilepath = "http://mt2.google.cn/vt/lyrs=s&scale=2&hl=zh-CN&gl=cn&x=" + str(x) + "&y=" + str(y) + "&z=" + str(zoom) \
                    + "&apistyle=s.t:0|s.e:l|p.v:off"
            # 天地图的url 可以换成谷歌地图的
                    getimg(tilepath, os.path.join(path, str(x) + "_" + str(y) + ".png"), x, y)


            #ret = os.access(path, os.F_OK)
                #for retrying in range(1, 10):
                    #if os.access(path, os.F_OK) == False:
                        #print('retrying' + str(retrting))
                        #getimg(tilepath, os.path.join(path, str(x) + "_" + str(y) + ".png"), x, y)
                    #else:
                        #break

    print('completed')