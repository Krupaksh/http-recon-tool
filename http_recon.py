import requests
import sys

def _validate_url(URL):
    if not(URL.startswith(("http://","https://"))):
        sys.exit("invalid URL, should have schema(protocol)")

def _send_request(URL):

    try:
         # verify=False used for local dev - SSL cert issues on Windows Python
         r = requests.get(URL, timeout=5 ,verify=False)
         return r
    
    except requests.exceptions.ConnectionError:
        sys.exit("Connection failed")
    except requests.exceptions.Timeout:
        sys.exit("Request time out")
    except requests.exceptions.SSLError:
         sys.exit("unable to verify the certificate")
         
def _extract_header(response):
    header_list={
        "Server": None ,
        "X-Powered-By": None ,
        "Content-Type": None,
        "X-Frame-Options": None,
        "Set-Cookie": None,

    }
    for header in header_list:
            header_list[header]=response.headers.get(header,"Not found")

    return header_list



def _print_result(response):
    header_dict=_extract_header(response)

    print("========== RECON RESULT ==========")
    print(f"{'Status Code':<15} : {response.status_code}")
    print(f"{'Response Time':<15} : {response.elapsed.total_seconds():.3f}s")
    print(f"{'Final URL':<15} : {response.url}")
    print(f"{'Content Length':<15} : {len(response.content)} bytes")
    print(f"\n[Headers]")
    for header in header_dict:
        print(f"{header :<15}: {header_dict[header]}")

    print("===================================")
    

if __name__=="__main__":
    if len(sys.argv) <2 :
        print("Usage: python recontool.py <URL>")

    else:
        _validate_url(sys.argv[1])
        response = _send_request(sys.argv[1])

        if response:
            _print_result(response)
        


