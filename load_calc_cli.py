import re
from collections import defaultdict


def compressor(load_dict: dict) -> dict:
    compressed_load_dict = defaultdict(float)
    LC_type = {"+": [], "-": [], "": []}
    for LC, val in load_dict.items():
        if "+" in LC:
            LC_type["+"].append(LC)
        elif "-" in LC:
            LC_type["-"].append(LC)
        else:
            LC_type[""].append(LC)
    for LC, vals in load_dict.items():
        mult = False
        for val in vals:
            if val == "->":
                mult = True
            if val != "->":
                if mult == True:
                    res = re.findall(r"[-+]?(?:\d*\.*\d+)", val)
                    if len(res) >= 2:
                        flt /= float(res[0])
                    else:
                        flt *= float(res[0])
                else:
                    flt = float(re.findall(r"[-+]?(?:\d*\.*\d+)", val)[0])
        if LC in LC_type["+"] or LC in LC_type[""]:
            compressed_load_dict[LC.replace("+", "")] += flt
        else:
            compressed_load_dict[LC.replace("-", "")] -= flt
    return compressed_load_dict


load_dict = {}
print("MyLC Version 1.0.0 Command line tool for rapid load combination maniputations")
storage = {}
while True:
    cmd = input(">>")
    if cmd == "exit":
        quit()
    if cmd == "v" or cmd == "":
        print("")
        for k, v in load_dict.items():
            print(k, *v)
        print("")
        continue
    elif cmd == "d":
        load_dict = {}
        continue
    elif cmd == "s":
        compressed_load_dict = compressor(load_dict)
        print("")
        for k, v in compressed_load_dict.items():
            print(k, v)
        print("")
    elif "store:" in cmd:
        print("")
        for k, v in load_dict.items():
            print(k, *v)
        print("")
        stored_load_dict_name = cmd.split(":")[1]
        storage[stored_load_dict_name] = load_dict
        load_dict = {}

    elif "recall:" in cmd:
        stored_load_dict_name = cmd.split(":")[1]
        load_dict = storage[stored_load_dict_name]
        print("")
        for k, v in load_dict.items():
            print(k, *v)
        print("")

    elif "LC:" in cmd:
        compressed_load_dict = compressor(load_dict)
        LC = cmd.split(":")[1]
        ult = 0
        for L in LC.split(" "):
            for compressed_LC, value in compressed_load_dict.items():
                if L[-2:] == compressed_LC:
                    ult += float(L[:-2]) * value
        print("")
        print(f"ultimate: {ult}")
        print("")
    elif "rm:" in cmd:
        del load_dict[cmd.split(":")[1]]

    else:
        cmd = cmd.split(" ")
        load_dict[cmd[0]] = cmd[1:]
        print("")
        for k, v in load_dict.items():
            print(k, *v)
        print("")
