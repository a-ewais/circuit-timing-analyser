from task_3 import Graph

graph = Graph('./Gatlevel_Netlists/num_9.json')
cp, time = graph.get_critical_path()
print(cp, time)
