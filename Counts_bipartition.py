import re
import sys 

'''
python version 3.9.1 
This is the function to count the existence of a particular bipartition; only for project Ceri right now
Last modified at 2022.1.5.
write by zhoubiaofeng.
'''



class CountsBipartition:
    def __init__(self,  clade_info):  #file which have infomation of each nodes contains
        self.clade_info = clade_info

    def Counts(self):
        clade_info = self.clade_info 
        f_clade_info = open(clade_info, 'r').readlines()
        clade_d = {}
        clade_cal = {}
        #clade_d = {"node1":set(["1", "2"]), "node2":set(["3","4"])}
        #clade_cal = {"node1":0 , "node2":0}
        for clade in f_clade_info:
            clade_l = clade.strip().split("\t")
            clade_d[clade_l[0]] = set(clade_l[1].split(" "))

        clade_d["C.carl_C.farg"] = set(
            list(clade_d["C.carl"]) + list(clade_d["C.farg"]))
        clade_d["C.eyre_C.lamo"] = set(
            list(clade_d["C.eyre"]) + list(clade_d["C.lamo"]))
        clade_d["Top_four"] = set(list(clade_d["C.carl_C.farg"]) +
            list(clade_d["C.eyre_C.lamo"]))
        clade_d["Top_five"] = set(
            list(clade_d["C.carl_C.farg"]) + list(clade_d["C.eyre_C.lamo"]) +
            list(clade_d["C.fabr"]))
        clade_d["C.hyst_C_ford"] = set(
            list(clade_d["C.hyst"]) + list(clade_d["C_ford"]))
        clade_d["mid_three"] = set(
            list(clade_d["C.hyst_C_ford"]) + list(clade_d["C.tibe"]))
        clade_d["Top_eight"] = set(
            list(clade_d["Top_five"]) + list(clade_d["mid_three"]))
        clade_d["C.chin_C.scle"] = set(
            list(clade_d["C.chin"]) + list(clade_d["C.scle"]))
        clade_d["bottom_three"] = set(
            list(clade_d["C.chin_C.scle"]) + list(clade_d["C.jucu"]))
        clade_d["eleven"] = set(
            list(clade_d["Top_eight"]) + list(clade_d["bottom_three"]))
        clade_d["tweleve"] = set(
            list(clade_d["eleven"]) + list(clade_d["C.fiss"]))

        for key in clade_d.keys():
            clade_cal[key] = 0
        return clade_d, clade_cal


    


