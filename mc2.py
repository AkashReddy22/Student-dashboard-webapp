import re
from enum import Enum
from collections import OrderedDict
import json
import pprint

class LineTypes(Enum):
    HEADING = "heading"
    COLUMNS = "column"
    DAY_ID = "day_id"
    DATA = "data"
    EMPTY = "empty"

class DataParser:
    def __extract_columns(self, line: str):
        data = re.split(r"\s+", line.strip())
        data = data[1:-1]
        return data

    def __extract_data(self, line: str):
        data = re.split(r"\s+", line.strip())
        item_id = data[0]
        data = data[1:]
        return {"id": item_id, "values": data}
        
    def __extract_day(self, line: str):
        day_regex = r"\[(\*,)(\w+)(,\*)\]"
        day_id = re.search(day_regex, line).group(2)
        return day_id

    def __parse_line(self, line: str):
        line = line.strip()
        if line.startswith("["):
            day_id = self.__extract_day(line)
            return day_id, LineTypes.DAY_ID
        elif line == "" or line.startswith(";"):
            return "", LineTypes.EMPTY
        elif line.startswith(":"):
            columns = self.__extract_columns(line)
            return columns, LineTypes.COLUMNS
        else:
            data = self.__extract_data(line)
            return data, LineTypes.DATA
    
    def parse(self, file_path: str):
        data_dict = OrderedDict()
        with open(file_path, "r") as f:
            day_id = ""
            for i, line in enumerate(f.readlines()):
                if i == 0:
                    continue
                try:
                    data, data_type = self.__parse_line(line)
                    if data_type == LineTypes.DAY_ID:
                        day_id = data
                        if day_id not in data_dict:
                            data_dict[day_id] = OrderedDict()
                    elif data_type == LineTypes.COLUMNS:
                        columns = data
                        for col in data:
                            if col not in data_dict[day_id]:
                                data_dict[day_id][col] = []
                    elif data_type == LineTypes.DATA:
                            item_id = data['id']
                            values = data['values']
                            if len(columns) == 0:
                                continue
                            for c,val in zip(columns, values):
                                if val != "0":
                                    data_dict[day_id][c].append(item_id)
                except KeyError as e:
                    print(f"Could not process line number: {i}")
        return data_dict
    
    def student_counts(self, file_path:str):
        data = self.parse(file_path)
        student_info = {}
        for day, day_data in data.items():

            for time, students in day_data.items():
    
                for student in students:
      
                    if student not in student_info:
                        student_info[student] = {
                            'count': 0,
                            'days': {}  
                        }
          
                    student_info[student]['count'] += 1
                    
                    if day not in student_info[student]['days']:
                        student_info[student]['days'][day] = []
                    
                    if time not in student_info[student]['days'][day]:
                        student_info[student]['days'][day].append(time)
        
        # Convert to list of tuples [(key, value), ...]
        info_items = list(student_info.items())

        # Sort list by key
        info_items.sort(key=lambda x: x[0].lower()) 

        # Convert back to dictionary
        sorted_student_info = dict(info_items)
            
        return sorted_student_info



if __name__ == "__main__":
    parser = DataParser()
    data = parser.parse("mc2.txt")
    counts = parser.student_counts("mc2.txt")
    with open ('table.json','w') as outfile:
        json.dump(data,outfile)
    
    with open ('summary.json','w') as countfile:
        json.dump(counts,countfile)
    students = {}
    with open('students.json') as f:
        student_data = json.load(f) 
        for e in student_data:
            asurite = e['email'].split('@')[0]
            first_name = e['first_name']
            last_name = e['last_name']
            
            students[asurite] = {'first_name':first_name,'last_name':last_name}
        
    with open('names.json','w') as fl:
        json.dump(students,fl)
    pprint.pprint(counts)
    # pprint.pprint(data)