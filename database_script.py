from class_script import *
from random import *

with open('txtfiles/department.txt') as f:
    content = f.readlines()
    # print(content)
arr = [i.strip().title() for i in content]

dept_name = []
dept_id = []


for i in arr:
    x = i[-4:-1]
    if x == '214' or x == '880':
        continue
    dept_name.append(i[:-6])
    dept_id.append(i[-4:-1])

# Convert to ints
# dept_id = [int(i) for i in dept_id]

# print(dept_name)
#Getclasscode takes in str of dept id

# ---------- Full List
A = []
# ---------- Half Lists
B = []
C = []
for i in dept_id:
    A.append(i)
    if int(i) < 500:
        B.append(i)
    if int(i) > 500:
        C.append(i)

count = 0



lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
file = open('txtfiles/tuples.txt','w')
for i in dept_id:
    for j in range(0, len(getClassInfo(i))):
        x = randint(1,5)
        y = randint(1,5)
        sem = 'Spring'
        yr = '2017'
        if random() < 0.5:
            sem = 'Fall'
            yr = '2018'
        query ="INSERT INTO `ratemyclass`.`Reviews` (`Class_id`, `Difficulty_rating`, `knowledge_gain_rating`, `review`, `Username`, `Review_year`, `Review_semester`) VALUES ('{}', '{}', '{}', '{}', 't6', '{}', '{}');\n".format(getClassInfo(i)[j][1], str(x), str(y), lorem ,yr,sem)
        file.write(query)

# for i in dept_id:
#     line = str(getClassName(i)) + '\n'
#     file.write(line)
# print(getClassName(198))

# nf = open('txtfiles/classData2.txt','w')
# cn_count = 0
# count = 0
# for i in C:
#     print('Starting: ' + str(C[count]))
#     for j in range(0, len(getClassInfo(i))):
#         query = "INSERT INTO `ratemyclass`.`Classes` (`Class_id`, `Class_name`, `dept_id`, `Uni_id`, `school_name`) VALUES ({}, '{}', {}, 1, 'School of Arts and Sciences');\n".format(getClassInfo(i)[j][1], getClassInfo(i)[j][0], C[count])
#         nf.write(query)
#     print('Finished: ' + str(C[count]))
#     count = count + 1

# cn = getClassCode('010')
# cn = [int(i) for i in cn]
# print(dept_id[0])
# count = 0

#GET CLASS ALL MAJOR INFO
# nf = open('txtfiles/classData.txt','w')
# for i in d2:
#     for j in range(0, len(getClassCode(i))):
#         print('Starting: ' + str(d2[count]))
#         # print(getClassCode(dept_id[j]))
#         # print(getClassName(dept_id[j]))
#         for k in range(0, len(getClassCode(d2[j]))):
#             query = "INSERT INTO `ratemyclass`.`Classes` (`Class_id`, `Class_name`, `dept_id`, `Uni_id`, `school_name`) VALUES ({}, '{}', {}, 1, 'School of Arts and Sciences');\n".format(
#                 getClassCode(d2[j])[k], getClassName(d2[j])[k], d2[count])
#             nf.write(query)
#         count = count + 1
#         print('Finished: ' + str(dept_id[count]))

# WRITE TO A FILE

# for i in dept_name:
#     pass
    # q2 = 'INSERT INTO `ratemyclass`.`Classes` (`Class_id`, `Class_name`, `dept_id`, `Uni_id`, `school_name`) VALUES (123, `test1`, 198, 1, 'test');'
    # query = "INSERT INTO `ratemyclass`.`Department` (`dept_id`, `dept_name`, `Uni_id`) VALUES ({}, '{}', 1);\n".format(dept_id[i],dept_name[i])
    # q3 = "INSERT INTO `ratemyclass`.`majors` (`major_name`) VALUES ('{}');\n".format(i)
    # nf.write(q3)