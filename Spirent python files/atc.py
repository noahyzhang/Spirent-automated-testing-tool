# self computer IP: 192.168.10.20
# other computer IP: 192.168.10.15

import json
import requests
class ATC:
    __atc_pc = "192.168.10.1"
    __atc_port = "8000"
    __test_pc_ip = ""
    __test_pc_port = "8888"

    def __init__(self,ip,port = "8888"):
        self.__test_pc_ip = ip
        self.__test_pc_port = port

    def __get_token(self):
        get_token_url = "http://" + self.__test_pc_ip + ":" + self.__test_pc_port
        print(get_token_url)
        response = requests.get(get_token_url)
        print(response)
        print(response.text)
        dict_response = json.loads(response.text)
        print("get_token")
        return dict_response["token"]

    # get_token("http://192.168.10.19:8888")

    def control_test_pc(self):
        url = "http://" + self.__atc_pc + ":" + self.__atc_port + "/api/v1/auth/" + self.__test_pc_ip + "/"
        headers = {"Content-Type":"application/json"}
        body = json.dumps({"token": self.__get_token()})
        response = requests.post(url=url,headers=headers,data=body)
        print(response)
        print("control test pc")
        # print(response.text)
        return

    def shutdown_test_pc_atc(self):
        url = "http://" + self.__atc_pc + ":" + self.__atc_port + "/api/v1/shape/" + self.__test_pc_ip + "/"
        print(url)
        response = requests.delete(url=url)
        print(response)
        print(response.text)
        print("shutdown test pc atc")
        return

    def set_test_pc_atc_paramter(self, atc_parameter):
        url = "http://" + self.__atc_pc + ":" + self.__atc_port + "/api/v1/shape/" + self.__test_pc_ip + "/"
        headers = {"Content-Type": "application/json"}
        body = json.dumps({
              "up": {
                "rate": atc_parameter["up_bandwidth"],
                "delay": {
                  "delay": atc_parameter["up_delay"],
                  "jitter": atc_parameter["up_jitter"],
                  "correlation": 0
                },
                "loss": {
                  "percentage": atc_parameter["up_loss"],
                  "correlation": 0
                },
                "reorder": {
                  "percentage": 0,
                  "correlation": 0,
                  "gap": 0
                },
                "corruption": {
                  "percentage": 0,
                  "correlation": 0
                },
                "iptables_options": []
              },
              "down": {
                "rate": atc_parameter["down_bandwidth"],
                "delay": {
                  "delay": atc_parameter["down_delay"],
                  "jitter": atc_parameter["down_jitter"],
                  "correlation": 0
                },
                "loss": {
                  "percentage": atc_parameter["down_loss"],
                  "correlation": 0
                },
                "reorder": {
                  "percentage": 0,
                  "correlation": 0,
                  "gap": 0
                },
                "corruption": {
                  "percentage": 0,
                  "correlation": 0
                },
                "iptables_options": []
              }
        })
        response = requests.post(url=url,headers=headers,data=body)
        print(response)
        print("set test pc atc parameter")
        # print(response.text)
        return

# atc = ATC(ip="192.168.10.15")
# atc.control_test_pc()
# set_test_pc_atc_paramter()


