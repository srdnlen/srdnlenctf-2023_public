import re

with open("~/koenigsberg/k_dec.txt", "w") as f:
    for ea in Functions():
        if ea < 0x5f326 or ea > 0x92d89:
            continue
        decompiled = idaapi.decompile(ea)
        s = f"{decompiled}"
        node_nums = re.findall("visited\[.*\] = visited\[.*\]", s)
        xor_byte = re.findall(" \^ .*", s)
        f.write(f" {ea} {node_nums} {xor_byte}\n")
