from task_3 import Graph

graph = Graph('./Gatlevel_Netlists/num_2.json')
cp, time = graph.get_critical_path()
print(cp, time)
skews = graph.get_skews()
print(skews)
constraints = graph.get_constraints()
print(constraints)
