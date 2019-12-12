from spirent import Spirent
import time
from atc import ATC
import execl
from execl import deal_execl
import os

# frameRate = 24
# minutes = 0
# seconds = 30
# processImmediately = False
# destinationPath = "C:\\Users\\SPIRENT\\Desktop\\11-15"  # must double slash
# test_pc_ip1 = "192.168.10.16"
# test_pc_port1 = "8888"
# test_pc_ip2 = "192.168.10.19"
# test_pc_port2 = "8888"
# case_execl_location = "C:\\Users\\SPIRENT\\Desktop\\test.xlsx"
# capture_video_path = "C:\\Users\\SPIRENT\\Desktop\\test_video_path.txt"

# print("please input paramter")
# frameRate = input("please input video frameRate:");
# minutes = input("please input test video mintues:")
# seconds = input("please input test video seconds:")
# test_pc_ip1 = input("please input test pc1 ip:")
# test_pc_ip2 = input("please input test pc2 ip:")
# case_execl_location = input("please input all case execl location(must double slash):")
# destinationPath = input("please input the path to store the result(must double slash):")
# capture_video_path = input("please input used to make the path to video in full reference mode(must double slash):")

class Main:

    __frameRate = 24
    __minutes = 0
    __seconds = 30
    # processImmediately = False
    __test_pc_ip1 = "192.168.10.16"
    # test_pc_port1 = "8888"
    __test_pc_ip2 = "192.168.10.19"
    # test_pc_port2 = "8888"
    __case_execl_location = "C:\\Users\\SPIRENT\\Desktop\\test.xlsx"
    __destinationPath = "C:\\Users\\SPIRENT\\Desktop\\11-15"  # must double slash
    __capture_video_path = "C:\\Users\\SPIRENT\\Desktop\\test_video_path.txt"

    __spirent_object = ""
    __atc_object1 = ""
    __atc_object2 = ""

    def __init__(self):
        self.input_parmeter()
        self.__spirent_object = Spirent(self.__frameRate, self.__minutes, self.__seconds, self.__destinationPath, self.__capture_video_path)
        return

    def input_parmeter(self):
        print("please input paramter")
        print("please input video frameRate(15/24/25/30/50/60):")
        frameRate = input()
        while (int(frameRate) in [15,24,25,30,50,60]) == False:
            print("frameRate choose: 15/24/25/30/50/60")
            frameRate = input()
        self.__frameRate = frameRate

        print("please input mintues and seconds")
        minutes = input("mintues:")
        seconds = input("seconds:")
        self.__minutes = minutes
        self.__seconds = seconds

        print("please input test pc1 ip (default:192.168.10.16):")
        test_pc_ip1 = input()
        if test_pc_ip1 == "":
            test_pc_ip1 = "192.168.10.16"
        print("please input test pc2 ip (default:192.168.10.19):")
        test_pc_ip2 = input()
        if test_pc_ip2 == "":
            test_pc_ip2 = "192.168.10.19"
        self.__test_pc_ip1 = test_pc_ip1
        self.__test_pc_ip2 = test_pc_ip2

        print("please input all case execl location(must double slash):")
        print("default: C:\\Users\\SPIRENT\\Desktop\\test.xlsx")
        case_execl_location = input()
        if case_execl_location == "":
            case_execl_location = "C:\\Users\\SPIRENT\\Desktop\\test.xlsx"
        while os.path.isfile(case_execl_location) == False:
            print("location not exist,please input again:")
            case_execl_location = input()
        self.__capture_video_path = case_execl_location

        print("please input the path to store the result(must double slash):")
        print("default: C:\\Users\\SPIRENT\\Desktop\\11-15")
        destinationPath = input()
        if destinationPath == "":
            destinationPath = "C:\\Users\\SPIRENT\\Desktop\\11-15"
        while os.path.exists(destinationPath) == False:
            print("location not exist,please input again:")
            destinationPath = input()
        self.__destinationPath = destinationPath

        print("please input used to make the path to video in full reference mode(must double slash):")
        print("default: C:\\Users\\SPIRENT\\Desktop\\test_video_path.txt")
        capture_video_path = input()
        if capture_video_path == "":
            capture_video_path = "C:\\Users\\SPIRENT\\Desktop\\test_video_path.txt"
        while os.path.isfile(capture_video_path) == False:
            print("location not exist,please input again:")
            capture_video_path = input()
        self.__capture_video_path = capture_video_path
        return


    def set_environment(self):
        # set non reference environment: settings
        self.__spirent_object.system_choose_non_reference()
        self.__spirent_object.settings_set_non_reference_parameter()

        #set non reference environment: capture
        self.__spirent_object.configure_channel_parameter(1)
        self.__spirent_object.configure_channel_parameter(2)
        self.__spirent_object.enable_channel(1)
        self.__spirent_object.enable_channel(2)
        return

    def set_atc(self):
        # set atc
        self.__atc_object1 = ATC(self.__test_pc_ip1)
        self.__atc_object1.control_test_pc()
        self.__atc_object2 = ATC(self.__test_pc_ip2)
        self.__atc_object2.control_test_pc()
        return

    def Start_process(self):
        self.set_environment()
        self.set_atc()
        # get all case
        tables = execl.import_execl(self.__case_execl_location)

        # set atc, next, start test
        for table in tables:
            self.__atc_object1.set_test_pc_atc_paramter(table)
            self.__atc_object2.set_test_pc_atc_paramter(table)
            self.__spirent_object.start_session_test(table["session_name"])
            time.sleep(int(self.__minutes)*60)
            time.sleep(int(self.__seconds)+1)

            # process sessions
            self.__spirent_object.process_unprocessed_sessions()


        # report sessions execl file
        while len(self.__spirent_object.get_list_session(False,True)) != 0:
            time.sleep(10)
            print("processing....")

        # video path for acquisition in full reference mode
        self.__spirent_object.get_folderpath()

        self.__spirent_object.create_session_report()


        while len(self.__spirent_object.get_list_session(True,False)) != 0:
            time.sleep(10)
            print("generatting final erport.....")

        # generate final report
        execl_object = execl.deal_execl(self.__destinationPath)
        execl_object.generate_final_report()
        return

object = Main()
object.Start_process()