
import json

test = [[i for i in range(10)] for _ in range(10)]

print(test)

with open('aux.json', 'w') as file:
    file.write(json.dumps(test))
