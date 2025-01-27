#!/usr/bin/env python3

import re
import requests
import sys
import zipfile
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import subprocess

def download_and_extract(url, https_proxy=None):
    # Set up retry strategy
    retry_strategy = Retry(
        total=5,  # Number of retries
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
        allowed_methods=["HEAD", "GET", "OPTIONS", "GET"],  # Retry on these methods
        backoff_factor=1  # Wait between retries
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    proxies = {
        "https": https_proxy,
    } if https_proxy else None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        # Fetch the HTML content
        response = http.get(url, proxies=proxies, headers=headers)
        response.raise_for_status()  # Raise an HTTPError on bad response
        html_content = response.text

        # Regular expression pattern to match the desired URL
        pattern = r'href="(https://www\.minecraft\.net/bedrockdedicatedserver/bin-linux/[^"]+\.zip)"'

        # Search for the pattern in the HTML content
        match = re.search(pattern, html_content)

        if match:
            download_url = match.group(1)
            print(f"Downloading from {download_url}")

            # Attempt to download the zip file using requests
            try:
                zip_response = http.get(download_url, proxies=proxies, headers=headers)
                zip_response.raise_for_status()  # Raise an HTTPError on bad response
                zip_path = "/tmp/bedrock-server.zip"

                with open(zip_path, "wb") as f:
                    f.write(zip_response.content)
            except requests.exceptions.RequestException as e:
                print(f"Error using requests: {e}")
                print("Attempting to download using curl with HTTP/1.1")

                # Fallback to using curl with HTTP/1.1
                curl_command = ['curl', '-L', '--http1.1', '-A', headers['User-Agent'], download_url, '-o', zip_path]
                if https_proxy:
                    curl_command.insert(1, f'--proxy {https_proxy}')
                subprocess.run(curl_command, check=True)

            # Unzip the file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall("./bedrock-server")

            print("Download and extraction complete.")
        else:
            print("No matching URL found.")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error using curl: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: ./download_server.py <URL> [https_proxy]")
        sys.exit(1)
    
    download_page_url = sys.argv[1]
    https_proxy = sys.argv[2] if len(sys.argv) == 3 else None
    download_and_extract(download_page_url, https_proxy)
