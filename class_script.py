import requests

def getClassName(class_code):
    url = 'http://sis.rutgers.edu/soc/courses.json?subject={}&semester=92018&campus=NB&level=U'.format(class_code)
    response = requests.get(url).json()
    arr = []
    for i in response:
        arr.append(i['title'].title())
    return arr

def getClassCode(class_code):
    url = 'http://sis.rutgers.edu/soc/courses.json?subject={}&semester=92018&campus=NB&level=U'.format(class_code)
    response = requests.get(url).json()
    arr = []
    for i in response:
        arr.append(i['courseNumber'])
    return arr

# print(getClassCode(198))
# print(getClassName(198))