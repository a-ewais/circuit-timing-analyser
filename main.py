from task_3 import Graph
# import pygraphviz as pgv

graph = Graph('./Gatlevel_Netlists/num_3.json')
cp, time = graph.get_critical_path()
print(cp, time)

print(graph.adj)

# G=pgv.AGraph(strict=False, directed=True)

target = open('graph.gv', 'w')

target.write("diagraph G {\n")

for node,arr in graph.adj.items():
    if graph.types[int(node)] != 'output' and graph.types[int(node)] != 'start':
        rt = graph.get_node(int(node)).required
        at = graph.get_node(int(node)).delay
        slack = graph.get_node(int(node)).slack
    else:
        rt = graph.timing_constraints['clock_period'] - graph.timing_constraints['output_delay']
        at = 0
        slack = 0
    start_node = 'start'

    if graph.types[int(node)] != 'output' and graph.types[int(node)] != 'start':
        start_node = graph.get_node(int(node)).name

    target.write(str(start_node) + ' [label="Name:' + str(start_node) + '\\nRT: ' + str(rt) + '\\nAT: ' + str(at) + '\\nSlack: ' + str(slack) + '"]\n')
    for i in arr:
        start = 'start'
        end = 'output'
        if graph.types[int(node)] != 'start':
            start = graph.get_node(int(node)).name

        if graph.types[int(i)] != 'output':
            end = graph.get_node(int(i)).name
        target.write(str(start) + ' -> ' + str(end) + '\n')