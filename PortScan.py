import threading
import socket
import concurrent.futures


# shit works

class PortScan():
    def __init__ (self):
        self.open_ports = []
        self.closed_ports = []
        
        
    def connect_port(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        
        try:
            s.connect((str(host), port))
            self.open_ports.append(port)
        except (ConnectionRefusedError, OSError):
            self.closed_ports.append(port)
        finally:
            s.close()
            
            
    def scan_ports(self, host, start_port=1, end_port=1024, ports=None):
        if ports is None:
            ports = range(start_port, end_port + 1) #optional parameter
            
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            executor.map(self.connect_port, [host] * len(ports), ports)
        print("Open ports:", self.open_ports)
        print("Closed ports:", self.closed_ports)
                        
call = PortScan()
call.scan_ports("192.168.1.1", ports=[80, 443]) # or call.scan_ports("IP"), start_port=123, end_port=126)
