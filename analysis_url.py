from urllib.parse import urlparse


def analyze_url(url):
    parsed_url = urlparse(url)
    url_info = {}
    if parsed_url.scheme: 
        url_info['Scheme'] = parsed_url.scheme
        # print(f"Scheme: {parsed_url.scheme}") 
    if parsed_url.netloc: 
        url_info['Netloc']=parsed_url.netloc
        # print(f"Netloc: {parsed_url.netloc}") # 包含域名和端口
    if parsed_url.path: 
        url_info['Path']=parsed_url.path
        # print(f"Path: {parsed_url.path}")
    if parsed_url.params: 
        url_info['Params']=parsed_url.params
        # print(f"Params: {parsed_url.params}")
    if parsed_url.query: 
        url_info['Query']=parsed_url.query
        # print(f"Query: {parsed_url.query}")
    if parsed_url.fragment: 
        url_info['Fragment']=parsed_url.fragment
        # print(f"Fragment: {parsed_url.fragment}")
    return url_info
# analyze_url()
'''
基于 URL 的检测 主要依赖于分析 URL 的不同组成部分，寻找可能暗示其为钓鱼网站的可疑模式。以下是一些常用的分析方法和特征：
1. 分析域名：
域名长度： 钓鱼网站域名可能较长且复杂，试图模仿知名品牌或公司，但仔细观察会发现细微差别。
顶级域名 (TLD)： 钓鱼网站可能会使用与合法网站相似的 TLD，例如 ".net" 而不是 ".com"，或者使用一些不太常见的 TLD，例如 ".cc" 或 ".info"。
子域名： 钓鱼网站可能会在 URL 中使用多个子域名，以使其看起来更真实，但实际上是为了混淆用户。例如，使用 "login.google.phishing.com" 而不是 "login.google.com"。
域名相似度： 钓鱼网站可能会注册与合法网站非常相似的域名，例如使用字母替换、添加或删除字符等方式，例如 "gooogle.com" 或者 "amaz0n.com"。
2. 分析路径和文件名：
目录结构： 钓鱼网站的 URL 路径可能与合法网站不一致，或者包含一些不必要的目录层级。
文件名： 钓鱼网站可能会使用与合法网站相似的文件名，但内容完全不同，例如 "login.html" 或 "account.php"。
3. 分析 URL 参数：
参数数量： 钓鱼网站的 URL 可能包含大量参数，这些参数可能被用于收集用户信息或进行其他恶意活动。
参数名称和值： 钓鱼网站可能会使用与合法网站相似的参数名称，但参数值可能包含恶意代码或用于进行网络钓鱼攻击。
'''