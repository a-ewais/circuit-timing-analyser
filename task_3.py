import numpy as np
import json
from node import Node

# class path:
#     def __init__(self,graph):

class Graph:
    adj = [] #adjacency matrix with the nodes indeces
    types =[] #the type of each node
    paths =[] #the paths that starts at input
    ff_paths =[] #the paths that starts at ff
    gates ={} #dictionary with node objects describing the graph

    def __init__(self,circuit_file,output_file=None,library_file='osu350.json'):
        self.adj,self.types,Gates = self.__build_graph(circuit_file)
        capacitances, flip_flops = self.__read_library(library_file)
        self.paths = []
        self.ff_paths = []
        self.dfs(0, 1, [])
        for i in range(len(Gates)):
            if len(Gates[i]) == 3:
                pins = {}
                for name, connected_to in Gates[i][2].items():
                    if name != 'Y':
                        pins[name] = {'cell_rise': capacitances[Gates[i][1]]['Y'][name]['cell_rise'],
                                      'cell_fall': capacitances[Gates[i][1]]['Y'][name]['cell_fall'],
                                      'rise_transition': capacitances[Gates[i][1]]['Y'][name]['rise_transition'],
                                      'fall_transition': capacitances[Gates[i][1]]['Y'][name]['fall_transition'],
                                      'capacitance': capacitances[Gates[i][1]][name],
                                      'connected_to': connected_to}
                pins['Y'] = {
                    'connected_to': Gates[i][2]['Y']
                }
                Gates[i][2] = pins

        self.gates = {}
        for gate in Gates:
            if len(gate) > 1:
                self.gates[gate[0]] = Node(gate[0], gate[1], gate[2],self)

        for name in self.adj:
            name = int(name)
            if name!=0 and str(name) not in self.gates:
                self.gates[str(name)] = Node(str(name),'input',None,self)
        for _,gate in sorted(self.gates.items()):
            print('delay', gate.name,gate.get_delay())


    def dfs(self,index, type, to_print):
        # vis[index] = 1
        to_print.append(index)
        if type == 0 and self.types[index] == 'DFFPOSX1':
            self.ff_paths.append(to_print)
            return
        if type == 1 and self.types[index] == 'output':
            self.paths.append(to_print)
            return
        for i in range(len(self.adj[index])):
            # if not vis[adj[index][i]]:
            self.dfs(self.adj[index][i], type, list(to_print))


    def __read_library(self,library_file = 'osu350.json'):
        liberty = json.loads(open(library_file).read())
        FLIP_FLOPS = {'hold': {}, 'setup': {}}
        pin_capacitances = {}

        for i in liberty['cells']:
            if i == 'DFFPOSX1':
                print('ANA FLIP FLOP')
                if 'pins' in liberty['cells'][i].keys():
                    temp = []
                    for k in liberty['cells'][i]['pins']:
                        pin = {}
                        if 'capacitance' in liberty['cells'][i]['pins'][k].keys():
                            pin[k] = liberty['cells'][i]['pins'][k]['capacitance']
                            temp = np.append(temp, pin)

                        if k is 'Q':
                            if 'timing' in liberty['cells'][i]['pins']['Q']:
                                pin[k] = {}
                                for j in liberty['cells'][i]['pins']['Q']['timing']:
                                    pin[k][j] = {}
                                    if 'cell_rise' in liberty['cells'][i]['pins']['Q']['timing'][j]:
                                        if 'x_values' in liberty['cells'][i]['pins']['Q']['timing'][j]['cell_rise']:
                                            y_values = liberty['cells'][i]['pins']['Q']['timing'][j]['cell_rise'][
                                                'y_values']
                                            x_values = liberty['cells'][i]['pins']['Q']['timing'][j]['cell_rise'][
                                                'x_values']
                                            table = liberty['cells'][i]['pins']['Q']['timing'][j]['cell_rise']['table']
                                            pin[k][j]['cell_rise'] = {}
                                            pin[k][j]['cell_rise']['y_values'] = y_values
                                            pin[k][j]['cell_rise']['x_values'] = x_values
                                            pin[k][j]['cell_rise']['table'] = table

                                            y_values = liberty['cells'][i]['pins']['Q']['timing'][j]['cell_fall'][
                                                'y_values']
                                            x_values = liberty['cells'][i]['pins']['Q']['timing'][j]['cell_fall'][
                                                'x_values']
                                            table = liberty['cells'][i]['pins']['Q']['timing'][j]['cell_fall']['table']
                                            pin[k][j]['cell_fall'] = {}
                                            pin[k][j]['cell_fall']['y_values'] = y_values
                                            pin[k][j]['cell_fall']['x_values'] = x_values
                                            pin[k][j]['cell_fall']['table'] = table

                                            y_values = liberty['cells'][i]['pins']['Q']['timing'][j]['rise_transition'][
                                                'y_values']
                                            x_values = liberty['cells'][i]['pins']['Q']['timing'][j]['rise_transition'][
                                                'x_values']
                                            table = liberty['cells'][i]['pins']['Q']['timing'][j]['rise_transition'][
                                                'table']
                                            pin[k][j]['rise_transition'] = {}
                                            pin[k][j]['rise_transition']['y_values'] = y_values
                                            pin[k][j]['rise_transition']['x_values'] = x_values
                                            pin[k][j]['rise_transition']['table'] = table

                                            y_values = liberty['cells'][i]['pins']['Q']['timing'][j]['fall_transition'][
                                                'y_values']
                                            x_values = liberty['cells'][i]['pins']['Q']['timing'][j]['fall_transition'][
                                                'x_values']
                                            table = liberty['cells'][i]['pins']['Q']['timing'][j]['fall_transition'][
                                                'table']
                                            pin[k][j]['fall_transition'] = {}
                                            pin[k][j]['fall_transition']['y_values'] = y_values
                                            pin[k][j]['fall_transition']['x_values'] = x_values
                                            pin[k][j]['fall_transition']['table'] = table

                    pin_capacitances[i] = temp

                if 'hold_rising' in liberty['cells'][i].keys():
                    FLIP_FLOPS['hold'] = {i: {'hold_rising': {'rise_constraint': {}, 'fall_constraint': {}}}}

                    y_values = liberty['cells'][i]['hold_rising']['rise_constraint']['y_values']
                    x_values = liberty['cells'][i]['hold_rising']['rise_constraint']['x_values']
                    table = liberty['cells'][i]['hold_rising']['rise_constraint']['table']

                    FLIP_FLOPS['hold'][i]['hold_rising']['rise_constraint']['y_values'] = y_values
                    FLIP_FLOPS['hold'][i]['hold_rising']['rise_constraint']['x_values'] = x_values
                    FLIP_FLOPS['hold'][i]['hold_rising']['rise_constraint']['table'] = table

                    y_values = liberty['cells'][i]['hold_rising']['fall_constraint']['y_values']
                    x_values = liberty['cells'][i]['hold_rising']['fall_constraint']['x_values']
                    table = liberty['cells'][i]['hold_rising']['fall_constraint']['table']

                    FLIP_FLOPS['hold'][i]['hold_rising']['fall_constraint']['y_values'] = y_values
                    FLIP_FLOPS['hold'][i]['hold_rising']['fall_constraint']['x_values'] = x_values
                    FLIP_FLOPS['hold'][i]['hold_rising']['fall_constraint']['table'] = table

                if 'setup_rising' in liberty['cells'][i].keys():
                    FLIP_FLOPS['setup'] = {i: {'setup_rising': {'rise_constraint': {}, 'fall_constraint': {}}}}

                    y_values = liberty['cells'][i]['setup_rising']['rise_constraint']['y_values']
                    x_values = liberty['cells'][i]['setup_rising']['rise_constraint']['x_values']
                    table = liberty['cells'][i]['setup_rising']['rise_constraint']['table']

                    FLIP_FLOPS['setup'][i]['setup_rising']['rise_constraint']['y_values'] = y_values
                    FLIP_FLOPS['setup'][i]['setup_rising']['rise_constraint']['x_values'] = x_values
                    FLIP_FLOPS['setup'][i]['setup_rising']['rise_constraint']['table'] = table

                    y_values = liberty['cells'][i]['setup_rising']['fall_constraint']['y_values']
                    x_values = liberty['cells'][i]['setup_rising']['fall_constraint']['x_values']
                    table = liberty['cells'][i]['setup_rising']['fall_constraint']['table']

                    FLIP_FLOPS['setup'][i]['setup_rising']['fall_constraint']['y_values'] = y_values
                    FLIP_FLOPS['setup'][i]['setup_rising']['fall_constraint']['x_values'] = x_values
                    FLIP_FLOPS['setup'][i]['setup_rising']['fall_constraint']['table'] = table

            else:
                if 'pins' in liberty['cells'][i].keys():
                    temp = []
                    for k in liberty['cells'][i]['pins']:
                        pin = {}
                        if 'capacitance' in liberty['cells'][i]['pins'][k].keys():
                            pin[k] = liberty['cells'][i]['pins'][k]['capacitance']
                            temp = np.append(temp, pin)

                        if k is 'Y':
                            if 'timing' in liberty['cells'][i]['pins']['Y']:
                                pin[k] = {}
                                for j in liberty['cells'][i]['pins']['Y']['timing']:
                                    pin[k][j] = {}
                                    if 'cell_rise' in liberty['cells'][i]['pins']['Y']['timing'][j]:
                                        if 'x_values' in liberty['cells'][i]['pins']['Y']['timing'][j]['cell_rise']:
                                            y_values = liberty['cells'][i]['pins']['Y']['timing'][j]['cell_rise'][
                                                'y_values']
                                            x_values = liberty['cells'][i]['pins']['Y']['timing'][j]['cell_rise'][
                                                'x_values']
                                            table = liberty['cells'][i]['pins']['Y']['timing'][j]['cell_rise']['table']
                                            pin[k][j]['cell_rise'] = {}
                                            pin[k][j]['cell_rise']['y_values'] = y_values
                                            pin[k][j]['cell_rise']['x_values'] = x_values
                                            pin[k][j]['cell_rise']['table'] = table

                                            y_values = liberty['cells'][i]['pins']['Y']['timing'][j]['cell_fall'][
                                                'y_values']
                                            x_values = liberty['cells'][i]['pins']['Y']['timing'][j]['cell_fall'][
                                                'x_values']
                                            table = liberty['cells'][i]['pins']['Y']['timing'][j]['cell_fall']['table']
                                            pin[k][j]['cell_fall'] = {}
                                            pin[k][j]['cell_fall']['y_values'] = y_values
                                            pin[k][j]['cell_fall']['x_values'] = x_values
                                            pin[k][j]['cell_fall']['table'] = table

                                            y_values = liberty['cells'][i]['pins']['Y']['timing'][j]['rise_transition'][
                                                'y_values']
                                            x_values = liberty['cells'][i]['pins']['Y']['timing'][j]['rise_transition'][
                                                'x_values']
                                            table = liberty['cells'][i]['pins']['Y']['timing'][j]['rise_transition'][
                                                'table']
                                            pin[k][j]['rise_transition'] = {}
                                            pin[k][j]['rise_transition']['y_values'] = y_values
                                            pin[k][j]['rise_transition']['x_values'] = x_values
                                            pin[k][j]['rise_transition']['table'] = table

                                            y_values = liberty['cells'][i]['pins']['Y']['timing'][j]['fall_transition'][
                                                'y_values']
                                            x_values = liberty['cells'][i]['pins']['Y']['timing'][j]['fall_transition'][
                                                'x_values']
                                            table = liberty['cells'][i]['pins']['Y']['timing'][j]['fall_transition'][
                                                'table']
                                            pin[k][j]['fall_transition'] = {}
                                            pin[k][j]['fall_transition']['y_values'] = y_values
                                            pin[k][j]['fall_transition']['x_values'] = x_values
                                            pin[k][j]['fall_transition']['table'] = table

                    pin_capacitances[i] = temp

        capacitances = {}

        for i in pin_capacitances:
            for j in pin_capacitances[i]:
                if i in capacitances.keys():
                    capacitances[i] = {**j, **capacitances[i]}
                else:
                    capacitances[i] = j

        return capacitances, FLIP_FLOPS

    def __build_graph(self,json_file = './num_2.json'):
        data = json.loads(open(json_file).read())
        ports = {}
        nodes = {}
        types = {}
        Gates = []

        for i in data['modules']:
            for j in data['modules'][i]:
                for k in data['modules'][i]['ports']:
                    ports[k] = sum(data['modules'][i]['ports'][k]['bits'])
                    types[sum(data['modules'][i]['ports'][k]['bits'])] = data['modules'][i]['ports'][k]['direction']

            for m in data['modules'][i]['cells']:
                type_ = data['modules'][i]['cells'][m]['type']
                temp = {}
                out = -1
                for l in data['modules'][i]['cells'][m]['connections']:
                    if l != 'Y' and l != 'Q':
                        temp[l] = sum(data['modules'][i]['cells'][m]['connections'][l])
                    else:
                        out = sum(data['modules'][i]['cells'][m]['connections'][l])
                        types[out] = type_

                for key, value in temp.items():
                    temp = []

                    if value in nodes.keys():
                        temp = nodes[value]

                    # if type(out) is int:
                    #     out = np.append(out, 'Y')
                    #
                    # print(temp, out)

                    temp = np.append(temp, out)

                    nodes[value] = temp
                pre_gates = np.append(data['modules'][i]['cells'][m]['connections']['Y'], type_)
                pre_gates = np.append(pre_gates, data['modules'][i]['cells'][m]['connections'])
                Gates = np.append(Gates, pre_gates)

        Gates = [Gates[i * 3:(i * 3) + 3] for i in range((len(Gates) // 3) + 1)]

        outs = []
        for i in nodes.values():
            for j in i:
                if j not in nodes.keys():
                    outs.append(j)
        last = int((sorted(nodes.keys())[-1]) + 1)
        types[last] = 'output'
        for wire in outs:
            nodes[wire] = np.array([last])
        types[0] = 'start'
        nodes[0] = np.array([])
        for index, type_ in types.items():
            if type_ == 'input':
                nodes[0] = np.append(nodes[0], index)
        return nodes,types,Gates

    def write_paths(self,file,paths,types):
        target = open(file, 'w')
        target.write('PATHS WITH PORT NUMBERS\n=======================\n')
        for i in range(len(paths)):
            target.write('PATH ' + str(i))
            target.write(str(paths[i]))
            target.write("\n")

        target.write('\nPATHS WITH GATE NAMES\n======================\n')
        paths_to_read = [[types[node] for node in path] for path in paths]

        for i in range(len(paths_to_read)):
            target.write('PATH ' + str(i))
            target.write(str(paths_to_read[i]))
            target.write("\n")
        target.close()

    def get_node(self,index):
        return self.gates[index]

    def get_critical_path(self):
        mx = 0
        mx_index = 0
        for path in self.paths:
            path.pop()
            path.pop(0)
            sum = 0
            for i in path:

                i = str(int(i))
                sum += self.get_node(i).get_delay()
            if(sum > mx):
                mx =sum
                mx_index = path
        return mx_index,mx

    
