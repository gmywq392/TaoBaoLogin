# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time, random, requests, json

from get_qianniu_orders import QianNiuOrderCollector


class TBLogin(object):
    """淘宝登陆"""

    def __init__(self, username, password):
        self.browser = self.__init_browser()
        self.wait = WebDriverWait(self.browser, 10)
        # 输入用户名和密码
        self.username, self.password = username, password

    def __init_browser(self):  # 初始化浏览器驱动
        # 使用 geckodriver
        profile = webdriver.FirefoxProfile()
        # 启用 https 代理
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.ssl', '127.0.0.1')
        profile.set_preference('network.proxy.ssl_port', 8080)
        profile.update_preferences()
        # 添加下面两个参数防止 SSL 报错，参考自：https://www.guru99.com/ssl-certificate-error-handling-selenium.html#2
        profile.accept_untrusted_certs = True
        profile.assume_untrusted_cert_issuer = False
        self.browser = webdriver.Firefox(firefox_profile=profile)
        self.browser.maximize_window()
        return self.browser

    def send_key(self):  # 输入用户名和密码
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'TPL_username_1')))
        username.clear()
        username.send_keys(self.username)
        time.sleep(random.uniform(1.2, 2))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'TPL_password_1')))
        password.click()
        password.clear()
        password.send_keys(self.password)
        time.sleep(random.uniform(1.2, 2))
        login_button = self.wait.until(EC.presence_of_element_located((By.ID, 'J_SubmitStatic')))
        login_button.click()

    def login(self):  # 登陆
        self.browser.get('https://login.taobao.com/member/login.jhtml')
        change_login_met = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="密码登录"]')))
        change_login_met.click()
        self.send_key()

    def get_cookies(self):  # 获得登陆后的cookies,保存为字典
        cookies = self.browser.get_cookies()
        # 格式化 cookies 为字典
        item = {}
        for cookie in cookies:
            item[cookie['name']] = cookie['value']
        return item