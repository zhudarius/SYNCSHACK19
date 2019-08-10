import json
import re

#each element of the input list is (uos_code,[prohibitions],[prereqs])
def create_json(uos_list):

    data = {}
    data['units'] = []

    for uos in uos_list:

        data['units'].append({
            'uos_code': uos[0],
            'cp': uos[1],
            'prereqs': uos[2],
            'prohibitions': uos[3],
            'coreqs': uos[4]
        })

    with open('data.txt','w') as outfile:
        json.dump(data, outfile)


#grabs important information and formats into uos_list
def stripper(junk_list):

    uos_list = []

    for unit in junk_list:

        uos = []

        #get uos_code
        uos_code = unit[:8]
        #print("uos_code:",uos_code)

        #get credit points
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

        #print("credit points:", cp)

        #get prereqs
        unit = unit[i:]
        if re.search("\\n", unit):
            unit = re.sub("\\n", "", unit)


        if " P " in unit:
            if " N " in unit:
                prereq_str = re.search(' P (.*) N', unit)
                prereqs = re.findall(r"([A-Z]{4}[0-9]{4})", prereq_str.group(1))
                #print("prereq: ",prereqs)

            elif " C " in unit:
                prereq_str = re.search(' P (.*) C', unit)
                #print(prereq_str.group(1))
                prereqs = re.findall(r"([A-Z]{4}[0-9]{4})", prereq_str.group(1))
                #print("prereq: ",prereqs)

            else:
                prereq_str = unit
                #print(prereq_str)
                prereqs = re.findall(r"([A-Z]{4}[0-9]{4})", prereq_str)
                #print("prereq: ",prereqs)

        #get prohibitions
        if " N " in unit:

            x = unit.split(" N ")

            if " C " in x[1]:
                y = " N " + x[1]
                prohibition_str = re.search(' N (.*) C', y)
                prohibitions = re.findall(r"([A-Z]{4}[0-9]{4})", prohibition_str.group(1))
                #print("prohib: ", prohibitions)


            else:
                prohibition_str = x[1]
                prohibitions = re.findall(r"([A-Z]{4}[0-9]{4})", x[1])
                #print("prohib: ", prohibitions)

        if " C " in unit:

            final_split = unit.split(" C ")
            coreq = re.findall(r"([A-Z]{4}[0-9]{4})", final_split[1])
            #print("coreq: ", coreq)


        uos.append(uos_code)
        uos.append(cp)
        uos.append(prereqs)
        uos.append(prohibitions)
        uos.append(coreq)

        uos_list.append(uos)

    create_json(uos_list)
