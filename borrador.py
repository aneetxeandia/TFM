# import json
#
# data = {}
# data['rango_precio_1'] = 0
# data['rango_precio_2'] = 150000
# data['rango_precio_3'] = 300000
#
#
#
# with open('params.json', 'w') as outfile:
#     json.dump(data, outfile)
#





import json

with open('params.json') as json_file:
    data = json.load(json_file)
    # data['tagDelJson'] te daevuelve el valor para ese tag en params.json
    print(data['rango_precio_2'])
    print(data['AT'])
    print('')