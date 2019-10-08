# googlemap-collector
a python script to collect google map image and satelite imaga, finetuen from https://blog.csdn.net/u012866178/article/details/83188581. urls:https://www.cnblogs.com/janehlp/p/7821036.html
首先是脚本启动后的输入部分
pls input save path:E:/data（最后不要加/，我代码里加了）
pls input raw data zoom:11,12,13(低分辨率的zoom等级，可以输入单值或多值，中间用逗号分隔）
pls input aligned zoom: 13,14,15(高分辨率的zoom等级，可以输入单值或多值，中间用逗号分隔；有数值比低分辨zoom列表里小也不要紧）
pls input location:anywhere(这个就是写个文件名而已）
pls input lat_deg of lefttop：28.555（输入区域左上角纬度值）
pls input lon_deg of lefttop：120（同上经度）
pls input lat_deg of rightbottom:24(右下角纬度）
pls input lon_deg of rightbottom：118（右下角经度）
回车就开始跑了
会下载所有低分辨率的瓦片，然后根据低分辨率瓦片去下载高分辨率瓦片，然后合成跟低分辨率瓦片对齐的大图.文件夹结构的话，每一级别的小图(512*512)各有一个文件夹
小图合成的对齐大图会在对应的低zoom的文件夹下，影像地图分开，坐标文件在根文件夹下
