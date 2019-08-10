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

        #get uos_code
        uos_code = unit[:8]
        print("uos_code:",uos_code)

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

        print("credit points:", cp)

        #get prereqs
        unit = unit[i:]

        if " P " in unit:
            if " N " in unit:
                prereq_str = re.search(' P (.*)N', unit)
                #print(prereq_str.group(1))
                r1 = re.findall(r"([A-Z]{4}[0-9]{4})", prereq_str.group(1))
                print(r1)

            elif " C " in unit:
                prereq_str = re.search(' P (.*)C', unit)
                print(prereq_str.group(1))

            else:
                prereq_str = unit
                print(prereq_str)


        #prereq_str.toString()

        #print(prereq_str)

        #prereqs = []
        #if







#uos_list = [('INFO1110',[],[]),('COMP2123',['INFO1105','INFO1905'],['INFO1110']),('ISYS2120',["INFO2120","INFO2820","COMP5138"],["INFO1113"]),('INFO3333',[],['INFO1111'])]
#create_json(uos_list)

stripper(["COMP3308Introduction to Artificial Intelligence \n6 \xa0\xa0\n P Algorithms. Programming skills (e.g. Java, Python, C, C++, Matlab) INFO1110 N COMP3608 \n\nSemester 1"])
