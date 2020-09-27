## Working with Network Security

#### Port Testing
- A simple python script to take in an IP Address and test port connectivity. 
- Ports are stored in the `PortTesting/ports.txt` file. 
- You can simply add ports to the list and test the application
- 

#### TLS/SSL Scanner API
- Uses the `pysslscan` package to run the sslScan
- Runs on a flask server
- Checks for SSLv2, SSLv3, TLSv1.0, TLSv1.1, TLSv1.2 & TLSv1.3 and return a dictionary with the final result

