import time, json, os


root = os.path.dirname(__file__)
employees = json.load(open(os.path.join(root, '../../config/employees.json')))

print employees.items()

print map(lambda e: e[1]['gpio'], employees.items())