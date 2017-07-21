# -*- coding: utf-8 -*-
def __readFullGrid(f, grid):
    lev_name = None
    grid["levels"] = {}
    try:
        #xmax
        line = f.readline().rstrip()
        splt = line.split(" = ")
        grid["to"] = float(splt[1])
        #tiers
        line = f.readline()
        line = f.readline().rstrip()
        splt = line.split(" = ")
        n_lev = int(splt[1])
        line = f.readline()
        i_lev = 0
        while i_lev < n_lev:
            line = f.readline()
            line = f.readline()
            line = f.readline().strip()
            splt = line.split(" = ")
            lev_name = splt[1][1:-1]
            line = f.readline()
            line = f.readline()
            line = f.readline().strip()
            splt = line.split(" = ")
            n_items = int(splt[1])
            i_item = 0
            if not grid["levels"].get(lev_name): grid["levels"][lev_name] = []
            while i_item<n_items:
                temp = {}
                line = f.readline()
                #xmin
                line = f.readline().strip()
                splt = line.split(" = ")
                temp["frm"] = float(splt[1])
                #xmax
                line = f.readline().strip()
                splt = line.split(" = ")
                temp["to"] = float(splt[1])
                #name
                line = f.readline().strip()
                splt = line.split(" = ")
                temp["nm"] = splt[1][1:-1]
                #adding into array
                grid["levels"][lev_name].append(temp)
                i_item+=1
            i_lev+=1
        return True
    except Exception as err:
        print(err)
        return None
def __readSmallGrid(f, grid):
    try:
        lev_name = None
        grid["to"] = float(f.readline().strip())
        f.readline()
        n_lev = int(f.readline().strip())
        i_lev = 0
        grid["levels"] = {}
        while i_lev < n_lev:
            f.readline()
            lev_name = f.readline().strip()[1:-1]
            grid["levels"][lev_name] = []
            f.readline()
            f.readline()
            n_item = int(f.readline().strip())
            i_item = 0
            while i_item < n_item:
                #frm
                grid["levels"][lev_name].append({"frm": float(f.readline().strip())})
                #to
                grid["levels"][lev_name][-1]["to"] = float(f.readline().strip())
                #nm
                grid["levels"][lev_name][-1]["nm"] = f.readline().strip()[1:-1]
                i_item +=1
            i_lev+=1
        return True
    except Exception as err:
        print(err)
        return None


def readGrid(f_name, levelsToRead = None, encoding = "utf16"):
    try:
        grid = {}
        f = open(f_name, "r", encoding = encoding)
        try:
            line = f.readline().rstrip()
        except:
            if f is not None: f.close()
            f = open(f_name, "r")
            line = f.readline()
        ind = line.index('File type = "ooTextFile"')
        line = f.readline()
        ind = line.index('Object class = "TextGrid"')
        line = f.readline()
        #xmin
        #checking whther it is full or small text grid
        line = f.readline().rstrip()
        try:
            #Reading small Text grid
            grid["frm"] = float(line)
            if not __readSmallGrid(f, grid): return None
        except:
            #Reading full text grid
            #xmin
            splt = line.split(" = ")
            grid["frm"] = float(splt[1])
            if not __readFullGrid(f, grid): return None
        return grid
    except Exception as err:
        print(err)
    finally:
        if f is not None: f.close()