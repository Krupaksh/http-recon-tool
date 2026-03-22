import requests
import sys


class HTTPReconTool:
    def __init__(self, url):
        self.url = url
        self.response = None

    
    #checks URL for protocol
    def validate_url(self):
        if not(self.url.startswith(("http://","https://"))):
            sys.exit("invalid URL, should have schema(protocol)")


    #gets response from url given and handles errors which can happen
    def send_request(self):

        try: 
            # verify=False used for local dev - SSL cert issues on Windows Python
            self.response = requests.get(self.url, timeout=5 ,verify=False)
    
        except requests.exceptions.ConnectionError:
            sys.exit("Connection failed")
        except requests.exceptions.Timeout:
            sys.exit("Request time out")
        except requests.exceptions.SSLError:
            sys.exit("unable to verify the certificate")
        
    
    #gets all necessary headers from the response recieved and sets default value to not existing header
    def extract_headers(self):
            header_list={
                "Server": None ,
                "X-Powered-By": None ,
                "Content-Type": None,
                "X-Frame-Options": None,
                "Set-Cookie": None,
            }

            for header in header_list:
                header_list[header]=self.response.headers.get(header,"Not found")
            
            return header_list
                

    #detects the technology clues and what they unlock
    def detect_technology(self):
         keywords={
             "wp-content":"WordPress",
            ".php":"PHP",
            "django":"Django",
            "laravel":"Laravel",
            "csrf":"Framework Protection",
                }
  
         detected = []
         content = self.response.text.lower() #converts to lowercase incase of text case issues

         for key in keywords:
            if key in content:
                detected.append(keywords[key])
    
         return list(set(detected)) #removes duplicate values
    

    #displays the output
    def print_result(self):
           header_dict=self.extract_headers()
           
           print("========== RECON RESULT ==========")
           print(f"{'Target':<15} : {self.url}")
           print(f"{'Status Code':<15} : {self.response.status_code}")
           print(f"{'Response Time':<15} : {self.response.elapsed.total_seconds():.3f}s")
           print(f"{'Final URL':<15} : {self.response.url}")
           print(f"{'Content Length':<15} : {len(self.response.content)} bytes")

           print(f"\n[Technology Clues]")
           technologies=self.detect_technology()
           if technologies:
                for value in technologies:
                    print(f"- {value}")
           else :
                 print("No obvious technologies detected")

           print(f"\n[Headers]")
           for header in header_dict:
               print(f"{header:<15} : {header_dict[header]}")

           print("===================================")
    

    #to execute all methods in class
    def run(self):
        self.validate_url()
        self.send_request()

        if self.response:
            self.print_result()


if __name__=="__main__":
    if len(sys.argv) <2 :
        print("Usage: python recontool.py <URL>")

    else:
        recon=HTTPReconTool(sys.argv[1])
        recon.run()
