from selenium import webdriver
from bs4 import BeautifulSoup

from converter import stripper
import pandas as pd
import re

class Parser:
    def __init__(self, course_link):
        self.course_link = course_link
        #self.course_link = "https://sydney.edu.au/handbooks/engineering/advanced_computing/advanced_computing_table.shtml"


        self.driver = webdriver.Chrome()

        self.driver.get(self.course_link)
        self.unit_row = []
        self.table_rows = []
        self.unit_list = []

        self.content = self.driver.page_source
        self.soup = BeautifulSoup(self.content)

        self.unit_html = self.soup.find('table', {'class':'tabledata_blue'})
        self.table_rows = self.unit_html.findAll('tr')

        for row in self.table_rows:
            self.unit_row.append(row.get_text().strip())

        for row in self.unit_row:
            if re.match(r"^([A-Z]{4}[0-9]{4})", row):
                #print(row)
                self.unit_list.append(row)
            
            
        #print(self.unit_list)

    def get_units(self):
        #stripper(self.unit_list)
        pass

    def print_unformatted_unit_list(self):
        for unit in self.unit_list:
            print(unit)


parser = Parser("https://sydney.edu.au/handbooks/engineering/advanced_computing/advanced_computing_table.shtml")
parser.print_unformatted_unit_list()


print("trash")







