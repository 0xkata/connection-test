# Testing connection to url

import argparse
import requests
from requests.adapters import HTTPAdapter, Retry
import time
import os
from halo import Halo
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

success = []
failure = []
s = requests.Session()
retries = Retry(total=0)
s.mount("http://", HTTPAdapter(max_retries=retries))
s.mount("https://", HTTPAdapter(max_retries=retries))


def connection(url):
    try:
        response = s.head(url)
        status_code = response.status_code
        allowed_methods = response.headers.get("Allow", "")
        if status_code == 200 and "GET" in allowed_methods.split(","):
            success.append(url)
        else: 
            failure.append(url)
        return status_code
    except Exception as e:
        return e


def process_file(filename, output_file):
    try:
        with open(filename, "r") as urls, open(output_file, "a") as output, Halo(text="Loading...", spinner="dots") as loading:
            for url in urls:
                url = url.strip()
                if url:
                    loading.start(f'Testing "{url}"')
                    result = connection(url)
                    time.sleep(1)
                    loading.stop()
                    print(f"{url:<90} ----- {result}") 
                    output.write(f"{url:<90} ----- {result}\n")
    except FileNotFoundError:
        print("File not found!")
        exit()

def main():
    parser = argparse.ArgumentParser(description="Test connection to url")
    parser.add_argument("-u", "--url", type=str, help="url to test connection")
    parser.add_argument("-f", "--file", type=str, help="file path of urls")
    parser.add_argument("-o", "--output", type=str, help="output file path (will not save if single url)", default="output.txt")
    args = parser.parse_args()

    url = args.url
    file = args.file
    output = args.output

    if url:
        connection(url)
    elif file:
        process_file(file, output)

if __name__ == "__main__":
    main()
