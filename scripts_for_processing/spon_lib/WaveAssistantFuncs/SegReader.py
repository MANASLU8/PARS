# -*- coding: utf-8 -*-
__author__ = "Alexander Shipilo"
#Seg Reader function to read and to convert labels to per +
#readSeg - reading seg
#SegToPraatFormat - convert labels to periods in praat format
#SegToPer -
import spon_lib.WaveAssistantFuncs.SegDict as SegDict
import os, re
def __read_seg(f_name, seg = None, encoding="windows-1251"):
    if seg is None:
        seg = {}
    try:
        f = None
        f = open(f_name, "r", encoding = encoding)

        #reading header
        line = f.readline().rstrip()
        if line.find("[PARAMETERS]") == -1:
            raise Exception
        #samp_rate
        line = f.readline().rstrip()
        splt = line.split("=")
        if splt[0] != "SAMPLING_FREQ":
            raise Exception
        seg["sample_rate"] = int(splt[1])
        #byte_per_sample
        line = f.readline().rstrip()
        splt = line.split("=")
        if splt[0] != "BYTE_PER_SAMPLE":
            raise Exception
        seg["byte_per_sample"] = int(splt[1])
        #code
        line = f.readline().rstrip()
        splt = line.split("=")
        if splt[0] != "CODE":
            raise Exception
        seg["code"] = int(splt[1])
        #n_channel
        line = f.readline().rstrip()
        splt = line.split("=")
        if splt[0] != "N_CHANNEL":
            raise Exception
        seg["n_channel"] = int(splt[1])
        #n_labels
        line = f.readline().rstrip()
        splt = line.split("=")
        if splt[0] != "N_LABEL":
            raise Exception
        seg["n_lab"] = seg.get("n_lab", 0) + int(splt[1])
        #LABELS
        line = f.readline().rstrip()
        if line != "[LABELS]":
            raise Exception
        #labels themselves
        if not seg.get("levels"):
            seg["levels"] = {}
        #getting level name
        ind_ext = f_name.rindex(".")
        extention = f_name[ind_ext+1:]

        #adding lev_name it is exrention of the file
        seg["levels"][extention] = []
        prev = -1
        for line in f:
            temp_lab = line.rstrip().split(",", 2)
            if int(temp_lab[0]) > prev:
                seg["levels"][extention].append({"frm": int(int(temp_lab[0])/seg["byte_per_sample"]), "nm": temp_lab[2]})
                prev = int(temp_lab[0])
    except Exception as err:
        print(err)
        return None
    finally:
        if f is not None:
            f.close()
def readSeg(f_name, rAllLevels = None, levels2read = None, encoding = "Windows-1251"):
    seg = {}
    ind_ext = f_name.rindex(".")
    extention = f_name[ind_ext+1:]
    seg["file"] = f_name
    if rAllLevels is not None:
        for key in SegDict.segColours.keys():
            temp_name = f_name[:ind_ext]+"."+key
            if os.path.isfile(temp_name):
                __read_seg(temp_name, seg = seg, encoding = encoding)
                t =1
        return seg
    elif levels2read is not None:
        for lev in levels2read:
            temp_name = f_name[:ind_ext]+"."+lev
            if os.path.isfile(temp_name):
                __read_seg(temp_name, seg = seg, encoding = encoding)
    else:
        __read_seg(f_name, seg = seg, encoding = encoding)
    return seg
def SegToPraatFormat(seg, del_orig = None, log = None):
    try:
        seg["periods"] = {}
        for key in seg["levels"].keys():
            if len(seg["levels"][key]) == 1:
                print("One label at the level in", seg["file"], " Impossible to get intervals at", key)
                log.add_inf("{0}\t{1}\t{2}\{3}\n".format("One label at the level in", seg["file"], " Impossible to get intervals at", key))
                continue
            seg["periods"][key] = []
            i = 1
            while i<len(seg["levels"][key]):
                frm = float(seg["levels"][key][i-1]["frm"]/seg["sample_rate"])
                to = float(seg["levels"][key][i]["frm"]/seg["sample_rate"])
                nm = seg["levels"][key][i-1]["nm"]
                seg["periods"][key].append({"frm": frm, "to": to, "nm": nm})
                i+=1
        if del_orig is not None:
            seg.pop("levels")
    except Exception as err:
        print(err)
        return None
