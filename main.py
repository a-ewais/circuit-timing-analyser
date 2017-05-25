from task_3 import Graph
# import pygraphviz as pgv

graph = Graph('./Gatlevel_Netlists/num_9.json')

# cp, time = graph.get_critical_path()
# print('critical_path = ',cp, time)


# G=pgv.AGraph(strict=False, directed=True)
def draw_graph(graph):
    target = open('graph.gv', 'w')

    target.write("digraph G {\n")

    for node,arr in graph.adj.items():
        if graph.types[int(node)] != 'output' and graph.types[int(node)] != 'start':
            rt = graph.get_node(int(node)).required
            at = graph.get_node(int(node)).arrival
            slack = graph.get_node(int(node)).slack
        else:
            rt = graph.timing_constraints['clock_period'] - graph.timing_constraints['output_delay']
            at = 0
            slack = 0
        start_node = 'start'

        if graph.types[int(node)] != 'output' and graph.types[int(node)] != 'start':
            start_node = graph.get_node(int(node)).name

        target.write(str(start_node) + ' [label="Name:' + str(start_node) + '\\nRT: ' + '%0.2f'%rt + '\\nAT: ' + '%0.2f'%at + '\\nSlack: ' + '%0.2f'%slack + '"];\n')
        for i in arr:
            start = 'start'
            end = 'output'
            if graph.types[int(node)] != 'start':
                start = graph.get_node(int(node)).name

            if graph.types[int(i)] != 'output':
                end = graph.get_node(int(i)).name
            target.write(str(start) + ' -> ' + str(end) + ';\n')

    target.write('}')
    target.close()

def generate_report(graph, output_path='report.txt'):
    cp, time ,type = graph.get_critical_path()
    print(cp , time, type)
    target = open(output_path, 'w')
    target.write("=================================\n")
    target.write("==STATIC TIMING ANALYSIS REPORT==\n")
    target.write("=================================\n\n")
    target.write("TIMING PATHS\n============\n")

    for key, value in graph.paths.items():
        if key == 'ito':
            target.write("Input to Output Paths\n---------------------\n")
        elif key == 'fto':
            target.write("Register to Output Paths\n------------------------\n")
        elif key == 'ftf':
            target.write("Register to Register Paths\n--------------------------\n")
        elif key == 'itf':
            target.write("Input to Register Paths\n-----------------------\n")

        if not len(value):
            target.write("None Found\n\n")
        else:
            target.write(str(value) + "\n\n")

    target.write("CRITICAL PATH\n=============\n")
    target.write("Path: " + str(cp) + "\nDelay: " + str(round(time, 3)) + "\nType: " + type+ "\n")
    target.write("Minimum clock cycle should be: " + str(round(time, 3)) + " ps\n\n")
    target.write("----------------------------------------------------\n")
    target.write("Pin\ttype\t\tIncr\t\tPath delay\n")
    target.write("----------------------------------------------------\n")

    path_delay = 0.0
    # for i in graph.critical_path.nodes:
    for i in cp:

        path_delay += graph.gates[str(i)].delay
        target.write(
            str(i) + "\t" + str(graph.types[int(i)]) + "\t\t" + str(round(graph.gates[str(i)].delay, 3)) + "\t\t" + str(
                round(path_delay, 3)) + "\n")
    target.write("----------------------------------------------------\n")
    target.write("Data Arrival Time\t\t\t" + str(round(path_delay, 3)) + "\n")
    target.close()

def draw_critical_path(critical_path):
    target = open('critical.gv', 'w')
    target.write("digraph G {\n")

    for node in critical_path:
        rt = graph.get_node(int(node)).required
        at = graph.get_node(int(node)).arrival
        slack = graph.get_node(int(node)).slack
        name = graph.get_node(int(node)).name

        target.write(str(name) + ' [label="Name:' + str(start_node) + '\\nRT: ' + str(rt) + '\\nAT: ' + str(
            at) + '\\nSlack: ' + str(slack) + '"];\n')

        for j in graph.adj[node]:
            start = graph.get_node(int(node)).name
            end = graph.get_node(int(j)).name

            target.write(str(start) + ' -> ' + str(end) + ';\n')

    target.write("}")
    target.close()

draw_graph(graph)
generate_report(graph)