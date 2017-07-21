# -*- coding: utf-8 -*-
__author__ = 'Alexander'


import os, codecs, re
import tkinter.filedialog as filedialog
import spon_lib.WaveAssistanFuncs.text_assistant_reader as text_reader

import spon_lib.TextGridReader as text_grid


import spon_lib.WaveAssistanFuncs.SegReader as SegReader
import spon_lib.WaveAssistanFuncs.SegWriter as SegWriter
import tkinter as tk

import tkinter.messagebox as tkMessageBox
def test_checker():
    ext_of_labelled_seg = "seg_B1"


    def one_file(event):
        input_dirname = read_param_file()
        seg_filename = filedialog.askopenfilename(initialdir = input_dirname)
        #seg_name_for_test = os.path.join(os.path.dirname(__file__), "0000_Путинцева", "0000.seg_{0}".format(ext_of_labelled_seg))
        if not os.path.isfile(seg_filename):
            tkMessageBox.showerror("Ошибка", "Вы не выбрали файл")
            return

        input_dirname = os.path.dirname(seg_filename)
        save_param_file(input_dirname)

        interval_checker(seg_filename)
        tkMessageBox.showinfo("Результат", "Файл обработан")
    def one_directory(event):
        input_dirname = read_param_file()
        input_directory = filedialog.askdirectory(initialdir = input_dirname)#r"0000_Путинцева"
        if not os.path.isdir(input_directory):
            tkMessageBox.showerror("Ошибка", "Вы не выбрали папку")
            return
        input_dirname = input_directory
        save_param_file(input_dirname)
        ind_files = 0
        for filename in os.listdir(input_directory):
            if not filename.endswith(ext_of_labelled_seg):
                continue

            interval_checker( os.path.join(input_directory, filename) )
            ind_files += 1
        if ind_files == 0:
            tkMessageBox.showerror("Результат", "Файлы seg_B1 не найдены в папке: {0}".format(input_dirname))
        else:
            tkMessageBox.showinfo("Результат", "Обработано {0} файл(-ов)".format(ind_files))
    def one_grid(event):
        input_dirname = read_param_file()
        seg_filename = filedialog.askopenfilename(initialdir = input_dirname)
        #seg_name_for_test = os.path.join(os.path.dirname(__file__), "0000_Путинцева", "0000.seg_{0}".format(ext_of_labelled_seg))
        if not os.path.isfile(seg_filename):
            tkMessageBox.showerror("Ошибка", "Вы не выбрали файл")
            return

        input_dirname = os.path.dirname(seg_filename)
        save_param_file(input_dirname)

        interval_checker_grid(seg_filename)
        tkMessageBox.showinfo("Результат", "Файл обработан")
    root = tk.Tk()
    root.title("Проверка разметки")
    btn1 = tk.Button(root, text="Выбрать файл")
    #btn1.config( height = 20, width = 20 )
    btn2 = tk.Button(root, text="Выбрать директорию")
    btn3 = tk.Button(root, text="Выбрать TextGrid")
    btn1.bind("<Button-1>", one_file)
    btn2.bind("<Button-1>", one_directory)
    btn3.bind("<Button-1>", one_grid)
    btn1.grid(row=0, column=0, sticky=tk.E+tk.W)
    btn2.grid(row=1, column=0, sticky=tk.E)
    btn3.grid(row=2, column=0, sticky=tk.E+tk.W)
    root.minsize(200, 55)
    root.maxsize(200, 70)
    root.mainloop()
def save_param_file(input_dir):
        try:
            with codecs.open(os.path.join(os.path.dirname(__file__), "checker.ini"), "w", encoding="UTF-8") as wh:
                wh.write(input_dir)
        except Exception as err:
            print("Save param file -> {0}".format(err))
def read_param_file():
        try:
            if not os.path.exists(os.path.join(os.path.dirname(__file__), "checker.ini")):
                return "."
            with codecs.open(os.path.join(os.path.dirname(__file__), "checker.ini"), "r", encoding="UTF-8") as fh:
                dirname = fh.readline().strip()
                if os.path.isdir(dirname):
                    return dirname
                return "."
        except Exception as err:
            print("read_param_file -> {0}".format(err))
            return "."
