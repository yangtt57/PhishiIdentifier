import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from urllib.parse import urljoin
def get_screenshot_html(url):
    # 设置请求头
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 "
            "Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"
        )
    }

    # 要下载图片的目标网页
    # url = 'https://dna-id-xv-news.resmi69.my.id/'

    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--proxy-server="direct://"')
    chrome_options.add_argument('--proxy-server=http://127.0.0.1:10809')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--disable-client-side-phishing-detection')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--lang=en')
    # 设置ChromeDriver路径
    webdriver_service = Service('/usr/local/bin/chromedriver')  # 替换为你的chromedriver路径
    
    # 启动浏览器
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    browser.get(url)

    # 等待某个元素加载完成，例如等待id为'content'的元素加载完成
    WebDriverWait(browser, 5)

    # 获取页面高度
    page_height = browser.execute_script("return document.body.scrollHeight")
    viewport_height = browser.execute_script("return window.innerHeight")
    viewport_width = browser.execute_script("return document.body.scrollWidth")

    # 设置窗口大小为整个页面大小
    browser.set_window_size(viewport_width, page_height)

    # 截取整个网页的屏幕截图
    screenshot_path = 'screenshot.png'
    browser.save_screenshot(screenshot_path)
    print(f'Screenshot saved to {screenshot_path}')

    # print(html)
    # browser.quit()
    
    
if __name__ == '__main__':
    url = 'https://pub-5712cface28040c48f34ee3d3ee532c6.r2.dev/index.html'
    get_screenshot_html(url)



