import ipaddress
import socket
import threading
import concurrent.futures

from .protocols.http import HTTPMonitor

TOTAL_HOURS_WASTED_HERE = 6


class ConnectionTester:
    """
    A class used to test connections to hosts on specific ports.

    ...

    Attributes
    ----------
    discovered_hosts : list
        a list of hosts that the tester was able to connect to
    failed_hosts : list
        a list of hosts that the tester failed to connect to

    Methods
    -------
    try_connect(host, port):
        Attempts to connect to a host on a specific port.
    """
    
    def __init__(self):
        """Initializes the ConnectionTester with empty lists for discovered and failed hosts."""
        self.discovered_hosts = []
        self.failed_hosts = []

    def try_connect(self, host, port):
        """
        Attempts to connect to a host on a specific port.

        If the connection is successful, the host is added to the list of discovered hosts.
        If the connection fails, the host is added to the list of failed hosts.

        Parameters
        ----------
        host : str
            The host to connect to.
        port : int
            The port to connect on.
        """
        
        print(f"Trying to connect to {host} on port {port}...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect((str(host), port))
            self.discovered_hosts.append(str(host))
            print(f"Host {host} is up on port {port}")
        except socket.error as e:
            self.failed_hosts.append(str(host))
            print(f"Failed to connect to {host} on port {port}")
        finally:
            s.close()

class HostDiscoverer:
    """
    A class used to discover hosts in a subnet that are listening on a specific port.

    ...

    Attributes
    ----------
    connection_tester : ConnectionTester
        the ConnectionTester used to test connections to hosts

    Methods
    -------
    discover_hosts(subnet, port):
        Discovers hosts in a subnet that are listening on a specific port.
    """
    
    def __init__(self):
        """Initializes the HostDiscoverer with a new ConnectionTester."""
        self.connection_tester = ConnectionTester()

    def discover_hosts(self, subnet, port):
        """
        Discovers hosts in a subnet that are listening on a specific port.
        
        Parameters
        ----------
        subnet : str
            The subnet to scan for hosts.
        port : int
            The port to test connections on.
        """
        
        network = ipaddress.ip_network(subnet)
        threads = []
        for host in network.hosts():
            thread = threading.Thread(target=self.connection_tester.try_connect, args=(host, port))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        print("Discovered hosts:", self.connection_tester.discovered_hosts)
        print("Failed hosts:", self.connection_tester.failed_hosts)
        return self.connection_tester.discovered_hosts, self.connection_tester.failed_hosts

class PortScanner:
    """
    A class used to scan for open ports on a host.

    ...

    Attributes
    ----------
    open_ports : list
        a list of open ports on the host
    closed_ports : list
        a list of closed ports on the host

    Methods
    -------
    try_connect_port(host, port):
        Attempts to connect to a host on a specific port.
    scan_ports(host, start_port=1, end_port=1024):
        Scans for open ports on a host.
    """
    
    def __init__(self, start_port=1, end_port=1024):
        """Initializes the PortScanner with empty lists for open and closed ports."""
        self.open_ports = []
        self.closed_ports = []

    def try_connect_port(self, params):
        """
        Attempts to connect to a host on a specific port.

        If the connection is successful, the port is added to the list of open ports.
        If the connection fails, the port is added to the list of closed ports.

        Parameters
        ----------
        host : str
            The host to connect to.
        port : int
            The port to connect on.
        """
        host, port = params
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        
        #print(f"Connectint to {host} on port {port}...")
        
        
        try:
            s.connect((str(host), port))
            self.open_ports.append(port)
        except:
            self.closed_ports.append(port)
        finally:
            s.close()

    def scan_ports(self, host, start_port=1, end_port=1024):
        """
        Scans for open ports on a host.

        Parameters
        ----------
        host : str
            The host to scan ports on.
        start_port : int, optional
            The port to start scanning from (default is 1).
        end_port : int, optional
            The port to stop scanning at (default is 1024).
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            executor.map(self.try_connect_port, [(host, port) for port in range(start_port, end_port + 1)])
        return self.open_ports, self.closed_ports

class NetworkMonitor:
    """
    A class used to monitor a network.

    ...

    Attributes
    ----------
    host_discoverer : HostDiscoverer
        the HostDiscoverer used to discover hosts
    port_scanner : PortScanner
        the PortScanner used to scan ports

    Methods
    -------
    discover_hosts(subnet, port):
        Discovers hosts in a subnet that are listening on a specific port.
    scan_ports(host, start_port=1, end_port=1024):
        Scans for open ports on a host.
    monitor_http(host):
        Monitors HTTP traffic on a host.
    monitor_tcp(host):
        Monitors TCP traffic on a host.
    monitor_udp(host):
        Monitors UDP traffic on a host.
    """
    
    def __init__(self):
        """Initializes the NetworkMonitor with a new HostDiscoverer and PortScanner."""
        self.host_discoverer = HostDiscoverer()
        self.port_scanner = PortScanner()

    def discover_hosts(self, subnet, port):
        """
        Discovers hosts in a subnet that are listening on a specific port.

        Parameters
        ----------
        subnet : str
            The subnet to discover hosts in.
        port : int
            The port to test connections on.
        """
        
        return self.host_discoverer.discover_hosts(subnet, port)

    def scan_open_ports(self, host, start_port=1, end_port=1024):
        """
        Scans for open ports on a host.

        Parameters
        ----------
        host : str
            The host to scan ports on.
        start_port : int, optional
            The port to start scanning from (default is 1).
        end_port : int, optional
            The port to stop scanning at (default is 1024).
        """
        
        return self.port_scanner.scan_ports(host, start_port, end_port)

    def monitor_http(self, host):
        """
        Monitors HTTP traffic on a host.

        Parameters
        ----------
        host : str
            The host to monitor HTTP traffic on.
        """
        
        #monitor = HTTPMonitor(host)
        pass

    def monitor_tcp(self, host):
        """
        Monitors TCP traffic on a host.

        Parameters
        ----------
        host : str
            The host to monitor TCP traffic on.
        """
        
        pass

    def monitor_udp(self, host):
        """
        Monitors UDP traffic on a host.

        Parameters
        ----------
        host : str
            The host to monitor UDP traffic on.
        """
        
        pass