# virginia/https_checker.py

import httpx

def check_http2_status(url):
    """
    Check if the given URL supports HTTP/2.

    :param url: URL to check
    :return: True if the URL supports HTTP/2, False otherwise
    """
    try:
        with httpx.Client(http2=True) as client:
            response = client.get(url)
            return response.http_version == "HTTP/2"
    except httpx.ConnectTimeout:
        return "Error: Connection to the URL timed out."
    except httpx.HTTPStatusError as exc:
        return f"Error: HTTP error occurred: {exc.response.status_code} - {exc.response.text}"
    except httpx.RequestError as exc:
        return f"Error: An error occurred while requesting {exc.request.url!r}."

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
    else:
        url = sys.argv[1]
        is_http2 = check_http2_status(url)
        if isinstance(is_http2, str):
            print(is_http2)
        else:
            print(f"HTTP/2 support for {url}: {is_http2}")
