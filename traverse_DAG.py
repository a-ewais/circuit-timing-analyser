import json
import numpy as np
from task_3 import Graph
# fp = './num_2.json'
# data = json.loads(open(fp).read())
#
# ports = {}
# nodes = {}
# types = {}
# Gates = []
#
# for i in data['modules']:
#     for j in data['modules'][i]:
#         for k in data['modules'][i]['ports']:
#             ports[k] = sum(data['modules'][i]['ports'][k]['bits'])
#             types[sum(data['modules'][i]['ports'][k]['bits'])] = data['modules'][i]['ports'][k]['direction']
#
#     for m in data['modules'][i]['cells']:
#         type_ = data['modules'][i]['cells'][m]['type']
#         temp = {}
#         out = -1
#         for l in data['modules'][i]['cells'][m]['connections']:
#             if l != 'Y' and l != 'Q':
#                 temp[l] = sum(data['modules'][i]['cells'][m]['connections'][l])
#             else:
#                 out = sum(data['modules'][i]['cells'][m]['connections'][l])
#                 types[out] = type_
#
#         for key, value in temp.items():
#             temp = []
#
#             if value in nodes.keys():
#                 temp = nodes[value]
#
#             # if type(out) is int:
#             #     out = np.append(out, 'Y')
#             #
#             # print(temp, out)
#
#             temp = np.append(temp, out)
#
#             nodes[value] = temp
#         pre_gates = np.append(data['modules'][i]['cells'][m]['connections']['Y'], type_)
#         connections = data['modules'][i]['cells'][m]['connections']
#
#         pre_gates = np.append(pre_gates, data['modules'][i]['cells'][m]['connections'])
#         Gates = np.append(Gates, pre_gates)
#
# Gates = [Gates[i*3:(i*3)+3] for i in range((len(Gates) // 3)+1)]
#
# outs = []
# for i in nodes.values():
#     for j in i:
#         if j not in nodes.keys():
#             outs.append(j)
# last = int((sorted(nodes.keys())[-1])+1)
# types[last] = 'output'
# for wire in outs:
#     nodes[wire] = np.array([last])
# types[0] = 'start'
# nodes[0] = np.array([])
# for index, type_ in types.items():
#     if type_ == 'input':
#         nodes[0] = np.append(nodes[0], index)
#
# # vis = []
# paths = []
# adj = nodes
#
#
# def dfs(index, type, to_print):
#     # vis[index] = 1
#     to_print.append(index)
#     if type == 0 and types[index] == 'DFFPOSX1':
#         paths.append(to_print)
#         return
#     if type == 1 and types[index] == 'output':
#         paths.append(to_print)
#         return
#     for i in range(len(adj[index])):
#         # if not vis[adj[index][i]]:
#         dfs(adj[index][i], type, list(to_print))
#
# target = open('./num_1.txt', 'w')
#
# dfs(0, 1, [])
#
# target.write('PATHS WITH PORT NUMBERS\n=======================\n')
# for i in range(len(paths)):
#     target.write('PATH ' + str(i))
#     target.write(str(paths[i]))
#     target.write("\n")
#
# target.write('\nPATHS WITH GATE NAMES\n======================\n')
# paths_to_read = [[types[node] for node in path] for path in paths]
#
# for i in range(len(paths_to_read)):
#     target.write('PATH ' + str(i))
#     target.write(str(paths_to_read[i]))
#     target.write("\n")
# target.close()
#
# # print('NODES:', nodes)
# # print('TYPES:', types)
# # print('PATHS:', paths)
# # print('GATES PATHS:', paths_to_read)
# #print('CONNECTIONS:', Gates)
#
# fp = 'osu350.json'
# liberty = json.loads(open(fp).read())
#
# pin_capacitances = {}
# tables = {}
#
# for i in liberty['cells']:
#     if 'pins' in liberty['cells'][i].keys():
#         temp = []
#         for k in liberty['cells'][i]['pins']:
#             pin = {}
#             if 'capacitance' in liberty['cells'][i]['pins'][k].keys():
#                 pin[k] = liberty['cells'][i]['pins'][k]['capacitance']
#                 temp = np.append(temp, pin)
#
#             if k is 'Y':
#                 if 'timing' in liberty['cells'][i]['pins']['Y']:
#                     pin[k] = {}
#                     for j in liberty['cells'][i]['pins']['Y']['timing']:
#                         pin[k][j] = {}
#                         if 'cell_rise' in liberty['cells'][i]['pins']['Y']['timing'][j]:
#                             if 'x_values' in liberty['cells'][i]['pins']['Y']['timing'][j]['cell_rise']:
#                                 y_values = liberty['cells'][i]['pins']['Y']['timing'][j]['cell_rise']['y_values']
#                                 x_values = liberty['cells'][i]['pins']['Y']['timing'][j]['cell_rise']['x_values']
#                                 table = liberty['cells'][i]['pins']['Y']['timing'][j]['cell_rise']['table']
#                                 pin[k][j]['cell_rise'] = {}
#                                 pin[k][j]['cell_rise']['y_values'] = y_values
#                                 pin[k][j]['cell_rise']['x_values'] = x_values
#                                 pin[k][j]['cell_rise']['table'] = table
#
#                                 y_values = liberty['cells'][i]['pins']['Y']['timing'][j]['cell_fall']['y_values']
#                                 x_values = liberty['cells'][i]['pins']['Y']['timing'][j]['cell_fall']['x_values']
#                                 table = liberty['cells'][i]['pins']['Y']['timing'][j]['cell_fall']['table']
#                                 pin[k][j]['cell_fall'] = {}
#                                 pin[k][j]['cell_fall']['y_values'] = y_values
#                                 pin[k][j]['cell_fall']['x_values'] = x_values
#                                 pin[k][j]['cell_fall']['table'] = table
#
#                                 y_values = liberty['cells'][i]['pins']['Y']['timing'][j]['rise_transition']['y_values']
#                                 x_values = liberty['cells'][i]['pins']['Y']['timing'][j]['rise_transition']['x_values']
#                                 table = liberty['cells'][i]['pins']['Y']['timing'][j]['rise_transition']['table']
#                                 pin[k][j]['rise_transition'] = {}
#                                 pin[k][j]['rise_transition']['y_values'] = y_values
#                                 pin[k][j]['rise_transition']['x_values'] = x_values
#                                 pin[k][j]['rise_transition']['table'] = table
#
#                                 y_values = liberty['cells'][i]['pins']['Y']['timing'][j]['fall_transition']['y_values']
#                                 x_values = liberty['cells'][i]['pins']['Y']['timing'][j]['fall_transition']['x_values']
#                                 table = liberty['cells'][i]['pins']['Y']['timing'][j]['fall_transition']['table']
#                                 pin[k][j]['fall_transition'] = {}
#                                 pin[k][j]['fall_transition']['y_values'] = y_values
#                                 pin[k][j]['fall_transition']['x_values'] = x_values
#                                 pin[k][j]['fall_transition']['table'] = table
#
#         pin_capacitances[i] = temp
#
# capacitances = {}
#
# for i in pin_capacitances:
#     for j in pin_capacitances[i]:
#         if i in capacitances.keys():
#             capacitances[i] = {**j, **capacitances[i]}
#         else:
#             capacitances[i] = j
#
# # print(Gates)
# # print(capacitances['AND2X1']['Y']['A'])
#

graph = Graph('./num_2.json')
cp,time = graph.get_critical_path()
print(cp,time)
# print(graph.get_node('6').get_delay())