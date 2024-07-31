# status_checker/main.py

import httpx

def check_page_availability(url):
    """
    Check if the given URL is available.

    :param url: URL to check
    :return: True if the URL is available, False otherwise
    """
    try:
        response = httpx.get(url, timeout=10)
        return response.status_code == 200
    except httpx.RequestError:
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
    else:
        url = sys.argv[1]
        is_available = check_page_availability(url)
        print(is_available)
