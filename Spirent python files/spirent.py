import json
import requests
import time

class Spirent:
    __frameRate = 30
    __minutes = 0
    __seconds = 0
    __destinationPath = ""
    __capture_video_path = ""

    def __init__(self,frameRate,minutes,seconds,destinationPath,capture_video_path):
        self.__frameRate = frameRate
        self.__minutes = minutes
        self.__seconds = seconds
        self.__destinationPath = destinationPath
        self.__capture_video_path = capture_video_path

    # set system non_reference
    def system_choose_non_reference(self):
        system_url = "http://localhost:5000/System/CurrentMethodology"
        system_headers = {'accept': 'application/json', 'Content-Type': 'application/json-patch+json'}
        system_body = json.dumps({ "name": "NON_REFERENCE"})
        system_response = requests.put(url=system_url,headers=system_headers,data=system_body)
        print(system_response)
        print(system_response.text)
        print("system choose non reference")
        return ;

    # set non_reference parameter
    def settings_set_non_reference_parameter(self):
        settings_url = "http://localhost:5000/Settings/ConfigureNonReferenceSettings"
        settings_headers = {'accept': 'application/json', 'Content-Type': 'application/json-patch+json'}
        settings_body = json.dumps({ "nrBuffering": "true",
                                     "nrLive": "false",
                                     "capturePath": "",
                                     "scoringModel": "HD Large Screen",
                                     "captureRate": self.__frameRate,
                                     "bufferingThreshold": 200,
                                     "freezingThreshold": 0,
                                     "enableConcurrentProcessing": "true",
                                     "notifyWhenProcessingIsCompleted": "true"})
        settings_response = requests.put(url=settings_url,headers=settings_headers,data=settings_body)
        print(settings_response)
        print(settings_response.text)
        print("setting set non reference parameter")
        return ;

    # return non_reference mothodology
    def get_methodologies_id(self):
        return "ddbb13a9-6ca1-4c69-8bc0-4ea75f006f8f";


    # set channel parameter,channelA is 1,channelB is 2.frameRate useless,what software does the description represent.
    def configure_channel_parameter(self,channel):
        # methodology_id = get_methodologies_id()
        url = "http://localhost:5000/Methodologies/ddbb13a9-6ca1-4c69-8bc0-4ea75f006f8f/Channels/configure"
        headers = {"accept": "application/json", "Content-Type": "application/json-patch+json"}
        if channel == 1:
            description = "zoom"
        else:
            description = "teams"
        body = json.dumps({"channelIndex": channel,
                           "make": description,
                          "model": "surface",
                          "role": "highmotion",
                          "hwIdentifier": "",
                          "description": description,
                          "frameRate": self.__frameRate })
        configure_channel_response = requests.put(url=url,headers=headers,data=body)
        print(configure_channel_response)
        print(configure_channel_response.text)
        print("configure channel parameter")
        return ;

    # enable channel,channelA is 1,channelB is 2.
    def enable_channel(self,channel):
        # methodology_id = get_methodologies_id()
        url = "http://localhost:5000/Methodologies/ddbb13a9-6ca1-4c69-8bc0-4ea75f006f8f/Channels/enable"
        headers = {"accept": "application/json", "Content-Type": "application/json-patch+json"}
        if channel == 1:
            videoDeviceName = "1-Spirent HDMI"
        else:
            videoDeviceName = "2-Spirent HDMI"
        body = json.dumps({"channelIndex": channel,
                          "videoDeviceName": videoDeviceName,
                          "audioDeviceName": "Disabled" })
        enable_channel_response = requests.put(url=url,headers=headers,data=body)
        print(enable_channel_response)
        print(enable_channel_response.text)
        print("enable channel")
        return ;


    # start session test,The sessionName is labeled with the name of the export file.
    # processImmediately repersents whether or not process is completed.
    def start_session_test(self,sessionName):
        # methodology_id = get_methodologies_id()
        url = "http://localhost:5000/Methodologies/ddbb13a9-6ca1-4c69-8bc0-4ea75f006f8f/Sessions"
        headers = {"accept": "application/json", "Content-Type": "application/json-patch+json"}
        body = json.dumps({ "description": sessionName,
                          "hours": 0,
                          "minutes": self.__minutes,
                          "seconds": self.__seconds,
                          "processImmediately": False })
        session_test_response = requests.post(url=url,headers=headers,data=body)
        print(session_test_response)
        print(session_test_response.text)
        print("start session test")
        return ;

    # get session list.
    # includeProcessed is processed session,includeUnProcessed is unprocessed session
    def get_list_session(self,includeProcessed,includeUnProcessed):
        url = "http://localhost:5000/Methodologies/ddbb13a9-6ca1-4c69-8bc0-4ea75f006f8f/Sessions/list"
        headers = {"accept": "application/json", "Content-Type": "application/json-patch+json"}
        body = json.dumps({"includeProcessed": includeProcessed, "includeUnProcessed": includeUnProcessed })
        list_session_response = requests.post(url=url,headers=headers,data=body)
        # print(list_session_response)
        # print(list_session_response.text)
        dict_sessions = json.loads(list_session_response.text)
        # print(dict_sessions["sessions"])
        # print(type(dict_sessions["sessions"]))
        print("get list session")
        return dict_sessions["sessions"]; # return list of dict

    # process unprocessed sessions
    # use def of get_list_session()
    def process_unprocessed_sessions(self):
        url = "http://localhost:5000/Methodologies/ddbb13a9-6ca1-4c69-8bc0-4ea75f006f8f/Sessions/processUnprocessed"
        headers = {"accept": "application/json", "Content-Type": "application/json-patch+json"}
        list_session_dict = self.get_list_session(False,True)
        # check null
        for dict in list_session_dict:
            sessionIDs = []
            sessionIDs.append(dict["sessionId"])
            body = json.dumps({"sessionIDs": sessionIDs})
            process_session_response = requests.put(url=url, headers=headers, data=body)
            print(process_session_response)
            print(process_session_response.text)
            print("process unprocessed sessions")
            while True:
                time.sleep(5)
                list_session = self.get_list_session(False,True)
                if dict in list_session:
                    continue
                else:
                    break
        # print(sessionIDs)
        return ;

    # report seesion execl file
    def create_session_report(self):
        url = "http://localhost:5000/Methodologies/ddbb13a9-6ca1-4c69-8bc0-4ea75f006f8f/Sessions/report"
        headers = {"accept": "application/json", "Content-Type": "application/json-patch+json"}
        processed_sessions = self.get_list_session(True,False)
        for dict in processed_sessions:
            print(dict["sessionId"])
            print(dict["description"])
            body = json.dumps({"sessionID": dict["sessionId"],"destinationPath": self.__destinationPath })
            report_response = requests.post(url=url,headers=headers,data=body)
            print(report_response)
            print(report_response.text)
            self.__remove_a_list_of_session(dict["sessionId"])
        print("create session report")
        return ;

    # remove a list of session
    def __remove_a_list_of_session(self,remove_processed_session):
        url = "http://localhost:5000/Methodologies/ddbb13a9-6ca1-4c69-8bc0-4ea75f006f8f/Sessions/removeSessions"
        headers = {"accept": "application/json", "Content-Type": "application/json-patch+json" }
        body = json.dumps( [ remove_processed_session ] )
        response = requests.put(url=url,headers=headers,data=body)
        print(response)
        print(response.text)
        print("remove_a_list_of_session")
        return ;

    # full-reference
    def get_folderpath(self):
        list_session_dict = self.get_list_session(True,False)
        # check null
        folderPaths = []
        f = open(self.__capture_video_path,'w+')
        for dict in list_session_dict:
            session_path_id = dict["folderPath"]
            path = "D:/Spirent Communications/captures/" + session_path_id[35:52]
            folderPaths.append(path)
            f.writelines(path)
            f.write('\n')
        print(folderPaths)
        f.close()
        return ;
    def __get_session(self,sessionId):
        url = "http://localhost:5000/Methodologies/ddbb13a9-6ca1-4c69-8bc0-4ea75f006f8f/Sessions/" + sessionId
        headers = {"accept": "application/json"}
        response = requests.get(url=url,headers=headers)
        print(response)
        if response.status_code == 200:
            return True
        else :
            return False



# def get_session(sessionId):
#     url = "http://localhost:5000/Methodologies/ddbb13a9-6ca1-4c69-8bc0-4ea75f006f8f/Sessions/" + sessionId
#     headers = {"accept": "application/json"}
#     response = requests.get(url=url,headers=headers)
#     print(response)
#     if response.status_code == 200:
#         return True
#     else :
#         return False
#
# print(get_session("56f94373-dd97-4e47-a029-923eab1daa9b"))

# get_folderpath()

# settings_set_non_reference_parameter();
# get_methodologies_id();
# configure_channel_parameter(1,24);
# configure_channel_parameter(2,24);
# enable_channel(1);
# enable_channel(2);
# start_session_test("zy",0,10,False);
# dict_sessions = get_list_session(False,True);
# for list_session in dict_sessions:
#     print(list_session)
#     print(type(list_session))
#     print("\n")
# process_unprocessed_sessions(False,True);
# create_session_report("C:\\Users\\SPIRENT\\Desktop\\11-15");