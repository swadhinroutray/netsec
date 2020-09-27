import subprocess
import sys, socket,ssl
from subprocess import PIPE,Popen
import flask
from flask_cors import CORS,cross_origin
app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)

# url  = "google.com"

# file ="SCAN.txt"
def checkTLSv1(name,dict):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    try:
        with socket.create_connection((name,443)) as sock:
            with context.wrap_socket(sock,server_hostname=name) as ssl_sock:
                 dict.update({'TLSv10':1})
               # print(ssl_sock.version())
    except:
        dict.update({'TLSv10':0})
        print(ssl.SSLError)
def checkTLSv1_1(name,dict):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
    try:
        with socket.create_connection((name,443)) as sock:
            with context.wrap_socket(sock,server_hostname=name) as ssl_sock:
                dict.update({'TLSv11':1})
                # print(ssl_sock.version())
    except:
        dict.update({'TLSv11':0})
        print(ssl.SSLError)
def checkTLSv1_2(name,dict):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    try:
        with socket.create_connection((name,443)) as sock:
            with context.wrap_socket(sock,server_hostname=name) as ssl_sock:
                dict.update({'TLSv12':1})
                # print(ssl_sock.version())
    except:
        dict.update({'TLSv12':0})
        print(ssl.SSLError)
def writeScan(url,dict):
    output = open("SCAN.txt", "w")
    try:
        command = "pysslscan scan --scan=protocol.http --scan=vuln.heartbleed --scan=server.renegotiation --scan=server.preferred_ciphers --scan=server.ciphers --report=term:rating=ssllabs.2009e --ssl2 --ssl3 --tls10 --tls11 --tls12 " + url
        print(command.split())
       
        ciphers = subprocess.check_output(command.split())

        data = ciphers.decode('utf-8')
        # print(data)
        output.write(data)
    except:
        print("Error")
@app.route('/',methods=['GET'])
def index():
    return app.send_static_file('index.html')

@app.route('/check', methods=['GET'])
@cross_origin()
def checkVersions():
    # url = flask.request.args['url']
   
    reqData = flask.request.get_json(force=True)
    # url = flask.request.form.get('URL',None).strip()
    # print(url)
    print(reqData)
    print(reqData['url'])
    url = reqData['url'].strip()
    try:
        dict ={}
        writeScan(url,dict)
        response = subprocess.call(['./clean.sh'])
        # output = open('scan.csv',"w+")
        data =  open('finalResult.txt',"r")
        found_type = False
        for line in data:
            if 'Preferred Server Cipher(s)' in line:
                found_type = True
                continue                    

            if found_type:
                if 'Session' in line:
                   found_type = False               
                else:  
                    print(line.split())
                    if line.split()[1] == 'Protocol':  
                        # output.write(line.split()[0]+" 0"+"\r")
                        dict.update({line.split()[0]:0})
                    else:
                        dict.update({line.split()[0]:1})
                        # output.write(line.split()[0]+" 1"+"\r")

        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.options |= ssl.OP_NO_TLSv1_2 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1

        try:
            with socket.create_connection((url,443)) as sock:
                with context.wrap_socket(sock,server_hostname=url) as ssl_sock:
                    dict.update({'TLSv13':1})
                    # output.write("TLSv13 1"+"\r")
            if 'TLSv10' not in dict:    
                checkTLSv1(url,dict)
            if 'TLSv11' not in dict:    
                checkTLSv1_1(url,dict)
            if 'TLSv12' not in dict:   
                checkTLSv1_2(url,dict)
            if 'SSLv3' not in dict:
                dict.update({'SSLv3':0})

        except:
            dict.update({'TLSv13':0})
            # output.write("TLSv13 0"+"\r")
            print(ssl.SSLError)
    except:
        print("error")
    return dict
    
app.run()