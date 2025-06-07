# http_ping
This is a ping utility that works over HTTP/HTTPS. I needed something for working behind SLIRP-style connections with no ICMP.

    Usage:
    
            python3 http_ping.py [-h] [-c COUNT] [-i INTERVAL] [--http-proxy HTTP_PROXY] [--https-proxy HTTPS_PROXY]
                        [--socks-proxy SOCKS_PROXY] [--socks4-proxy SOCKS4_PROXY] [--socks4a-proxy SOCKS4A_PROXY]
                        [--socks5-proxy SOCKS5_PROXY] [--socks5h-proxy SOCKS5H_PROXY] [--no-http-proxy] [--no-https-proxy]        
                        [--no-socks-proxy] [--no-socks4-proxy] [--no-socks4a-proxy] [--no-socks5-proxy] [--no-socks5h-proxy]      
                        [--no-proxies]
                        url
    
    HTTP ping utility with full curl-style proxy support
    
    positional arguments:
      url                   URL to ping (will default to https:// if no protocol is specified)
    
    options:
      -h, --help            show this help message and exit
      -c COUNT, --count COUNT
                            Number of requests to send
      -i INTERVAL, --interval INTERVAL
                            Interval between requests in seconds
      --http-proxy HTTP_PROXY
                            HTTP proxy URL (overrides HTTP_PROXY environment variable)
      --https-proxy HTTPS_PROXY
                            HTTPS proxy URL (overrides HTTPS_PROXY environment variable)
      --socks-proxy SOCKS_PROXY
                            SOCKS proxy URL (overrides SOCKS_PROXY environment variable)
      --socks4-proxy SOCKS4_PROXY
                            SOCKS4 proxy URL (overrides SOCKS4_PROXY environment variable)
      --socks4a-proxy SOCKS4A_PROXY
                            SOCKS4a proxy URL (overrides SOCKS4A_PROXY environment variable)
      --socks5-proxy SOCKS5_PROXY
                            SOCKS5 proxy URL (overrides SOCKS5_PROXY environment variable)
      --socks5h-proxy SOCKS5H_PROXY
                            SOCKS5h proxy URL (overrides SOCKS5H_PROXY environment variable)
      --no-http-proxy       Ignore the HTTP_PROXY environment variable
      --no-https-proxy      Ignore the HTTPS_PROXY environment variable
      --no-socks-proxy      Ignore the SOCKS_PROXY environment variable
      --no-socks4-proxy     Ignore the SOCKS4_PROXY environment variable
      --no-socks4a-proxy    Ignore the SOCKS4A_PROXY environment variable
      --no-socks5-proxy     Ignore the SOCKS5_PROXY environment variable
      --no-socks5h-proxy    Ignore the SOCKS5H_PROXY environment variable
      --no-proxies          Ignore all proxy settings (environment variables and command-line arguments)

Oh and this was written almost 100% with Google Gemini. Pretty nifty, right?
