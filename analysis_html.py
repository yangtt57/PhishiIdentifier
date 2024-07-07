import requests
from bs4 import BeautifulSoup
import re
import whois
from datetime import datetime
from urllib.parse import urlparse, urljoin
import esprima
# 获取网页内容的函数
def get_webpage_content(url, proxies=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1'  # Do Not Track Request Header
    }
    
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

# 获取源码中的文本
'''
判断有没有出现符合下述情况的关键词，如：
营造紧张感: "最后通牒", "过期", "立即行动", "账户冻结", "安全警告", "系统错误"
伪造身份: "官方", "客服", "技术支持", "安全团队", "银行代表", "获奖通知"
诱导点击: "点击这里", "了解更多", "更新信息", "领取奖品", "验证账户"
关键词上下文分析: 不要仅仅依靠关键词出现与否来判断，还要考虑其上下文语境。例如，"账户问题" 出现在银行官网的客服页面可能是正常的，但出现在一个伪造的登录页面就很可疑。
多语言分析: 可以从不同语言进行分析 
'''
def get_text(soup):
    text = soup.get_text().replace("\n",' ').replace('\t', " ") 
    cleaned_text = ' '.join(text.split())
    return cleaned_text

# 分析表单结构
'''
分析HTML中的表单结构和内容，在提交的内容中
url 指的是表单提交的目标URL， method指的是表单提交的方式，fields指的是表达中出现的字段
'''
def analyze_form(soup, url):
    forms = soup.find_all('form')
    domain = urlparse(url).hostname
    # print(domain)
    form_info = []
    # actions = []
    for form in forms:
        info = {}
        # 获取表单提交的目标URL
        action = form.get('action')
        info['url'] = action
        # 获取表单的提交方式
        method = form.get('method','').upper()
        info['method'] = method
        # 检查表单字段
        input_fields = form.find_all('input')
        fields = []
        for i,field in enumerate(input_fields):
            ft = field.get('type','').lower()
            fn = field.get('name')
            fi = field.get('id')
            fields.append(f"{i}. type: {ft}, name: {fn}, id: {fi}")
        info['fields'] = fields
        form_info.append(info)
    return form_info
    
# 分析链接
'''
分析源码中的链接
'''
def analyze_link(soup):
    links = soup.find_all('a', href = True)
    link_info = []
    for link in links:
        href = link['href']
        # 检查链接是否使用了 JavaScript 跳转
        if "javascript:" in href and "location.href" in href:
            # 提取跳转目标 URL
            match = re.search(r"location\.href\s*=\s*['\"](.*?)['\"]", href)
            if match:
                redirect_url = match.group(1)
                print(f"警告：发现 JavaScript 跳转到：{redirect_url}")
        link_info.append(link)
    return link_info

# 分析图片
'''
检查域名是否与当前网站域名一致，如果不一致，则该图片来自外部网站，需要提高警惕。
检查图片链接是否使用 HTTPS 协议: 即使图片来自合法域名， 也建议使用 HTTPS 协议加载图片，以防止图片内容被篡改。
分析图片 alt 属性:
检查 alt 属性是否为空。 合法的网站通常会为图片添加描述性 alt 属性， 而钓鱼网站可能忽略这一点。
检查 alt 属性是否包含可疑关键词， 例如与登录、账户、安全等相关的词汇。
'''
def analyze_img(soup):
    
    images = soup.find_all('img')
    imgs = []
    for img in images:
        img_src = img.get('src')
        # print(img)
        imgs.append(img)
    return imgs

# 分析iframe
'''
下面是网站源码中所有的iframe元素，你可以首先对其链接进行分析，然后可以根据需要对 iframe 内容进行更深入的分析，例如检查可疑元素、关键词等
'''
# 检查隐藏的 iframe
def check_hidden_iframes(soup):
    iframes = soup.find_all('iframe')
    hidden_iframes = []
    
    for iframe in iframes:
        style = iframe.get('style', '')
        width = iframe.get('width', 'auto')
        height = iframe.get('height', 'auto')
        
        if ('display: none' in style or 'visibility: hidden' in style or
            width == '0' or height == '0'):
            hidden_iframes.append(iframe)
    
    return hidden_iframes
# 提取JS
def extract_js_from_html_bs(soup):
  """使用 BeautifulSoup 从 HTML 代码中提取 JavaScript 代码。

  Args:
      html_content: HTML 代码字符串.

  Returns:
      一个列表，包含所有提取到的 JavaScript 代码片段。
  """
  js_code_snippets = []
  extern_js_link = []
  for script in soup.find_all('script'):
    if script.string:
      # 获取内联 JavaScript 代码
      js_code_snippets.append(script.string.strip())
    elif script.get('src'):
      # 获取外部 JavaScript 文件链接
    #   js_code_snippets.append(f"外部脚本: {script['src']}")
        extern_js_link.append(script['src'])
  return js_code_snippets,extern_js_link

def extract_functions(code):
    functions = []
    ast = esprima.parseScript(code, {
        'range': True,
        'loc': True,
        'tokens': True,
        'comment': True
    })
    
    for node in ast.body:
        if node.type == 'FunctionDeclaration':
            functions.append(node.id.name)
        elif node.type == 'VariableDeclaration':
            for declaration in node.declarations:
                if declaration.init and declaration.init.type == 'FunctionExpression':
                    functions.append(declaration.id.name)
        elif node.type == 'ClassDeclaration':
            for method in node.body.body:
                if method.type == 'MethodDefinition':
                    functions.append(method.key.name)
    
    return functions
# 检查重定向代码
def check_redirects(soup):
    redirects = []
    
    # Check for meta refresh tags
    meta_refresh = soup.find('meta', attrs={'http-equiv': 'refresh'})
    if meta_refresh:
        redirects.append(meta_refresh)
    
    # Check for JavaScript redirects
    scripts = soup.find_all('script')
    js_redirects = []
    js_redirect_patterns = [
        re.compile(r'window\.location\.href\s*=\s*["\']([^"\']+)["\']'),
        re.compile(r'document\.location\s*=\s*["\']([^"\']+)["\']')
    ]
    
    for script in scripts:
        if script.string:
            for pattern in js_redirect_patterns:
                if pattern.search(script.string):
                    js_redirects.append(script)
                    break
    
    redirects.extend(js_redirects)
    
    return redirects
if __name__ == '__main__':
    url = 'http://pub-498d8eaa61d44640a3e76392c814fc09.r2.dev/dse_sign.html'
    proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'https://127.0.0.1:10809'
    }   
    content = get_webpage_content(url)
    print(content)
    # # print(content)
    # soup = BeautifulSoup(content,'html.parser')
    # # print(analyze_iframe(soup))
    # js_code_snippets,extern_js_link = extract_js_from_html_bs(soup)
    # print(extern_js_link)
    