from pynetmon.pynetmon.main_monitor import NetworkMonitor

monitor = NetworkMonitor()

# Discover hosts in a subnet on port {someport}
#discovered_hosts, failed_hosts = monitor.discover_hosts("192.168.1.0/24", 80)
# dont print, its a built in function

# Scan ports on a host
open_ports, closed_ports = monitor.scan_open_ports("192.168.1.50")
#print("Open ports:", open_ports)
#print("Closed ports:", closed_ports)

# Monitor HTTP traffic of a host

# Monitor TCP traffic of a host

# Monitor UDP traffic of a hostcls


