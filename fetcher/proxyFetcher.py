# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: proxyFetcher
-------------------------------------------------
"""
__author__ = 'JHao'

import re
from time import sleep

from util.webRequest import WebRequest


class ProxyFetcher(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy01():
        """
        无忧代理 http://www.data5u.com/
        几乎没有能用的
        :return:
        """
        url_list = [
            'http://www.data5u.com/',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml'
        ]
        key = 'ABCDEFGHIZ'
        for url in url_list:
            html_tree = WebRequest().get(url).tree
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                try:
                    ip = ul.xpath('./span[1]/li/text()')[0]
                    classnames = ul.xpath('./span[2]/li/attribute::class')[0]
                    classname = classnames.split(' ')[1]
                    port_sum = 0
                    for c in classname:
                        port_sum *= 10
                        port_sum += key.index(c)
                    port = port_sum >> 3
                    yield '{}:{}'.format(ip, port)
                except Exception as e:
                    print(e)

    @staticmethod
    def freeProxy02():
        """
        代理66 http://www.66ip.cn/
        :return:
        """
        url = "http://www.66ip.cn/mo.php"

        resp = WebRequest().get(url, timeout=10)
        proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})', resp.text)
        for proxy in proxies:
            yield proxy

    @staticmethod
    def freeProxy03(page_count=1):
        """
        西刺代理 http://www.xicidaili.com  网站已关闭
        :return:
        """
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url = each_url + str(i)
                tree = WebRequest().get(page_url).tree
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        pass

    @staticmethod
    def freeProxy04():
        """
        全网代理 http://www.goubanjia.com/
        :return:
        """
        url = "http://www.goubanjia.com/"
        tree = WebRequest().get(url).tree
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                        and not(contains(@style, 'display:none'))
                                        and not(contains(@class, 'port'))
                                        ]/text()
                                """

        # port是class属性值加密得到
        def _parse_port(port_element):
            port_list = []
            for letter in port_element:
                port_list.append(str("ABCDEFGHIZ".find(letter)))
            _port = "".join(port_list)
            return int(_port) >> 0x3

        for each_proxy in proxy_list:
            try:
                ip_addr = ''.join(each_proxy.xpath(xpath_str))
                port_str = each_proxy.xpath(".//span[contains(@class, 'port')]/@class")[0].split()[-1]
                port = _parse_port(port_str.strip())
                yield '{}:{}'.format(ip_addr, int(port))
            except Exception:
                pass

    @staticmethod
    def freeProxy05(page_count=1):
        """
        快代理 https://www.kuaidaili.com
        """
        url_pattern = [
            'https://www.kuaidaili.com/free/inha/{}/',
            'https://www.kuaidaili.com/free/intr/{}/'
        ]
        url_list = []
        for page_index in range(1, page_count + 1):
            for pattern in url_pattern:
                url_list.append(pattern.format(page_index))

        for url in url_list:
            tree = WebRequest().get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            sleep(1)  # 必须sleep 不然第二条请求不到数据
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def freeProxy06():
        """
        代理盒子 https://proxy.coderbusy.com/
        :return:
        """
        urls = ['https://proxy.coderbusy.com/zh-hans/ops/country/cn.html']
        for url in urls:
            tree = WebRequest().get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            for tr in proxy_list[1:]:
                proxy = '{}:{}'.format("".join(tr.xpath("./td[1]/text()")).strip(),
                                       "".join(tr.xpath("./td[2]//text()")).strip())
                if proxy:
                    yield proxy

    @staticmethod
    def freeProxy07():
        """
        云代理 http://www.ip3366.net/free/
        :return:
        """
        urls = ['http://www.ip3366.net/free/?stype=1',
                "http://www.ip3366.net/free/?stype=2"]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy08():
        """
        IP海 http://www.iphai.com/free/ng
        :return:
        """
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy09(page_count=1):
        """
        http://ip.jiangxianli.com/?page=
        免费代理库
        :return:
        """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?country=中国&page={}'.format(i)
            html_tree = WebRequest().get(url).tree
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()

    # @staticmethod
    # def freeProxy10():
    #     """
    #     墙外网站 cn-proxy
    #     :return:
    #     """
    #     urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    # @staticmethod
    # def freeProxy11():
    #     """
    #     https://proxy-list.org/english/index.php
    #     :return:
    #     """
    #     urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
    #     request = WebRequest()
    #     import base64
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
    #         for proxy in proxies:
    #             yield base64.b64decode(proxy).decode()

    # @staticmethod
    # def freeProxy12():
    #     urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    @staticmethod
    def freeProxy13(max_page=2):
        """
        http://www.89ip.cn/index.html
        89免费代理
        :param max_page:
        :return:
        """
        base_url = 'http://www.89ip.cn/index_{}.html'
        for page in range(1, max_page + 1):
            url = base_url.format(page)
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(
                r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
                r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    @staticmethod
    def freeProxy14():
        """
        http://www.xiladaili.com/
        西拉代理
        :return:
        """
        urls = ['http://www.xiladaili.com/putong/',
                "http://www.xiladaili.com/gaoni/",
                "http://www.xiladaili.com/http/",
                "http://www.xiladaili.com/https/"]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", r.text)
            for ip in ips:
                yield ip.strip()

    @staticmethod
    def freeProxy15():
        """
        http://ip.ihuan.me/
        小幻HTTP代理
        :return:
        """
        urls = ['https://ip.ihuan.me/address/5Lit5Zu9.html?page=b97827cc',
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=4ce63706",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=5crfe930",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=f3k1d581",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=ce1d45977",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=881aaf7b5",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=eas7a436",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=981o917f5",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=2d28bd81a",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=a42g5985d",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=came0299",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=e92k59727",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=242r0e7b5",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=bc265a560",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=622b6a5d3",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=ae3g7e7aa",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=b01j07395",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=68141a2df",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=904545743",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=0134c4568",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=885t249e8",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=ed442164b",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=806fe4987",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=0558da7f4",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=3734334de",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=636g6d8ca",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=3252d86d1",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=d67sbb99f",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=0e1q9e209",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=078e9d9eb",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=476p30758",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=9520ab2cf",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=cd7772718",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=669i449ed",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=7c7l8a702",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=637sa470e",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=645pdd5b9",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=e25uc357c",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=c19of28a3",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=5fa0ad8bb",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=eabh0997c",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=026i27546",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=859ddf7d1",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=33b0f488f",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=602q622b1",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=75bge08a1",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=562ud6274",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=943073281",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=dec88f8ec",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=bdauca7c9",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=8dcoec821",
                "https://ip.ihuan.me/address/5Lit5Zu9.html?page=fa84ca5bd"]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(
                r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
                r.text)
            for proxy in proxies:
                yield ':'.join(proxy)
