import requests

class API_manager():
    def __init__(self, base_url, resource, headers={"Content-Type": "application/json"}):
        self.base_url = base_url + "/" + resource
        self.headers = headers

    def call(self, type, request_name, timeout, body={}, params = []):
        url = self.base_url + "/" + request_name + "?" if request_name != "" else self.base_url + "?"
        for param in params:
            url += param[0] + "=" + param[1] + "&"
        url = url[:-1]
        # print(url)
        # print("Request url: " + url)
        if type.upper() == "GET":
            response = requests.get(url, headers=self.headers, timeout=timeout)
        if type.upper() == "PUT":
            response = requests.put(url, headers=self.headers, timeout=timeout)
        if type.upper() == "POST":
            response = requests.post(url, headers=self.headers, json=body,  timeout=timeout)
        if type.upper() == "DELETE":
            response = requests.delete(url, headers=self.headers, timeout=timeout)
        # print("Status code: " + str(response.status_code))
        json_response = "Success"
        if response.status_code == 200:
            if response is not None:
                try:
                    json_response = response.json()
                except:
                    return json_response
            return json_response
        return "Fail"