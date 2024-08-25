import requests

# Class to manage API calls
class API_manager():
    # Constructor to initialize the API manager with base URL, resource, and headers.
    def __init__(self, base_url, resource, headers={"Content-Type": "application/json"}):
        # Combine the base URL with the resource endpoint to form the complete URL.
        self.base_url = base_url + "/" + resource
        # Set default headers, which can be overridden by passing custom headers.
        self.headers = headers

    # Method to make API calls of various types (GET, POST, PUT, DELETE).
    def call(self, type, request_name, timeout, body={}, params = []):
        try:
            # Construct the full URL by appending the request name and parameters.
            url = self.base_url + "/" + request_name + "?" if request_name != "" else self.base_url + "?"
            
            # Append each parameter to the URL in the format: param_name=param_value&.
            for param in params:
                url += param[0] + "=" + param[1] + "&"
            # Remove the trailing "&" or "?" at the end of the URL.
            url = url[:-1]
            
            # Uncomment the following lines for debugging purposes to print the constructed URL.
            # print(url)
            # print("Request url: " + url)
            
            # Depending on the request type, make the appropriate HTTP call using the requests library.
            if type.upper() == "GET":
                response = requests.get(url, headers=self.headers, json=body, timeout=timeout)
            if type.upper() == "PUT":
                response = requests.put(url, headers=self.headers, json=body, timeout=timeout)
            if type.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=body,  timeout=timeout)
            if type.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers, json=body, timeout=timeout)
            
            # Initialize the default response as "Success".
            json_response = "Success"
            
            # Check if the response status code is 200 (OK).
            if response.status_code == 200:
                if response is not None:
                    # Try to parse the response as JSON, if possible.
                    try:
                        json_response = response.json()
                    except:
                        # If JSON parsing fails, return the default success message.
                        return json_response
                # If successful, return the JSON response.
                return json_response
            
            # If the status code is not 200, return "Fail".
            return "Fail"
        except Exception as e:
            print(e)
            return "Fail"