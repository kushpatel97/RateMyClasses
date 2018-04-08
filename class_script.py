import requests

def getClassInfo(class_code):
    dicts = {}
    url = 'http://sis.rutgers.edu/soc/courses.json?subject={}&semester=92018&campus=NB&level=U'.format(class_code)
    response = requests.get(url).json()
    t1 = []
    t2 = []
    for i in response:
        if i['courseNumber'] == '880' or i['courseNumber'] == '214':
            continue
        t1.append(i['title'].title())
        t2.append(i['courseNumber'])
    for i in range(0, len(t1)):
        dicts[i] = (t1[i],t2[i])
    return dicts

def getClassName(class_code):
    url = 'http://sis.rutgers.edu/soc/courses.json?subject={}&semester=92018&campus=NB&level=U'.format(class_code)
    response = requests.get(url).json()
    arr = []
    for i in response:
        arr.append(i['title'].title())
    return arr

# print(getClassCode(198))
# print(getClassName(198))