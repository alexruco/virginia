# checker_status/curl_emulator.py

import requests
import argparse
import sys

def check_url_status(url):
    """
    Check the status of the given URL, including handling redirects.

    :param url: URL to check
    :return: status code of the final URL response, or an error message
    """
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        if response.status_code == 200:
            if "html" in response.headers.get("Content-Type", "").lower():
                return 200
            else:
                return "Error: URL did not return an HTML page"
        return response.status_code
    except requests.RequestException as e:
        return f"Error: {e}"

def emulate_curl(url, method='GET', headers=None, data=None, files=None, verbose=False, timeout=10):
    """
    Emulate some common functionalities of curl using Python's requests library.
    
    :param url: URL to request
    :param method: HTTP method (GET, POST, etc.)
    :param headers: Dictionary of HTTP headers
    :param data: Data to send in the body of the request (for POST, PUT, etc.)
    :param files: Dictionary of files to upload
    :param verbose: Flag for verbose output
    :param timeout: Request timeout in seconds
    :return: Response object
    """
    try:
        response = requests.request(method, url, headers=headers, data=data, files=files, timeout=timeout)
        if verbose:
            print(f"Request URL: {response.url}")
            print(f"Request Method: {method}")
            print(f"Status Code: {response.status_code}")
            print("Response Headers:")
            for key, value in response.headers.items():
                print(f"  {key}: {value}")
            print("Response Body:")
            print(response.text[:2000])  # Print only first 2000 chars for brevity
        return response
    except requests.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Emulate curl using Python.")
    parser.add_argument('url', help="URL to request")
    parser.add_argument('-X', '--request', default='GET', help="HTTP method to use (default: GET)")
    parser.add_argument('-H', '--header', action='append', help="HTTP headers to include in the request")
    parser.add_argument('-d', '--data', help="Data to send in the body of the request")
    parser.add_argument('-F', '--form', action='append', help="Files to upload (format: key=@filename)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output")
    parser.add_argument('--timeout', type=int, default=10, help="Timeout for the request in seconds (default: 10)")
    
    args = parser.parse_args()
    
    headers = {}
    if args.header:
        for header in args.header:
            key, value = header.split(':', 1)
            headers[key.strip()] = value.strip()
    
    files = {}
    if args.form:
        for form in args.form:
            key, value = form.split('=', 1)
            if value.startswith('@'):
                file_path = value[1:]
                files[key] = open(file_path, 'rb')
    
    response = emulate_curl(args.url, method=args.request, headers=headers, data=args.data, files=files, verbose=args.verbose, timeout=args.timeout)
    
    if not args.verbose:
        print(f"Status of {args.url}: {response.status_code if isinstance(response, requests.Response) else response}")

    # Close any open files
    for file in files.values():
        file.close()
