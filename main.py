# 导入
import bs4      # BeautifulSoup4
import urllib3  # 网络请求库，用于下载网页内容
import sys      # 系统库，这里只用于退出程序

targetUrl = 'https://www.bilibili.com/v/popular/rank/all'   # 哔哩哔哩排行榜的网址
http = urllib3.PoolManager()                                # 使用urllib3时，为了发起网络请求，需要建立一个池，池可以重用网络连接来循环利用系统资源

# http请求头，如果不标识User-Agent(类似浏览器种类)的话，哔哩哔哩不会响应内容
headers={"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}

# 若是当成文件来执行
if __name__ == '__main__':
    # 参数1: (HTTP)请求方法(GET方法为获取内容) 参数2: 请求地址 返回值: 服务器响应 合： 请求排行榜的网页内容
    response = http.request('GET', targetUrl, headers=headers)

    if response.status != 200:  # 服务器响应状态码200即为请求成功，这里不处理网络不连通的异常
        print('请求网址失败')
        sys.exit(0) # 退出程序
    
    # 从响应中读取数据内容并按UTF-8字符编码处理
    data = response.data.decode('utf-8')

    # 创建BeautifulSoup对象对网页内容进行解析，使用html.parser进行解析
    bs = bs4.BeautifulSoup(data, 'html.parser')

    # 用CSS选择器查找出每个排行榜项目，items为一个列表
    items = bs.select('.rank-list .content')

    # 遍历items，enumerate函数把items列表包装成一个可以遍历索引和内容的对象（直接遍历列表不能读出索引），索引还是原来列表的索引，内容还是原来列表的内容
    for ranking, item in enumerate(items):
        # 继续查找，".info"选择到的元素内有视频信息，a标签是链接元素的标签名
        # 由于网页就是这么设计的，所以这里只会查找出一个结果，所以对于一个列表的返回值，直接取第零个就行
        a = item.select('.info a')[0]

        # href属性指示了视频的链接（格式为https://www.bilibili.com/video/BV号），标签的内容是标题
        link = a.attrs.get('href')
        title = a.text

        # 取BV号 字符串[起始下标:]可以取字符串在起始下标后的内容 字符串.find(子字符串) 可以查找到在字符串里第一次出现子字符串的下标（下标在子字符串前）
        bvcode = link[link.find('BV'):]

        # 输出，字符串格式化
        print('排行在{}的视频：{}, BV号: {}'.format(ranking + 1, title, bvcode))
        # 和以下代码同理
        # print('排行在', ranking + 1, '的视频：', title, 'BV号: ', bvcode)


