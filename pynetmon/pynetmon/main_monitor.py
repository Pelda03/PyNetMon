import ipaddress
import socket
import threading
from .protocols import http

# SPAGHETTI CODE ALERT - This is a very basic implementation of a network monitor
TODO = "Implment a less spaghetti code version of this class AND separate each method into its own class"
class NetworkMonitor:
    def __init__(self):
        self.discovered_hosts = []
        self.failed_hosts = []
        self.open_ports = []
        self.closed_ports = []

    def try_connect(self, host, port):
        """
        Attempt to connect to a host on a specific port.

        This method tries to establish a TCP connection to the specified host on the specified port. 
        If the connection is successful, the host is added to the list of discovered hosts. 
        If the connection fails, the host is added to the list of failed hosts.

        Args:
            host (str): The IP address of the host to connect to.
            port (int): The port to attempt to connect on.

        Note:
            This method is used internally by the `discover_hosts` method and may not be useful to call directly.
        """
        
        print(f"Trying to connect to {host} on port {port}...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect((str(host), port))  # Try to connect to the host on the specified port
            self.discovered_hosts.append(str(host))
            print(f"Host {host} is up on port {port}")
        except socket.error as e:
            self.failed_hosts.append(str(host))
            print(f"Failed to connect to {host} on port {port}")
        finally:
            s.close()

    def discover_hosts(self, subnet, port):
        """
        Discover hosts in a subnet that are listening on a specific port.

        This method uses multithreading to attempt to connect to each host in the specified subnet on the specified port. 
        If the connection is successful, the host is considered "up" and is added to the list of discovered hosts. 
        If the connection fails (for example, because the host is down or because it's not listening on the specified port), 
        the host is added to the list of failed hosts.

        The method prints a message for each host it tries to connect to, indicating whether the connection was successful or not. 
        At the end, it prints the list of all discovered hosts and the list of all failed hosts.

        Args:
            subnet (str): The subnet to scan, in CIDR notation (for example, '192.168.1.0/24').
            port (int): The port to check on each host.

        Returns:
            tuple: A tuple containing two lists: the IP addresses of the hosts that were discovered and the IP addresses of the hosts that failed to connect.

        Usage:
            monitor = NetworkMonitor()
            discovered_hosts, failed_hosts = monitor.discover_hosts("10.112.23.90/24", 80)
            print("Discovered hosts:", discovered_hosts)
            print("Failed hosts:", failed_hosts)
            Or use discovered/failed hosts your own way
        """
        network = ipaddress.ip_network(subnet)
        threads = []
        for host in network.hosts():
            thread = threading.Thread(target=self.try_connect, args=(host, port))
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        print("Discovered hosts:", self.discovered_hosts)
        print("Failed hosts:", self.failed_hosts)
        return self.discovered_hosts, self.failed_hosts

    def scan_ports(self, host, start_port=1, end_port=1024): # Idea: use nmap lib in the future instead of this?
        """
        Scan open ports on a host.
        
        
         
        This method attempts to establish a TCP connection to each port on the specified host in the range from start_port to end_port. 
        If the connection is successful, the port is considered "open" and is added to the list of open ports. 
        If the connection fails, the port is considered "closed".

        Args:
            host (str): The IP address of the host to scan.
            start_port (int): The first port in the range to scan.
            end_port (int): The last port in the range to scan.

        Returns:
            list: A list of open ports on the host.

        Usage:
            monitor = NetworkMonitor()
            open_ports = monitor.scan_ports("10.112.23.90")
            print("Open ports:", open_ports)
        """
        open_ports = []
        closed_ports = []
        threads = []

        def try_connect_port(port):
            """
            Attempt to connect to a host on a specific port.

            This function is a helper function used within the `scan_ports` method. It tries to establish a TCP connection to the specified host on the specified port. 
            If the connection is successful, the port is considered "open" and is added to the list of open ports. 
            If the connection fails, the port is considered "closed" and is added to the list of closed ports.

            Args:
                port (int): The port to attempt to connect on.

            Note:
                This function is used internally by the `scan_ports` method and may not be useful to call directly.
            """
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            try:
                s.connect((host, port))
                open_ports.append(port)
                print(f"Port {port} is open")
            except socket.error as e:
                closed_ports.append(port)
                print(f"Port {port} is closed")
            finally:
                s.close()

        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=try_connect_port, args=(port,))
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        return open_ports, closed_ports

    def monitor_http(self, host):
        """Monitor HTTP traffic of a host."""
        # Use http module to monitor HTTP traffic
        pass

    def monitor_tcp(self, host):
        """Monitor TCP traffic of a host."""
        # Use tcp module to monitor TCP traffic
        pass

    def monitor_udp(self, host):
        """Monitor UDP traffic of a host."""
        # Use udp module to monitor UDP traffic
        pass

"""monitor = NetworkMonitor()
#monitor.discover_hosts("10.112.23.0/24", 80)
open_ports, closed_ports = monitor.scan_ports("10.116.74.101")
print("Open ports:", open_ports)
print("Closed ports:", closed_ports)
"""
