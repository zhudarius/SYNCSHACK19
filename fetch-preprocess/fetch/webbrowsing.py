from selenium import webdriver
from bs4 import BeautifulSoup

from converter import stripper
import pandas as pd
import re

class ParserInterface:
    def __init__(self, course_link):
        self.course_link = course_link
        #self.course_link = "https://sydney.edu.au/handbooks/engineering/advanced_computing/advanced_computing_table.shtml"


        self.driver = webdriver.Chrome()

        self.driver.get(self.course_link)


class Parser_USYD(ParserInterface):
    def __init__(self, course_link):
        ParserInterface.__init__(self, course_link)
        self.unit_row = []
        self.table_rows = []
        self.unit_list = []

        self.content = self.driver.page_source
        self.soup = BeautifulSoup(self.content, features="lxml")

        self.unit_html = self.soup.find('table', {'class':'tabledata_blue'})
        self.table_rows = self.unit_html.findAll('tr')

        for row in self.table_rows:
            self.unit_row.append(row.get_text().strip())

        for row in self.unit_row:
            if re.match(r"^([A-Z]{4}[0-9]{4})", row):
                #print(row)
                self.unit_list.append(row)
            

    def get_units(self):
        stripper(self.unit_list)
        pass
    
    # Debugging
    def print_unformatted_unit_list(self):
        for unit in self.unit_list:
           print(unit)
        #print(self.unit_list)

class Parser_UNSW(ParserInterface):
    def __init__(self, course_link):
        ParserInterface.__init__(self, course_link)
        self.unit_row = []
        self.table_rows = []
        self.unit_list = []

        self.content = self.driver.page_source
        self.soup = BeautifulSoup(self.content, features="lxml")

        self.unit_html = self.soup.find('table', {'class':'tabledata_blue'})
        self.table_rows = self.unit_html.findAll('tr')
        driver.find_element_by_xpath("//*[@id="subjectUndergraduate"]/div/button")
        

        for row in self.table_rows:
            self.unit_row.append(row.get_text().strip())

        for row in self.unit_row:
            if re.match(r"^([A-Z]{4}[0-9]{4})", row):
                #print(row)
                self.unit_list.append(row)
            

    def get_units(self):
        stripper(self.unit_list)
        pass
    
    # Debugging
    def print_unformatted_unit_list(self):
        for unit in self.unit_list:
           print(unit)
        #print(self.unit_list)


parser_usyd = Parser_USYD("https://sydney.edu.au/handbooks/engineering/advanced_computing/advanced_computing_table.shtml")
#parser.print_unformatted_unit_list()
#parser_usyd.get_units()

parser_unsw = Parser_UNSW("https://www.handbook.unsw.edu.au/ComputerScience/browse?sa=91ce03204f0f5b00eeb3eb4f0310c782")
#parser.print_unformatted_unit_list()
#parser_unsw.get_units()

print("end")






