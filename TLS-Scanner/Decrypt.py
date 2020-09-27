from socket import socket
import ssl
import OpenSSL
from cryptography import x509
from cryptography.hazmat.backends import default_backend
data= ssl.get_server_certificate(('www.linkedin.com', 443))
# print(cert)
cert = OpenSSL.crypto.load_certificate(
      OpenSSL.crypto.FILETYPE_PEM,
      data
)
# data = x509.load_pem_x509_certificate(cert,default_backend())
# print(x509.get_subject().get_components())
data = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_TEXT, cert)
print(data)
file1 = open('certificate.txt','w')
file1.writelines(data.decode('utf-8'))
