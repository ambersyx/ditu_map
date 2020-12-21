from urllib.parse import quote
from urllib import request
import json
import xlwt

# amap_web_key = 申请的密钥
amap_web_key = 'fb5b8974732a385a10e92d8c9581e71e'
poi_search_url = "http://restapi.amap.com/v3/place/text"
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"
#from transCoordinateSystem import gcj02_to_wgs84

# cityname为需要爬取的POI所属的城市名，nanning_areas为城市下面的所有区
cityname = '成都'
nanning_areas = ['青羊区']

# classes为多个分类名集合. (中文名或者代码都可以，代码详见高德地图的POI分类编码表)
# 01 = 汽车服务
# 12 = 商务住宅
classes = ['12']


# obtain poi by using constraits (cityname, nanning_areas, classes)
def getpois(cityname, keywords):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, i)
        print(result)
        result = json.loads(result)  # convert to json
        if result['count'] == '0':
            break
        hand(poilist, result)
        i = i + 1
    return poilist


#  write data into excel
def write_to_excel(poilist, cityname, classfield):
    # one Workbook object，create an excel file
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(classfield, cell_overwrite_ok=True)

    # the first line
    sheet.write(0, 0, 'x')
    sheet.write(0, 1, 'y')
    sheet.write(0, 2, 'count')
    sheet.write(0, 3, 'name')


    for i in range(len(poilist)):
        location = poilist[i]['location']
        name = poilist[i]['name']
        lng = str(location).split(",")[0]
        lat = str(location).split(",")[1]

        '''
        result = gcj02_to_wgs84(float(lng), float(lat))

        lng = result[0]
        lat = result[1]
        '''

        # write each line
        sheet.write(i + 1, 0, lng)
        sheet.write(i + 1, 1, lat)
        sheet.write(i + 1, 2, 1)
        sheet.write(i + 1, 3, name)


    book.save(r'' + cityname + "_" + classfield + '.xls')


def hand(poilist, result):
    # result = json.loads(result)  # convert to json text
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


# obtian pois, but every request can only crawl 900 pois
def getpoi_page(cityname, keywords, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    print(req_url)
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data


for clas in classes:
    classes_all_pois = []
    for area in nanning_areas:
        pois_area = getpois(area, clas)
        print('当前城区：' + str(area) + ', class：' + str(clas) + ", total amount:" + str(len(pois_area)) + "POIs")
        classes_all_pois.extend(pois_area)
    print("所有城区，total amout：" + str(len(classes_all_pois)))

    write_to_excel(classes_all_pois, cityname, clas)

    print('================class：'  + str(clas) + "write successfully")