import threading
import concurrent.futures
import socket

def try_connect(params):
    host, port, open_ports, closed_ports = params
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((str(host), port))
        open_ports.append(port)
    except:
        closed_ports.append(port)
    finally:
        s.close()        
        
host = '192.168.1.1'        

start_port = 1
end_port = 100

open_ports = []
closed_ports = []

with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
    executor.map(try_connect, [(host, port, open_ports, closed_ports) for port in range(start_port, end_port + 1)])
   
print("Whats open:", open_ports)
print("Whats closed", closed_ports)    


