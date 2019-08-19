# -*- coding:utf-8 -*-
import requests, json


class QianNiuOrderCollector(object):

    def __init__(self, cookies) -> None:
        self.cookies = cookies

    def get_page(self, page, dateBegin, dateEnd, page_size=15):
        """得到分页数据"""
        print('开始爬取第 %s 页的数据(每页%s条)' % (page, page_size))
        order_url = 'https://trade.taobao.com/trade/itemlist/asyncSold.htm?event_submit_do_query=1&_input_charset=utf8'
        headers = {
            'authority': 'trade.taobao.com',
            'method': 'POST',
            'path': '/trade/itemlist/asyncSold.htm?event_submit_do_query=1&_input_charset=utf8',
            'scheme': 'https',
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-length': '292',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 每天跑新数据时更新cookie信息，从浏览器登陆账号后复制过来
            # 'cookie': '',
            'referer': 'https://trade.taobao.com/trade/itemlist/list_sold_items.htm?spm=a1z02.1.1997525073.3.6307782dKPjdku',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        # 构建筛选数据
        data = {
            'auctionType': ' 0',
            'close': ' 0',
            'pageNum': page,
            'pageSize': page_size,
            'queryMore': 'false',
            'rxAuditFlag': '0',
            'rxElectronicAllFlag': ' 0',
            'rxElectronicAuditFlag': ' 0',
            'rxHasSendFlag': ' 0',
            'rxOldFlag': ' 0',
            'rxSendFlag': ' 0',
            'rxSuccessflag': ' 0',
            'tradeTag': ' 0',
            'useCheckcode': ' false',
            'useOrderInfo': ' false',
            'errorCheckcode': ' false',
            'action': ' itemlist / SoldQueryAction',
            # 筛选开始时间 把日期转为时间戳
            'dateBegin': dateBegin,
            # 截止时间
            'dateEnd': dateEnd,
            'prePageNo': (page - 1)
        }
        response = requests.post(url=order_url, cookies=self.cookies, headers=headers, data=data)
        return response

    def get_orders(self, p, flag):
        res = []
        resp = self.get_page(page=p, dateBegin=1560924861, dateEnd=0)
        orders_dictx = json.loads(resp.content.strip().decode('gbk'))
        pages = orders_dictx['page']['totalPage']
        res.extend(orders_dictx['mainOrders'])
        if flag == 0:
            for p in range(p + 1, pages + 1):
                res.extend(self.get_orders(p, 1))
        return res
