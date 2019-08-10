import json
import re

#each element of the input list is (uos_code,[prohibitions],[prereqs])
def create_json(uos_list):

    data = {}
    data['units'] = []

    for uos in uos_list:

        data['units'].append({
            'uos_code': uos[0],
            'prohibitions': uos[1],
            'prereqs': uos[2]
        })

    with open('data.txt','w') as outfile:
        json.dump(data, outfile)

        print("helloworld")

#grabs important information and formats into uos_list
def stripper(junk_list):

    for unit in junk_list:

        uos_code = unit[:8]
        print("uos_code:",uos_code)

        unit = unit[8:]

        i = 0
        while i < len(unit):
            if unit[i] == "\n":
                break
            i+=1

        if unit[i+2].isdigit():
            cp = unit[i+1] + unit[i+2]

        else:
            cp = unit[i+1]

        print("credit points:", cp)

        unit = unit[i:]
        prereq = re.search(' A (.*)N', unit)
        print(prereq.group(1))

