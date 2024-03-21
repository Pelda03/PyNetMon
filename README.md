# PyNetMon

PyNetMon is a Python library that provides various ways to monitor your network.
<strong> WORK IN PROGRESS</strong>

## Features

### Host Discovery

The `discover_hosts` method in the `NetworkMonitor` class allows you to discover hosts in a subnet that are listening on a specific port. Returns two lists of discovered and failed hosts: 

```python
from pynetmon.pynetmon.main_monitor import NetworkMonitor

monitor = NetworkMonitor()
discovered_hosts, failed_hosts = monitor.discover_hosts("192.168.1.0/24", 80)
```

### Port Scanning

The `scan_ports` method in the `NetworkMonitor` class allows you to scan for open ports on a host.

```python
from pynetmon.pynetmon.main_monitor import NetworkMonitor

monitor = NetworkMonitor()
open_ports, closed_ports = monitor.scan_ports("192.168.1.1")
```

You can also scan for specific ports on a host like this:
```python
from pynetmon import NetworkMonitor

monitor = NetworkMonitor()
monitor.scan_open_ports("192.168.1.1", ports=[80, 443]) # Scans only for ports 80 and 443
```
<strong>NOTICE: I've hardcoded a port range 1 - 1024, you can change it like this:<strong>

```python
from pynetmon import NetworkMonitor
monitor = NetworkMonitor()
monitor.scan_open_ports = ("192.168.1.1", start_port=1, end_port=500)
```
