import socket
import ipaddress

class NetworkMonitor:
    def __init__(self):
        pass

    def discover_hosts(self, subnet):
        """Discover hosts in a subnet."""
        network = ipaddress.ip_network(subnet)
        hosts = []
        for host in network.hosts():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            try:
                s.connect((str(host), 80))  # Try to connect to the host on port 80
                hosts.append(str(host))
            except socket.error as e:
                pass  # If the connection fails, just move on to the next host
            finally:
                s.close()
        return hosts

if __name__ == "__main__":
    # Code to test the NetworkMonitor class
    monitor = NetworkMonitor()
    subnet = "10.112.23.0/24"
    discovered_hosts = monitor.discover_hosts(subnet)
    print(discovered_hosts)

