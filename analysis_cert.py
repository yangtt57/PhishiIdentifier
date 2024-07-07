# 获取网站的证书信息
import ssl
import socket
import OpenSSL
from datetime import datetime

import OpenSSL.crypto
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import socks 
from urllib.parse import urlparse

def get_cert(url, port=443, phost=None, pport=None):
    hostname  = urlparse(url).hostname
    context = ssl.create_default_context()
    if phost and pport:
        socks.set_default_proxy(socks.SOCKS5, phost, pport)
        socket.socket = socks.socksocket
    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert_bin = ssock.getpeercert(True)
                cert = ssl.DER_cert_to_PEM_cert(cert_bin)
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,cert)

                cert_info = {
                    'Issuer': {k.decode(): v.decode() for k, v in x509.get_issuer().get_components()},
                    'Subject': {k.decode(): v.decode() for k, v in x509.get_subject().get_components()},
                    'Serial Number': x509.get_serial_number(),
                    'Not Before': datetime.strptime(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ'),
                    'Not After': datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ'),
                    # 'Public Key': x509.get_pubkey().to_cryptography_key().public_bytes(
                    #     encoding=Encoding.PEM,
                    #     format=PublicFormat.SubjectPublicKeyInfo
                    # ).hex()
                }
                return cert_info
    except(socket.error, ssl.SSLError) as e:
        print(f"Error fetching certificate for {hostname}: {e}")
        return None

if __name__ == "__main__":
    hostname = "http://discord.pyun.cc/"
    phost = "127.0.0.1"
    pport = 10808
    cert_info = get_cert(url=hostname, phost=phost, pport= pport)
    if cert_info:
        print(cert_info)
    else:
        print("cannot get certificate infomation.")