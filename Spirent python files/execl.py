import xlrd

def import_execl(case_execl_location):
    data = xlrd.open_workbook(case_execl_location)
    table = data.sheets()[0]
    count = 0
    tables = []
    for rown in range(table.nrows):
        array = {"session_name": "", "up_bandwidth": "", "up_delay": "", "up_jitter": "", "up_loss": "",
                 "down_bandwidth": "", "down_delay": "","down_jitter": "","down_loss": ""}
        array["session_name"] = table.cell_value(rown,0)
        array["up_bandwidth"] = table.cell_value(rown,1)
        array["up_delay"] = table.cell_value(rown, 2)
        array["up_jitter"] = table.cell_value(rown, 3)
        array["up_loss"] = table.cell_value(rown, 4)
        array["down_bandwidth"] = table.cell_value(rown,5)
        array["down_delay"] = table.cell_value(rown, 6)
        array["down_jitter"] = table.cell_value(rown, 7)
        array["down_loss"] = table.cell_value(rown, 8)
        if count != 0:
            tables.append(array)
        count = count + 1
    for i in tables:
        print(i)
    return tables

# tables = import_execl("C:\\Users\\SPIRENT\\Desktop\\test.xlsx")

import  xlrd
import xlwt
import os

class deal_execl:
    __result_directory = ""
    __names = []
    three_array = []
    def __init__(self,resule_directory):
        self.__result_directory = resule_directory
        self.__names = os.listdir(self.__result_directory)
        print(self.__names)
        self.get_data()
        return
    def get_data(self):
        nums = [6,15,19,24,27]
        for name in self.__names:
            dict = {}
            rbook = xlrd.open_workbook(self.__result_directory + "\\" + name)
            rsheet = rbook.sheet_by_name("Video Scorecard")
            for num in nums:
                list = []
                list.append(rsheet.cell(num,1).value)
                list.append(rsheet.cell(num,2).value)
                dict[rsheet.cell(num,0).value] = list
            self.three_array.append(dict)
        print(self.three_array)
        print("get data finish")
        return
    def generate_final_report(self):
        wbook = xlwt.Workbook()
        wsheet = wbook.add_sheet("sheet1")
        row = 4
        for name in self.__names:
            wsheet.write(row,1,name)
            row = row + 1
        wsheet.write(2,2,"Average MOS")
        wsheet.write(2,5,"% of Time Buffering")
        wsheet.write(2,8,"% of Time Frozen")
        wsheet.write(2,11,"Framerate")
        nums = [2, 5, 8, 11]
        for num in nums:
            wsheet.write(3,num,"zoom")
            wsheet.write(3,num+1,"teams")
        row = 4
        for dict in self.three_array:
            wsheet.write(row, 2, dict["Average MOS"][0])
            wsheet.write(row, 3, dict["Average MOS"][1])
            wsheet.write(row, 5, dict["% of Time Buffering"][0])
            wsheet.write(row, 6, dict["% of Time Buffering"][1])
            wsheet.write(row, 8, dict["% of Time Frozen"][0])
            wsheet.write(row, 9, dict["% of Time Frozen"][1])
            wsheet.write(row, 11, dict["Framerate"][0])
            wsheet.write(row, 12, dict["Framerate"][1])
            row = row + 1
        wbook.save(self.__result_directory + "\\res.xls")
        print("generate final report finish")
        return



# execl = deal_execl("C:\\Users\\user\\Desktop\\directory")
# execl.generate_final_report()