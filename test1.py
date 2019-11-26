import shutil
from multiprocessing import Pool
from multiprocessing import Manager
import multiprocessing
import os, tqdm,sys

import cv2


# 复制文件的方法
def copy_file(path, new_path):  # , q):
    for i in tqdm.tqdm(range(len(path))):
        shutil.copyfile(path[i], new_path[i])
        # q.put(path[i])


# 多线程复制文件
def run(datapath, savepath, threadnum):
    # if not os.path.exists(savepath):
    #     os.makedirs(savepath)
    data = os.listdir(datapath)
    filename = []
    new_filename = []
    # 根据zoom级别读取文件名，根据纵坐标与横坐标构建新的文件名
    for zoom in data:
        data_low = os.path.join(datapath, zoom)
        for x_low in os.listdir(data_low):  # 纵列
            for y_low in os.listdir(os.path.join(data_low, x_low)):  # 横行

                new_name = x_low + '_' + y_low
                new_path = os.path.join(os.path.join(savepath, str(zoom)), new_name)
                if not os.path.exists(os.path.join(savepath, str(zoom))):
                    os.makedirs(os.path.join(savepath, str(zoom)))
                filename.append(os.path.join(os.path.join(data_low, x_low), y_low))
                new_filename.append(new_path)

    pool = Pool(threadnum)  # threadnum开启线程的数量

    # q = Manager().Queue()
    n = int(len(filename) / 10)
    index = len(filename) % n
    for i in range(0, len(filename), n):
        pool.apply_async(copy_file, args=(filename[i:i + n], new_filename[i:i + n]))  # , q)) # 多线程运行

    if index < len(filename):
        copy_file(filename[index:], new_filename[index:])  # , q) # 将最后的少数图片补全

    # pool.close()
    # pool.join()
    # num = 0
    # allnum = len(filename)
    # while num < allnum:
    #     q.get()
    #     num += 1
    #     copyrate = int(num / allnum)
    #     print("\r 进度为：%.2f%%" % (copyrate * 100), end='')


def concat(save_path, dir2, zoomLow, zoomHigh, dir3):
    save_path = save_path + "\\streetmap\\streetmap" + str(zoomHigh) + "_" + str(zoomLow) + "_aligned"
    n = 2 ** (zoomHigh - zoomLow)
    if not os.path.exists(save_path):
        os.makedirs(save_path)  # 建立拼接后图片的存储位置
    save_path += "\\"
    filenames = os.listdir(dir3)  # dir3是zoomLow的文件夹
    for filename in filenames:  # 遍历zoomLOW图片
        try:
            if not os.path.exists(save_path + filename):  # 无拼接后的图片
                a = int(filename.find('_'))
                e = int(filename.find('.'))
                x = int(filename[0:a])  # 行
                y = int(filename[a + 1:e])  # 列
                x = x * n  # 乘以放大级别
                y = y * n
                imrow = []
                print(filename, end='')
                for a in range(0, n):
                    imcolumn = []
                    for e in range(0, n):
                        copyrate = (a * e) / (n * n)
                        sys.stdout.write("processing " + filename + "  %.2f%%  " % (copyrate * 100)+'\n')
                        file = dir2 + '\\' + str(x + a) + '_' + str(y + e) + '.png'
                        if os.path.exists(file):
                            im = cv2.imread(file)  # 读取列图片
                            imcolumn.append(im)
                        else:
                            a = (dir2 + '\\' + str(x + a) + '_' + str(y + e) + '.png').find('\\')
                            print((dir2 + '\\' + str(x + a) + '_' + str(y + e) + '.png')[a:] + "   don't exist")
                            raise Exception
                    imstripe = cv2.vconcat(imcolumn)  # 列拼接
                    imrow.append(imstripe)  # 将拼好的列放到行里
                imwhole = cv2.hconcat(imrow)  # cv2.hconcat(imrow) # 行拼接
                cv2.imwrite(save_path + filename, imwhole)  # 高分辨率地图合成对应的低分辨率地图
                print(save_path + filename)
        except Exception:
            continue


def concat_pict(datapath, savepath):
    import threading
    zoomLow = [min(int(x) for x in os.listdir(datapath))][0]
    zoomHighs = [int(x) for x in os.listdir(datapath)][1:]
    for zoomHigh in zoomHighs:
        t = multiprocessing.Process(target=concat(save_path=savepath,
                                           dir2=os.path.join(savepath, str(zoomHigh)),
                                           zoomLow=zoomLow, zoomHigh=zoomHigh,
                                           dir3=os.path.join(savepath, str(zoomLow))))
        t.start()


if __name__ == '__main__':
    datapath = 'E:\\map_concat\\data\\data\\googlemaps\\roadmap_nolabel'
    savepath = 'E:\\map_concat\\data\data_aligned'

    # run(datapath, savepath, threadnum=5)

    concat_pict(datapath=datapath, savepath=savepath)

    for zoom in os.listdir(os.path.join(savepath, "streetmap")):
        print(zoom, "的文件数量为：", len(os.listdir(os.path.join(os.path.join(savepath, "streetmap"), zoom))))
