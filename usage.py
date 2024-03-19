from pynetmon.pynetmon.main_monitor import NetworkMonitor

monitor = NetworkMonitor()

# Discover hosts in a subnet on port {someport}
#discovered_hosts, failed_hosts = monitor.discover_hosts("192.168.1.0/24", 80)
# dont print, its a built in function

# Scan ports on a host
monitor.scan_open_ports("192.168.1.1") # or or call.scan_ports("IP"), start_port=123, end_port=126)
#print("Open ports:", open_ports)
#print("Closed ports:", closed_ports)

# Monitor HTTP traffic of a host

# Monitor TCP traffic of a host

# Monitor UDP traffic of a hostcls

