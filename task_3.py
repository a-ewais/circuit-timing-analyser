import numpy as np
import json
from node import Node


# class path:
#     def __init__(self,graph):

class Graph:
    adj = []  # adjacency matrix with the nodes indeces
    types = []  # the type of each node
    paths = {'ito': [],
             'ftf': [],
             'itf': [],
             'fto': []}  # the paths
    gates = {}  # dictionary with node objects describing the graph
    module_name = ''
    timing_constraints = {}

    def __init__(self, circuit_file, output_file=None,
                 library_file='osu350.json', constraints_file='./timing_constraints.json',
                 skews_file ='./clock_skews.json'):
        self.adj, self.types, Gates = self.__build_graph(circuit_file)
        capacitances, flip_flops = self.__read_library(library_file)
        self.timing_constraints = self.__get_constraints(constraints_file)
        self.skews = self.__get_skews(skews_file)
        print(self.skews) #needs fixing
        print(self.types)
        print(self.adj)
        self.dfs(0, 0, [])
        self.dfs(0, 1, [])
        for i in self.types.keys():
            if self.types[i] == 'DFFPOSX1':
                self.dfs(i, 2, [])
                self.dfs(i, 3, [])
        print(self.paths)
        for i in range(len(Gates)):
            if len(Gates[i]) == 3:
                pins = {}
                pin_type = 'Y'
                for name, connected_to in Gates[i][2].items():
                    if name != 'Y' and name != 'Q':
                        if 'Y' in capacitances[Gates[i][1]]:
                            pin_type = 'Y'
                            pins[name] = {'cell_rise': capacitances[Gates[i][1]]['Y'][name]['cell_rise'],
                                          'cell_fall': capacitances[Gates[i][1]]['Y'][name]['cell_fall'],
                                          'rise_transition': capacitances[Gates[i][1]]['Y'][name]['rise_transition'],
                                          'fall_transition': capacitances[Gates[i][1]]['Y'][name]['fall_transition'],
                                          'capacitance': capacitances[Gates[i][1]][name],
                                          'connected_to': connected_to}
                        elif 'Q' in capacitances[Gates[i][1]]:
                            pin_type = 'Q'
                            if name == 'CLK':
                                pins[name] = {'cell_rise': capacitances[Gates[i][1]]['Q'][name]['cell_rise'],
                                              'cell_fall': capacitances[Gates[i][1]]['Q'][name]['cell_fall'],
                                              'rise_transition': capacitances[Gates[i][1]]['Q'][name][
                                                  'rise_transition'],
                                              'fall_transition': capacitances[Gates[i][1]]['Q'][name][
                                                  'fall_transition'],
                                              'capacitance': capacitances[Gates[i][1]][name],
                                              'connected_to': connected_to
                                              }
                            else:
                                pins[name] = {
                                    'capacitance': capacitances[Gates[i][1]][name],
                                    'connected_to': connected_to
                                }
                pins[pin_type] = {
                    'connected_to': Gates[i][2][pin_type]
                }
                Gates[i][2] = pins

        self.gates = {}
        for gate in Gates:
            if len(gate) > 1:
                self.gates[gate[0]] = Node(gate[0], gate[1], gate[2], self)

        for name in self.adj:
            name = int(name)
            if name != 0 and str(name) not in self.gates:
                self.gates[str(name)] = Node(str(name), 'input', None, self)

        # print(self.types)
        ff_info = {
            'hold_rise': flip_flops['hold']['DFFPOSX1']['hold_rising']['rise_constraint'],
            'hold_fall': flip_flops['hold']['DFFPOSX1']['hold_rising']['fall_constraint'],
            'setup_rise': flip_flops['setup']['DFFPOSX1']['setup_rising']['rise_constraint'],
            'setup_fall': flip_flops['setup']['DFFPOSX1']['setup_rising']['fall_constraint']
        }
        for gate in self.gates.values():
            gate.handle_ff(ff_info)
        for _, gate in sorted(self.gates.items()):
            print('delay', gate.name, gate.get_delay())

    def dfs(self, index, type, to_print):
        # vis[index] = 1
        to_print.append(int(index))
        if type == 0 and self.types[index] == 'DFFPOSX1':
            self.paths['itf'].append(to_print)
            return
        if type == 1:
            if self.types[index] == 'output':
                self.paths['ito'].append(to_print)
                return
            if self.types[index] == 'DFFPOSX1':
                return
        if type == 2 and self.types[index] == 'DFFPOSX1'\
                and len(to_print) > 1:
            self.paths['ftf'].append(to_print)
            return
        if type == 3:
            if self.types[index] == 'output':
                self.paths['fto'].append(to_print)
                return
            if self.types[index] == 'DFFPOSX1':
                return
        if self.types[index] == 'output':
            return
        for i in range(len(self.adj[index])):
            self.dfs(self.adj[index][i], type, list(to_print))

    def __read_library(self, library_file='osu350.json'):
        liberty = json.loads(open(library_file).read())
        FLIP_FLOPS = {'hold': {}, 'setup': {}}
        pin_capacitances = {}

        for i in liberty['cells']:
            if i == 'DFFPOSX1':
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

    def __build_graph(self, json_file):
        data = json.loads(open(json_file).read())
        index_start = json_file.find('num')
        index_end = json_file.find('.json')
        self.module_name = json_file[index_start:index_end]

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

                if 'Y' in data['modules'][i]['cells'][m]['connections']:
                    pre_gates = np.append(data['modules'][i]['cells'][m]['connections']['Y'], type_)
                    pre_gates = np.append(pre_gates, data['modules'][i]['cells'][m]['connections'])
                elif 'Q' in data['modules'][i]['cells'][m]['connections']:
                    pre_gates = np.append(data['modules'][i]['cells'][m]['connections']['Q'], type_)
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
        return nodes, types, Gates

    def write_paths(self, file, paths, types):
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

    def get_node(self, index):
        if type(index) is not str:
            index = str(index)
        return self.gates[index]

    def get_critical_path(self):
        mx = 0
        mx_index = 0
        for path in self.paths['ito']:
            path.pop()
            path.pop(0)
            sum = 0
            for i in path:
                i = str(int(i))
                sum += self.get_node(i).get_delay()
            if (sum > mx):
                mx = sum
                mx_index = path
        print(self.paths)
        for path in self.paths['ftf']:
            print(path)
            self.__inspect_ff_path(path)
        return mx_index, mx


    def __inspect_ff_path(self,path):
        tpd = 0
        for i in path:
            gate = self.get_node(i)
            if gate.type != 'DFFPOSX1':
                tpd = tpd + gate.get_delay()
        end_node = self.get_node(path[-1])
        start_node = self.get_node(path[0])
        setup,hold,slack = end_node.check_constraints(tpd,start_node.get_delay(),start_node.skew)
        if hold :
            print('==========================================')
            print('hold time violation in FF_FF path:')
            print(path)
            print('==========================================')

        if setup:
            print('==========================================')
            print('setup time violation in FF_FF path:')
            print(path)
            print(slack)
            print('==========================================')




    def __get_skews(self, json_file='./clock_skews.json'):
        data = json.loads(open(json_file).read())
        clock_skews = {}
        for _, gate in sorted(self.gates.items()):
            Type = gate.name[:8]
            index = gate.name[9:]
            if Type == 'DFFPOSX1':
                clock_skews[gate.name] = data['modules'][self.module_name]['clock_skew'][gate.name]

        return clock_skews

    def __get_constraints(self, json_file='./timing_constraints.json'):
        data = json.loads(open(json_file).read())
        timing_constraints={}
        timing_constraints['input_delay'] = data['modules'][self.module_name]['input_delay']
        timing_constraints['output_delay'] = data['modules'][self.module_name]['output_delay']
        timing_constraints['clock_period'] = data['modules'][self.module_name]['clock_period']

        return timing_constraints
