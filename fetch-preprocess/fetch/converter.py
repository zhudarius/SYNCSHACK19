import json
import re
from parsetree import *

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

#grabs list of strings consisting of unit code, 'and', 'or'
def and_or_trigger(str_lst):

    i = 0
    while i < len(str_lst):
        if str_lst[i] == " AND " or str_lst[i] == " and ":
            str_lst[i] = "&"
        elif str_lst[i] == " OR " or str_lst[i] == " or ":
            str_lst[i] = "|"
        i+=1

    separator = ''
    inp = separator.join(str_lst)
    out = generateParseTree(inp)
    return out





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
                prereq_str = re.search(' P (.*) C ', unit)
                #print(prereq_str.group(1))
                prereqs = re.findall(r"[A-Z]{4}[0-9]{4}| AND | OR |\(|\)| and | or ", prereq_str.group(1))
                #print("prereq: ",prereqs)
                tester = re.findall(r"[A-Z]{4}[0-9]{4}",prereq_str.group(1))
                if len(tester) == 1:
                    preq = tester
                else:
                    preq = and_or_trigger(prereqs)

            elif " N " in unit:
                prereq_str = re.search(' P (.*) N ', unit)
                prereqs = re.findall(r"[A-Z]{4}[0-9]{4}| AND | OR |\(|\)| and | or ", prereq_str.group(1))
                #print("prereq: ",prereqs)
                tester = re.findall(r"[A-Z]{4}[0-9]{4}",prereq_str.group(1))
                if len(tester) == 1:
                    preq = tester
                else:
                    preq = and_or_trigger(prereqs)

            else:
                prereq_str = unit
                #print(prereq_str)
                prereqs = re.findall(r"[A-Z]{4}[0-9]{4}| AND | OR |\(|\)| and | or ", prereq_str)
                #print("prereq: ",prereqs)
                preq = and_or_trigger(prereqs)

        else:
            preq = []

        #get prohibitions
        if " C " in unit:

            x = unit.split(" C ")

            if " N " in x[1]:
                y = " C " + x[1]
                coreq_str = re.search(' C (.*) N ', y)
                coreq = re.findall(r"[A-Z]{4}[0-9]{4}| AND | OR |\(|\)| and | or ", coreq_str.group(1))
                #print("coreq: ", coreq)
                coreqq = and_or_trigger(coreq)


            else:
                coreq_str = x[1]
                coreq = re.findall(r"[A-Z]{4}[0-9]{4}| AND | OR |\(|\)| and | or ", x[1])
                #print("coreq: ", coreq)
                coreqq = and_or_trigger(coreq)

        else:
            coreqq = []

        if " N " in unit:

            final_split = unit.split(" N ")
            prohibitions = re.findall(r"[A-Z]{4}[0-9]{4}| AND | OR |\(|\)| and | or ", final_split[1])
            #print("prohibitions: ", prohibitions)

        else:
            prohibitions = []


        uos.append(uos_code)
        uos.append(cp)
        uos.append(preq)
        uos.append(prohibitions)
        uos.append(coreqq)

        uos_list.append(uos)

    create_json(uos_list)





#uos_list = [('INFO1110',[],[]),('COMP2123',['INFO1105','INFO1905'],['INFO1110']),('ISYS2120',["INFO2120","INFO2820","COMP5138"],["INFO1113"]),('INFO3333',[],['INFO1111'])]
#create_json(uos_list)

#stripper(['COMP2017 \n6 P  INFO1113 or slakdfjlkaj or aslkrfjkljfsd N  COMP2129 '])
