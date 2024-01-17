import json
from bson import ObjectId


# Load user data from JSON 
with open('summary.json') as f:
    summary_data = json.load(f)

# Load MongoDB data from paste.txt
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


    