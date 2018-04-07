with open('schoolOfStudy.txt') as f:
    content = f.readlines()
arr = [i.strip().title() for i in content]
print(arr)