#!/usr/bin/python3

import time
import requests
import argparse
import os
from urllib.parse import urlparse

def normalize_proxy(proxy, proxy_type):
    """Normalize proxy URL by checking the proxy type and adding protocol if necessary."""
    
    # Handle specific SOCKS proxy types first
    if proxy_type == "socks4a_proxy":
        if not proxy.startswith("socks4a://"):
            proxy = "socks4a://" + proxy
    if proxy_type == "socks5h_proxy":
        if not proxy.startswith("socks5h://"):
            proxy = "socks5h://" + proxy
    if proxy_type == "socks5a_proxy":
        if not proxy.startswith("socks5a://"):
            proxy = "socks5a://" + proxy
    if proxy_type == "socks4_proxy":
        if not proxy.startswith("socks4://"):
            proxy = "socks4://" + proxy
    if proxy_type == "socks5_proxy":
        if not proxy.startswith("socks5://"):
            proxy = "socks5://" + proxy
    
    # For generic socks_proxy (without version), assume socks5
    if proxy_type == "socks_proxy":
        if not proxy.startswith("socks5://"):
            proxy = "socks5://" + proxy
    
    if proxy_type == "http_proxy":
        if not proxy.startswith("http://"):
            proxy = "http://" + proxy
    if proxy_type == "https_proxy":
        if not proxy.startswith("https://"):
            proxy = "https://" + proxy

    return proxy


def get_proxies(args):
    """Retrieve proxy settings from environment variables or command-line arguments."""
    proxies = {}

    # If --no-proxies is set, don't use any proxies (ignore environment variables)
    if args.no_proxies:
        return None

    # First, use proxies from command-line arguments if provided
    if args.socks_proxy:
        proxies["socks"] = normalize_proxy(args.socks_proxy, "socks_proxy")
    if args.socks4_proxy:
        proxies["socks"] = normalize_proxy(args.socks4_proxy, "socks4_proxy")
    if args.socks4a_proxy:
        proxies["socks"] = normalize_proxy(args.socks4a_proxy, "socks4a_proxy")
    if args.socks5_proxy:
        proxies["socks"] = normalize_proxy(args.socks5_proxy, "socks5_proxy")
    if args.socks5h_proxy:
        proxies["socks"] = normalize_proxy(args.socks5h_proxy, "socks5h_proxy")
    
    if args.http_proxy:
        proxies["http"] = normalize_proxy(args.http_proxy, "http_proxy")
    
    if args.https_proxy:
        proxies["https"] = normalize_proxy(args.https_proxy, "https_proxy")

    # If no proxies were provided on the command line, fall back to environment variables
    if not proxies:
        if not args.no_http_proxy:
            # Fall back to environment HTTP proxy if not specified on the command line
            http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
            if http_proxy:
                proxies["http"] = normalize_proxy(http_proxy, "http_proxy")
        
        if not args.no_https_proxy:
            # Fall back to environment HTTPS proxy if not specified on the command line
            https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
            if https_proxy:
                proxies["https"] = normalize_proxy(https_proxy, "https_proxy")
        
        if not args.no_socks_proxy:
            # Fall back to environment SOCKS proxy if not specified on the command line
            socks_proxy = os.getenv("SOCKS_PROXY") or os.getenv("socks_proxy")
            if socks_proxy:
                proxies["socks"] = normalize_proxy(socks_proxy, "socks_proxy")

    # If no HTTPS proxy is configured, but there is an HTTP proxy, use the HTTP proxy for HTTPS URLs
    if "https" not in proxies and "http" in proxies:
        proxies["https"] = proxies["http"].replace("http://", "https://")

    if "http" not in proxies and "https" in proxies:
        proxies["http"] = proxies["https"].replace("https://", "http://")

    return proxies


def should_bypass_proxy(url, no_proxy_list):
    """Check if the URL should bypass the proxy based on NO_PROXY rules."""
    hostname = urlparse(url).hostname
    return any(hostname.endswith(domain) for domain in no_proxy_list)

def normalize_target_url(url):
    """Ensure the target URL has a protocol, defaulting to https:// if not specified."""
    if not url:
        return None
    if "://" not in url:
        url = "https://" + url  # Default to https:// if no protocol is specified
    return url

def http_ping(url, count=4, interval=1, proxies=None):
    # Normalize target URL (default to https:// if no protocol is specified)
    url = normalize_target_url(url)

    print(f"Pinging {url} with HTTP requests" + (f" via proxy {proxies}" if proxies else "") + ":")

    for i in range(count):
        try:
            start_time = time.time()
            response = requests.get(url, timeout=interval, proxies=proxies)
            end_time = time.time()
            
            elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
            status_code = response.status_code
            
            print(f"Reply from {url}: status={status_code} time={elapsed_time:.2f}ms")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        
        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP ping utility with full curl-style proxy support")
    parser.add_argument("url", help="URL to ping (will default to https:// if no protocol is specified)")
    parser.add_argument("-c", "--count", type=int, default=4, help="Number of requests to send")
    parser.add_argument("-i", "--interval", type=float, default=1, help="Interval between requests in seconds")
    
    # Proxy arguments
    parser.add_argument("--http-proxy", help="HTTP proxy URL (overrides HTTP_PROXY environment variable)")
    parser.add_argument("--https-proxy", help="HTTPS proxy URL (overrides HTTPS_PROXY environment variable)")
    parser.add_argument("--socks-proxy", help="SOCKS proxy URL (overrides SOCKS_PROXY environment variable)")
    parser.add_argument("--socks4-proxy", help="SOCKS4 proxy URL (overrides SOCKS4_PROXY environment variable)")
    parser.add_argument("--socks4a-proxy", help="SOCKS4a proxy URL (overrides SOCKS4A_PROXY environment variable)")
    parser.add_argument("--socks5-proxy", help="SOCKS5 proxy URL (overrides SOCKS5_PROXY environment variable)")
    parser.add_argument("--socks5h-proxy", help="SOCKS5h proxy URL (overrides SOCKS5H_PROXY environment variable)")

    # Ignore proxy arguments
    parser.add_argument("--no-http-proxy", action="store_true", help="Ignore the HTTP_PROXY environment variable")
    parser.add_argument("--no-https-proxy", action="store_true", help="Ignore the HTTPS_PROXY environment variable")
    parser.add_argument("--no-socks-proxy", action="store_true", help="Ignore the SOCKS_PROXY environment variable")
    parser.add_argument("--no-socks4-proxy", action="store_true", help="Ignore the SOCKS4_PROXY environment variable")
    parser.add_argument("--no-socks4a-proxy", action="store_true", help="Ignore the SOCKS4A_PROXY environment variable")
    parser.add_argument("--no-socks5-proxy", action="store_true", help="Ignore the SOCKS5_PROXY environment variable")
    parser.add_argument("--no-socks5h-proxy", action="store_true", help="Ignore the SOCKS5H_PROXY environment variable")

    # No proxy argument
    parser.add_argument("--no-proxies", action="store_true", help="Ignore all proxy settings (environment variables and command-line arguments)")
    
    args = parser.parse_args()

    proxies = get_proxies(args)
    http_ping(args.url, args.count, args.interval, proxies)

