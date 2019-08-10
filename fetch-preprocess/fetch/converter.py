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

        try:
            i = 0
            while i < len(unit):
                if unit[i] == "\n":
                    break
                i+=1

            if unit[i+2].isdigit():
                cp = unit[i+1] + unit[i+2]

            else:
                cp = unit[i+1]

        except IndexError:
            continue
        #print("credit points:", cp)

        #get prereqs
        unit = unit[i:]
        if re.search("\\n", unit):
            unit = re.sub("\\n", "", unit)


        if " P " in unit:

            if " C " in unit:
                prereq_str = re.search(' P (.*) C', unit)
                #print(prereq_str.group(1))
                prereqs = re.findall(r"([A-Z]{4}[0-9]{4})", prereq_str.group(1))
                #print("prereq: ",prereqs)

            elif " N " in unit:
                prereq_str = re.search(' P (.*) N', unit)
                prereqs = re.findall(r"([A-Z]{4}[0-9]{4})", prereq_str.group(1))
                #print("prereq: ",prereqs)

            else:
                prereq_str = unit
                #print(prereq_str)
                prereqs = re.findall(r"([A-Z]{4}[0-9]{4})", prereq_str)
                #print("prereq: ",prereqs)

        else:
            prereqs = []

        #get prohibitions
        if " C " in unit:

            x = unit.split(" C ")

            if " N " in x[1]:
                y = " C " + x[1]
                coreq_str = re.search(' C (.*) N', y)
                coreq = re.findall(r"([A-Z]{4}[0-9]{4})", coreq_str.group(1))
                #print("coreq: ", coreq)


            else:
                coreq_str = x[1]
                coreq = re.findall(r"([A-Z]{4}[0-9]{4})", x[1])
                #print("coreq: ", coreq)

        else:
            coreq = []

        if " N " in unit:

            final_split = unit.split(" N ")
            prohibitions = re.findall(r"([A-Z]{4}[0-9]{4})", final_split[1])
            #print("prohibitions: ", prohibitions)

        else:
            prohibitions = []


        uos.append(uos_code)
        uos.append(cp)
        uos.append(prereqs)
        uos.append(prohibitions)
        uos.append(coreq)

        uos_list.append(uos)

    create_json(uos_list)





#uos_list = [('INFO1110',[],[]),('COMP2123',['INFO1105','INFO1905'],['INFO1110']),('ISYS2120',["INFO2120","INFO2820","COMP5138"],["INFO1113"]),('INFO3333',[],['INFO1111'])]
#create_json(uos_list)

#stripper(['COMP2017 \n6 P  INFO1113 OR INFO1105 OR INFO1905 OR INFO1103 C COMP2123 OR COMP2823 OR INFO1105 OR INFO1905 N  COMP2129 '])
