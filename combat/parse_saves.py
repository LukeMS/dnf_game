import re
from collections import OrderedDict


def parse_composite(line, save):
    adjustments = OrderedDict()
    [adjustments.update(x) for x in [
        {"(": ","},
        {")": ""},
        {"vs.": ";"}
    ]]
    def_mod = 0
    temp = {}
    # print("Line:", line)
    for replace_from, replace_to in adjustments.items():
        line = line.replace(replace_from, replace_to)

    # print("Line:", line)
    splitted = line.split(",")
    for split in splitted:

        searchobj = re.search('^( |)(\+|)(-\d*|\d*)( |)$', split, re.I)
        if searchobj:
            def_mod = int(searchobj.group(3))
            continue

        searchobj = re.search(
            '^( |)(\+|)(-\d*|\d*)( |);( |)(\w*|\w*-\w*|nonmagical disease)( effects|)( |)$',
            split, re.I)
        if searchobj:
            new = {save: {
                searchobj.group(6): searchobj.group(3)}}
            temp.update(dict(new))
            # print(split)
            # print(new)
            continue

        searchobj = re.search(
            '^( |)(\+|)(-\d*|\d*)( |);( |)(\w*) and (\w*|\w*-\w*) effects( |)$', split, re.I)
        if searchobj:
            new = {save: {
                searchobj.group(6): searchobj.group(3),
                searchobj.group(7): searchobj.group(3),}}
            temp.update(dict(new))
            # print(split)
            # print(new)
            continue

        print("***{}***".format(line))
        print('error: "{}" remains'.format(split))
        print('currently parsed:', def_mod, temp)
        exit()
    return def_mod, temp



def parse(table):

    save_mod = []
    special_saves = {}
    for save, i in zip(["fort", "ref", "will"], range(3)):
        try:
            save_mod.append(int(table[save]))
        except:
            comp_list, comp_dict = parse_composite(table[save], save)
            # print(comp_list)
            # print(comp_dict)
            save_mod.append(comp_list)
            special_saves.update(comp_dict)
    # print(save_mod)
    # print(special_saves)
    return save_mod, special_saves


        # raise ValueError("Error on {}: {}".format(save, table[save]))


if __name__ == '__main__':
    import bestiary
    bestiary = bestiary.Bestiary()
    while True:
        table = bestiary.get()
        parse_saves(table)


"""
        self.save_mod = [
            int(table["Fort"]),
            int(table["Ref"]),
            int(table["Will"])]
"""

#return list of int, dict
