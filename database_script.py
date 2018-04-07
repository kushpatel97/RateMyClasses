from class_script import *

with open('txtfiles/department.txt') as f:
    content = f.readlines()
arr = [i.strip().title() for i in content]

# print(len(arr))
# print(arr)
dept_name = []
dept_id = []


for i in arr:
    dept_name.append(i[:-6])
    dept_id.append(i[-4:-1])

# Convert to ints
# dept_id = [int(i) for i in dept_id]

print(dept_name)
#Getclasscode takes in str of dept id
# print(dept_id)
#
# cn = getClassCode('010')
# cn = [int(i) for i in cn]
# print(dept_id[0])
# count = 0

#GET CLASS ALL MAJOR INFO
# for i in dept_id:
#     for j in range(0, len(getClassCode(i))):
#         # print(getClassCode(dept_id[j]))
#         # print(getClassName(dept_id[j]))
#         for k in range(0, len(getClassCode(dept_id[j]))):
#             query = "INSERT INTO `ratemyclass`.`Classes` (`Class_id`, `Class_name`, `dept_id`, `Uni_id`, `school_name`) VALUES ({}, '{}', {}, 1, 'School of Arts and Sciences');\n".format(
#                 getClassCode(dept_id[j])[k], getClassName(dept_id[j])[k], dept_id[count])
#             nf.write(query)
#         count = count + 1
#         print(dept_id[count])

# WRITE TO A FILE
nf = open('txtfiles/majorname.txt','w')
for i in dept_name:
    # q2 = 'INSERT INTO `ratemyclass`.`Classes` (`Class_id`, `Class_name`, `dept_id`, `Uni_id`, `school_name`) VALUES (123, `test1`, 198, 1, 'test');'
    # query = "INSERT INTO `ratemyclass`.`Department` (`dept_id`, `dept_name`, `Uni_id`) VALUES ({}, '{}', 1);\n".format(dept_id[i],dept_name[i])
    q3 = "INSERT INTO `ratemyclass`.`majors` (`major_name`) VALUES ('{}');\n".format(i)
    nf.write(q3)