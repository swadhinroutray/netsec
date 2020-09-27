import socket


def portIsOpen(ip_add, port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    location = (ip_add,port)
    try:
     check_port = s.connect_ex(location)
     if check_port == 0:
        print("Port " + str(port) + " open")
        return
     print ("Port " + str(port) +" closed")
    finally:
        s.close()

if __name__ == '__main__':
    ip_add = input("Enter IP ")
    file = open('ports.txt','r')
    f = file.readlines()
    port_list = []
    for ports in f:
        if ports[-1] == '\n':
            port_list.append(ports[:-1])
        else:
            port_list.append(ports)
    print("Ports to be checked: \n")
    print(port_list)

    for port_num in port_list:
        portIsOpen(ip_add,int(port_num))
    print("\nCheck Complete")