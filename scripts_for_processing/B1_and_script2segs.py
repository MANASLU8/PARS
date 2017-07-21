# -*- coding: utf-8 -*-

__author__ = "Alexander Shipilo"
import os
import tkinter.filedialog as filedialog
import spon_lib.WaveAssistanFuncs.text_assistant_reader as text_reader
import tkinter as tk

import tkinter.messagebox as tkMessageBox

import spon_lib.WaveAssistanFuncs.SegReader as SegReader
import spon_lib.WaveAssistanFuncs.SegWriter as SegWriter

def main():
    filename = r"D:\GIT\DemoCorpus\tests\0005_129.seg_B1"

    to_all_seg_levels(filename)

def to_all_seg_levels(filename):
    try:

        interval_name = "seg_B1"
        begin_symbol = "s"
        seg_name = os.path.splitext(filename)[0] + ".seg_B1"
        txt_name = os.path.splitext(filename)[0] + ".txt"


        seg_ede = os.path.splitext(filename)[0] + ".seg_R1"
        seg_words = os.path.splitext(filename)[0] + ".seg_B2"


        seg_errors = os.path.splitext(filename)[0] + ".seg_R2"
        seg_base_error = os.path.splitext(filename)[0] + ".seg_R3"



        try:
            ede_array = [elem for elem in text_reader.read_txt(txt_name).split("\n") if elem.strip() != ""]
        except Exception as err:
            print("Вероятнее всего файл с расшифровкой \"txt\" не находится в папке с сег-файлом ")
            print("Имя требуемого файла с расшифровкой: {0}".format(txt_name))
            return
        if not os.path.isfile(seg_name):
            tkMessageBox.showerror("Результат", "Ошибка. Смотрите комментарий в консоли")
            print("Нет файла: {0}".format(seg_name))
            print("Возможно Вы либо не поставили галочку \"каждый тип меток в отдельный файл\"")
            print("Либо поставили, но не пересохранили результат!!!")
            print("Чтобы пересохранить результат")
            print("- откройте речевой сигнал, который вы размечали")
            print("- поставьте в любом месте файла метку на любом уровне")
            print("- удалите эту вновь созданную метку")
            print("- закройте WaveAssistant")
            print("- проверьте файл этой программой еще раз")
            return
    except Exception as err:
        print("to_all_seg_levels -> {0}".format(err))


        seg = SegReader.readSeg(seg_name)
        if not 'levels' in seg:
            SegReader.readSeg(seg_name, encoding = "UTF-8")

        if not len(seg.get('levels', {}).get(interval_name, {})):
            print("Не могу прочитать сег. Пробовал и UTF-8 и windows-1251. Sorry =(")
            print("Файл -> {0}".format(seg_name))

        SegReader.SegToPer(seg)

        n_ede_txt = len(ede_array)
        ede_frm_array = [i for i in range(len( seg["periods"][interval_name]) ) if seg["periods"][interval_name][i]["nm"] == begin_symbol ]
        ede_frm_array.append(len( seg["periods"][interval_name])-1)
        ind_ede = 0

        words_level = []
        edes_level = []
        error_n_intervals = []
        ede_base_error = []
        if len(ede_frm_array) != len(ede_array):
            ede_base_error = [{"frm": 0, "nm": "Количество ЭДЕ в расшифровке и сеге не совпадает. Проверьте количество меток \"s\""}]
        else:
            ede_base_error = [{"frm": 0, "nm": "Ok"}]


        for i in range(1, len(ede_frm_array)):
            if i == len(ede_frm_array)-1:
                a = 1
            frm = ede_frm_array[i - 1]
            t = ede_frm_array[i]
            if i == len(ede_frm_array)-1:
                t = len(seg["periods"][interval_name])

            cur_ede_intervals = [el for el in seg["periods"][interval_name][frm:t] if el["nm"] != "g"]

            cur_ede_frm_txt = [el for el in ede_array[ind_ede].strip().split(" ") if el.strip() != "" and not el.strip().startswith("!")]

            if len(cur_ede_frm_txt) == len(cur_ede_intervals):
                for j in range(len(cur_ede_intervals)):
                    words_level.append({
                        "frm": cur_ede_intervals[j]["frm"],
                        "to": cur_ede_intervals[j]["to"],
                        "nm": cur_ede_frm_txt[j]
                    })
                edes_level.append({
                    "frm": cur_ede_intervals[0]["frm"],
                    "to": cur_ede_intervals[-1]["to"],
                    "nm": "{0}".format(ind_ede),
                })
            else:
                error_n_intervals.append({
                    "frm": cur_ede_intervals[0]["frm"],
                    "to": cur_ede_intervals[0]["to"],
                    "nm": "{0}. Не совпадает кол-во интервалов со словами".format(ind_ede),
                })
            ind_ede += 1
            a = 1



        #Осталось записать в сеги результат
        SegWriter.write_seg(seg_words, SegWriter.SegToPer(words_level), sample_rate = seg["sample_rate"])
        SegWriter.write_seg(seg_ede, SegWriter.SegToPer(edes_level), sample_rate = seg["sample_rate"])
        SegWriter.write_seg(seg_errors, SegWriter.SegToPer(error_n_intervals), sample_rate = seg["sample_rate"])
        SegWriter.write_seg(seg_base_error, ede_base_error, sample_rate = seg["sample_rate"] )

def read_conll_for_repairs(conll_name):
    try:
        a = 1
    except Exception as err:
        print("read_conll_for_repairs -> {0}".format(err))
if __name__ == "__main__":
    main()