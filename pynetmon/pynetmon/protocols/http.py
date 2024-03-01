# http.py

import http.client

class HTTPMonitor:
    def __init__(self, host):
        self.host = host

    def monitor_http(self):
        """
        Monitor HTTP traffic of a host.

        This method sends a GET request to the specified host and prints the response headers and body.
        """
        # Create an HTTP connection to the host
        conn = http.client.HTTPConnection(self.host)

        # Send a GET request
        conn.request("GET", "/")

        # Get the response
        response = conn.getresponse()

        # Print the status and reason
        print("Status:", response.status)
        print("Reason:", response.reason)

        # Print the headers
        print("Headers:")
        headers = response.getheaders()
        for header in headers:
            print(header)

        # Print the body
        print("Body:")
        body = response.read().decode()
        print(body)

        # Close the connection
        conn.close()