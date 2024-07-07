from analysis_cert import *
from analysis_domain import *
from analysis_html import *
from analysis_url import *
from website_screenshot import *
from paddleOCR import *
import threading
from openai import OpenAI
from multiprocessing import Process, Manager
import sys
def collect_info(url, result_dict):
    proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'https://127.0.0.1:10809'
    }   
    content = get_webpage_content(url)
    phost='127.0.0.1'
    pport_s=10808
    url_info = analyze_url(url)
    print('url done')
    cert_info = get_cert(url,phost=phost,pport=pport_s)
    print('cert done')
    domain_info_ = domain_info(url)
    print('domain done')
    soup = BeautifulSoup(content,'html.parser')
    html_text = get_text(soup)
    form_info=analyze_form(soup,url)
    link_info=analyze_link(soup)
    img_info=analyze_img(soup)
    iframe_info=check_hidden_iframes(soup)
    redirect_info=check_redirects(soup)
    _ ,extern_js_link = extract_js_from_html_bs(soup)

    result_dict['url_info'] = url_info
    result_dict['cert_info'] = cert_info
    result_dict['domain_info_'] = domain_info_
    result_dict['html_text'] = html_text
    result_dict['form_info'] = form_info
    result_dict['link_info'] = link_info
    result_dict['img_info'] = img_info
    result_dict['iframe_info'] = iframe_info
    result_dict['redirect_info'] = redirect_info
    result_dict['extern_js_link'] = extern_js_link

def get_ocr(url,result_dict):
    print('begin ocr')
    get_screenshot_html(url)
    ocr_result=Ocr('./screenshot.png')
    result_dict['ocr_result'] = ocr_result

def test():
    # 截取网站图片并进行OCR
    print('begin ocr')
    get_screenshot_html(url)
    ocr_result=Ocr('./screenshot.png')
    print(ocr_result)

def ask_gemini(url):
    # 创建线程
    ocr_thread = threading.Thread(target=get_ocr, args=(url, result_dict))
    collect_info_thread = threading.Thread(target=collect_info, args=(url, result_dict))

    # 启动线程
    ocr_thread.start()
    collect_info_thread.start()

    # 等待线程完成
    ocr_thread.join()
    collect_info_thread.join()

    # 获取结果
    ocr_result = result_dict.get('ocr_result', None)
    url_info = result_dict.get('url_info', None)
    cert_info = result_dict.get('cert_info', None)
    domain_info_ = result_dict.get('domain_info_', None)
    html_text = result_dict.get('html_text', None)
    form_info = result_dict.get('form_info', None)
    link_info = result_dict.get('link_info', None)
    img_info = result_dict.get('img_info', None)
    iframe_info = result_dict.get('iframe_info', None)
    redirect_info = result_dict.get('redirect_info', None)
    extern_js_link = result_dict.get('extern_js_link', None)

    print("URL Info:", url_info)
    print("Certificate Info:", cert_info)
    print("Domain Info:", domain_info_)
    print("HTML Text:", html_text)
    print("Form Info:", form_info)
    print("Link Info:", link_info)
    print("Image Info:", img_info)
    print("IFrame Info:", iframe_info)
    print("Redirect Info:", redirect_info)
    print("External JS Link:", extern_js_link)
    print("OCR Result:", ocr_result)


def write_to_file(file_path, url, url_info, cert_info, domain_info_, html_text, form_info, link_info, img_info, iframe_info, redirect_info, extern_js_link, ocr_result):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"Target URL: {url}\n")
        file.write(f"URL Info: {url_info}\n")
        file.write(f"Certificate Info: {cert_info}\n")
        file.write(f"Domain Info: {domain_info_}\n")
        file.write(f"HTML Text: {html_text}\n")
        file.write(f"Form Info: {form_info}\n")
        file.write(f"Link Info: {link_info}\n")
        file.write(f"Image Info: {img_info}\n")
        file.write(f"IFrame Info: {iframe_info}\n")
        file.write(f"Redirect Info: {redirect_info}\n")
        file.write(f"External JS Link: {extern_js_link}\n")
        file.write(f"OCR Result: {ocr_result}\n")

url = sys.argv[1]
if url is None:
    print('Please give the target URL.\nUsage: python get_info.py <url>')
result_dict = {}
# 创建线程
ocr_thread = threading.Thread(target=get_ocr, args=(url, result_dict))
collect_info_thread = threading.Thread(target=collect_info, args=(url, result_dict))

# 启动线程
ocr_thread.start()
collect_info_thread.start()

# 等待线程完成
ocr_thread.join()
collect_info_thread.join()

# 获取结果
ocr_result = result_dict.get('ocr_result', None)
url_info = result_dict.get('url_info', None)
cert_info = result_dict.get('cert_info', None)
domain_info_ = result_dict.get('domain_info_', None)
html_text = result_dict.get('html_text', None)
form_info = result_dict.get('form_info', None)
link_info = result_dict.get('link_info', None)
img_info = result_dict.get('img_info', None)
iframe_info = result_dict.get('iframe_info', None)
redirect_info = result_dict.get('redirect_info', None)
extern_js_link = result_dict.get('extern_js_link', None)

write_to_file("output.txt", url, url_info, cert_info, domain_info_, html_text, form_info, link_info, img_info, iframe_info, redirect_info, extern_js_link, ocr_result)

    # ask_deepseek(url, ocr_result,url_info ,cert_info ,domain_info_ ,html_text ,form_info ,link_info ,img_info ,iframe_info ,redirect_info,extern_js_link )
    
