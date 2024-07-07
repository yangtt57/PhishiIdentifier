import whois
from datetime import datetime

def domain_info(domain):
    try:
        domain_info = whois.whois(domain)
        return domain_info
        
        # 检查域名注册时间
        if isinstance(domain_info.creation_date, list):
            creation_date = domain_info.creation_date[0]
        else:
            creation_date = domain_info.creation_date
        
        if creation_date:
            age_in_days = (datetime.now() - creation_date).days
            if age_in_days < 180:  # 设定为6个月
                print("  Warning: Domain age is less than 6 months, potential phishing risk.")
        
        # 检查域名所有者信息
        if domain_info.registrar is None:
            print("  Warning: Domain registrar information is missing, potential phishing risk.")
    except Exception as e:
        print(f"Error retrieving whois information: {e}")

if __name__ == "__main__":
    hostname = "http://pub-498d8eaa61d44640a3e76392c814fc09.r2.dev/dse_sign.html"
    domain_info_ = domain_info(hostname)
    print(domain_info_)
'''
分析注册信息，找出可疑特征
新注册域名： 钓鱼网站通常生命周期较短，域名注册时间很可能在最近几天或几周内。你可以检查 creation_date 是否在某个时间阈值内。
域名即将到期： 一些钓鱼网站可能会使用即将到期的域名，以便在被发现后快速转移。你可以检查 expiration_date 是否距离当前时间很近。
使用隐私保护服务： 很多钓鱼网站会利用域名隐私保护服务隐藏注册人信息，避免被追踪。你可以检查 registrant 信息是否包含隐私保护服务的标识符，例如 "Domains By Proxy"、"WhoisGuard" 等。
注册信息不完整： 一些钓鱼网站的注册信息可能不完整或明显是虚假的。你可以检查 registrant 信息是否存在缺失或异常。
高风险域名注册商/服务器： 一些域名注册商或服务器可能更容易被用于注册钓鱼网站。
'''