def SegToPer(seg, del_orig = False):
    try:
        seg["periods"] = {}
        for key in seg["levels"].keys():
            if len(seg["levels"][key]) == 1:
                print("One label at the level in", seg["file"], " Impossible to get intervals at", key)
                continue
            seg["periods"][key] = []
            i = 1
            while i<len(seg["levels"][key]):
                frm = seg["levels"][key][i-1]["frm"]
                to = seg["levels"][key][i]["frm"]
                nm = seg["levels"][key][i-1]["nm"]
                seg["periods"][key].append({"frm": frm, "to": to, "nm": nm})
                i+=1
        if del_orig == True:
            seg.pop("levels")
    except Exception as err:
        print(err)
        return None

def PerToLab(seg, level = None):
    outpt = []
    if level is not None:
        i = 1
        outpt.append({"frm": seg["periods"][level][0]["frm"], "nm": seg["periods"][level][0]["nm"]})
        if len(seg["periods"][level]) == 1:
            outpt.append({"frm": seg["periods"][level][0]["to"], "nm": ""})
            return
        while i<len(seg["periods"][level]):
            temp = seg["periods"][level][i]
            prev = seg["periods"][level][i-1]
            if prev["to"] == temp["frm"]:
                outpt.append({"frm": temp["frm"], "nm": temp["nm"]})
            else:
                outpt.append({"frm": prev["to"], "nm": ""})
                outpt.append({"frm": temp["frm"], "nm": temp["nm"]})
            i+=1
        if not seg.get("levels"): seg.setdefault("levels", {level: []})
        seg["levels"][level] = outpt
        seg["periods"].pop(level)
    else:
        try:
            for key in seg["periods"].keys():
                if len(seg["periods"][key]) == 0:
                    continue
                outpt = []
                i = 1
                outpt.append({"frm": seg["periods"][key][0]["frm"], "nm": seg["periods"][key][0]["nm"]})
                if len(seg["periods"][key]) == 1:
                    if not seg.get("levels"): seg.setdefault("levels", {key: []})
                    outpt.append({"frm": seg["periods"][key][0]["to"], "nm": ""})
                    seg["levels"][key] = outpt
                    continue
                while i<len(seg["periods"][key]):
                    temp = seg["periods"][key][i]
                    prev = seg["periods"][key][i-1]
                    if prev["to"] == temp["frm"]:
                        outpt.append({"frm": temp["frm"], "nm": temp["nm"]})
                    else:
                        outpt.append({"frm": prev["to"], "nm": ""})
                        outpt.append({"frm": temp["frm"], "nm": temp["nm"]})
                    i+=1
                if not seg.get("levels"): seg.setdefault("levels", {key: []})
                #if not seg["levels"].get(key): seg.setdefault(key, [])
                seg["levels"][key] = outpt
                #seg["periods"].pop(key)
        except Exception as err:
            print(err)
def get_labels_id(seg: dict, level: str, search: str, where:str ='periods'):
        '''
        На вход строку, которую нужно  найти
        :param search:
        :return: возвращает индексы всех аллофонов, которые подписаны именно так
        '''
        try:
            res_ids = []
            if where in seg and level in seg[where]:
                res_ids = [ind for ind in range(len(seg[where][level])) if seg[where][level][ind]["nm"] == search]
            else:
                if not where in seg:
                    print("Нет -> {0}".format(where))
                else:
                    print("Нет -> {0} в {1}".format(level, where))
        except Exception as err:
            print("SegReader get_labels_id -> {0}".format(err))
        finally:
            return res_ids
def get_labels_id_re(seg: dict, level: str, reg_expr_string: str, where:str ='periods'):
        '''
            На вход строку. где прописано регулярное выражение, которое нужно найти
            :param search:
            :return: возвращает индексы всех аллофонов, которые подписаны в соотвествии с re
        '''
        try:
            res_ids = []
            if where in seg and level in seg[where]:
                res_ids = [ind for ind in range(len(seg[where][level])) if re.search(reg_expr_string, seg[where][level][ind]["nm"])]
            else:
                if not where in seg:
                    print("Нет -> {0}".format(where))
                else:
                    print("Нет -> {0} в {1}".format(level, where))
        except Exception as err:
            print("SegReader get_labels_id_re -> {0}".format(err))
        finally:
            return res_ids