def interval_checker_grid(input_name):
    try:
        interval_ext = "TextGrid"
        interval_name = "wbound"

        grid_name = os.path.splitext(input_name)[0] + ".TextGrid"
        txt_name =  os.path.splitext(input_name)[0] + ".txt"

        res_grid = os.path.splitext(input_name)[0] + "_res.TextGrid"
        boundaries_text = read_ede_sentences(txt_name)

        grid = text_grid.readGrid(grid_name, encoding="UTF-8")

        intervals = [elem for elem in grid["levels"]["wbound"] if elem["nm"].strip() != "g"]
        pauses =  [{"frm": elem["frm"], "to": elem["to"], "nm": ""} for elem in grid["levels"]["wbound"] if elem["nm"].strip() == "g"]
        if intervals[0]["nm"].strip() == "":
            intervals = intervals[1:]


        ede_base_error = []
        if len(intervals) != len(boundaries_text):
            ede_base_error = [{"frm": 0, "nm": "Количество ЭДЕ в расшифровке и сеге не совпадает. Проверьте количество меток \"s\"", "to": grid["to"]}]
        else:
            ede_base_error = [{"frm": 0, "nm": "Ok", "to": grid["to"]}]


        n_labels = len(intervals)
        if n_labels < len(boundaries_text):
            n_labels = len(boundaries_text)

        words = []
        edes = []
        sentences = []
        sr = []
        frs = []

        ind_ede = 1
        ind_sentence = 1
        for i in range(n_labels):
            if i == len(intervals):
                break
            if i == len(boundaries_text):
                break

            cur_word = intervals[i]
            cur_text = boundaries_text[i]


            words.append({
                "frm": cur_word["frm"],
                "to": cur_word["to"],
                "nm": cur_text[0],
            })

            if cur_text[1] == 1:
                if len(sentences):
                    sentences[-1]["to"] = cur_word["frm"]
                sentences.append({
                    "frm": cur_word["frm"],
                    "to": cur_word["to"],
                    "nm": ind_sentence,
                })
                ind_sentence += 1
            if cur_text[3] == 1:
                if len(edes):
                    edes[-1]["to"] = cur_word["frm"]
                edes.append({
                    "frm": cur_word["frm"],
                    "to": cur_word["to"],
                    "nm": ind_ede,
                })
                ind_ede += 1
            a = 1
        words.extend(pauses)
        words.sort(key = lambda x: x["frm"])
        edes[-1]["to"] = intervals[-1]["to"]
        sentences[-1]["to"] = intervals[-1]["to"]

        write_text_grid_from_hash(res_grid, {
            "wbound": grid["levels"]["wbound"],
            "PSENT": sentences,
            "EDU": edes,
            "WF": words,
            "SR": [{"frm": 0, "to": intervals[-1]["to"], "nm": ""}],
            "FRS": [{"frm": 0, "to": intervals[-1]["to"], "nm": ""}],
        }, ["wbound", "PSENT", "EDU", "WF", "SR", "FRS"])
        a = 1
    except Exception as err:
        print("interval_checker_grid -> {0}".format(err))
def write_text_grid_from_hash(grid_name, seg, levels):
    try:
        w = None
        w = open(grid_name, "w", encoding = "utf8")
        if w is None:
            return
        #chapka
        w.write("File type = \"ooTextFile\"\nObject class = \"TextGrid\"\n\nxmin = 0.0\n")


        xmax = seg["wbound"][-1]["to"]
        w.write("xmax = {0}\ntiers? <exists>\nsize = {1}\nitem []:\n".format(float(xmax), len(seg)))


        size_total = 0
        ind_level = 1
        for level_name in levels:
            try:
                cur_intervals = seg[level_name]
                w.write("\titem [{0}]\n".format(ind_level))
                w.write("\t\tclass = \"IntervalTier\"\n")
                w.write("\t\tname = \"{0}\"\n".format(level_name))
                w.write("\t\txmin = {0}\n".format(float(cur_intervals[0]["frm"])))
                w.write("\t\txmax = {0}\n".format(float(xmax)))
                if len(cur_intervals):
                    w.write("\t\tintervals: size = {0}\n".format(len(cur_intervals)))
                    j_ind = 1
                    for item in cur_intervals:
                        w.write("\t\tintervals [{0}]:\n".format(j_ind))
                        w.write("\t\t\txmin = {0}\n".format(float(item["frm"])))
                        w.write("\t\t\txmax = {0}\n".format(float(item["to"])))
                        w.write("\t\t\ttext = \"{0}\"\n".format(item["nm"]))
                        j_ind += 1
                else:
                    w.write("\t\tintervals: size = 1\n")
                    w.write("\t\tintervals [1]:\n")
                    w.write("\t\t\txmin = 0\n")
                    w.write("\t\t\txmax = {0}\n".format(float(item["to"])))
                    w.write("\t\t\ttext = \"\"\n")
                a = 1
            except Exception as err:
                print(err)

    except Exception as err:
        print(err)
    finally:
        if w is not None:
            w.close()
def read_ede_sentences(txt_file):
    try:
        outpt = []
        fh = None
        fh = codecs.open(txt_file, "rb")

        binary = fh.read( os.path.getsize(txt_file) )
        text = ""
        flag = False
        for encod in ["UTF-8", "utf-8-sig", "windows-1251", "UTF-16"]:
            try:
                text = binary.decode(encod)
                flag = True
                break
            except Exception as err:
                continue
        begin_new_sentence = True
        temp_ede = []
        for line in text.split("\n"):
            if line.startswith("#"):
                continue

            if line.strip() == "":
                outpt[-1][2] = 1
                begin_new_sentence = True
            else:
                splt = line.strip().split(" ")
                for i in range(len(splt)):
                    outpt.append([splt[i], 0, 0, 0, 0])
                    if i == 0:
                        outpt[-1][3] = 1
                    if i == len(splt)-1:
                        outpt[-1][4] = 1
                    if begin_new_sentence:
                        outpt[-1][1] = 1
                        begin_new_sentence = False
                outpt[-1][2] = 1
                outpt[-1][4] = 1
    except Exception as err:
        print("read_ede_sentences -> {0}".format(err))
    finally:
        return outpt
def interval_checker(input_name):
    try:
        interval_name = "seg_B1"
        begin_symbol = "s"
        seg_name = os.path.splitext(input_name)[0] + ".seg_B1"
        txt_name = os.path.splitext(input_name)[0] + ".txt"

        seg_ede = os.path.splitext(input_name)[0] + ".seg_R1"
        seg_words = os.path.splitext(input_name)[0] + ".seg_B2"
        seg_errors = os.path.splitext(input_name)[0] + ".seg_R2"
        seg_base_error = os.path.splitext(input_name)[0] + ".seg_R3"

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

        seg = SegReader.readSeg(seg_name)
        SegReader.SegToPer(seg)

        n_ede_txt = len(ede_array)
        ede_frm_array = [i for i in range(len( seg["periods"][interval_name]) ) if seg["periods"][interval_name][i]["nm"] == "s" ]
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

    except Exception as err:
        print("interval_checker -> {0}".format(err))
if __name__ == '__main__':
    test_checker()
