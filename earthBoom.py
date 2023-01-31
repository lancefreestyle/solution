import requests
import time
from bs4 import BeautifulSoup
import openpyxl
# base64 解码此内容填充到下面 netUrl 变量中
# aHR0cDovL25ld3MuY2VpYy5hYy5jbi9pbmRleC5odG1sP3RpbWU9JXM=
netUrl = ''
def getSource():
    url = netUrl % str(int(time.time()))
    r = requests.get(url)
    if r.status_code == 200:
        # 设置编码格式 原格式为 ISO-8859-1
        r.encoding = 'utf-8'
        print('获取到数据 %s' % str(len(r.text)))
        return r.text


def analysisHtml(content):
    '''
    解析html 获取数据
    :param content:
    :return:
    '''
    soup = BeautifulSoup(content, 'lxml')
    contentDiv = soup.find(id="news")
    headList = []
    bodyList = []
    for i, trChild in enumerate(contentDiv.table.find_all(name='tr')):
        if i == 0:
            # 保存head头
            for th in trChild.find_all(name='th'):
                headList.append(th.text)
            continue
        tdList = []
        for td in trChild.find_all(name='td'):
            aTag = td.find_all(name='a')
            if len(td.find_all(name='a')) > 0:
                contentStr = aTag[0].text + ' ' + aTag[0]['href']
                tdList.append(contentStr)
            else:
                tdList.append(td.text)
        bodyList.append(tdList)

    return headList, bodyList


def writeExcel(heads, bodys):
    wb = openpyxl.Workbook()
    sh1 = wb.active
    sh1.append(heads)
    for tr in bodys:
        sh1.append(tr)
    wb.save(r'D:\data\target\earthBoom.xlsx')


if __name__ == '__main__':
    print('获取数据中....')
    source = getSource()
    print('获取完成!!!开始解析...')
    heads, bodys = analysisHtml(source)
    print('解析完成!!!,写入excel....')
    writeExcel(heads, bodys)
    print('写入完成!!!')
