from graphviz import Digraph
from sys import argv

if len(argv) == 1:
	print('Not enough arguments.')
	exit()
elif len(argv) > 2:
	print('Too many arguments.')
	exit()

project_name = argv[1]
log_file = './tracker/' + project_name + '.txt'
export_path = './flowchart/' + project_name


d = Digraph(project_name, filename=export_path, node_attr={'colorscheme': 'pastel13', 'fillcolor' : '2', 'style': 'filled', 'shape' : 'record'})

filtered_lines = []
fl_index = 0
START = 'START'
END = 'END'
START_SESSION = '---------- START NEW SESSION ----------\n'
END_SESSION = '------------- END SESSION -------------\n'

print('Filtering log file')

with open(log_file) as f:
	for line in f.readlines():
		if line == START_SESSION or line == END_SESSION:
			filtered_lines.append(line)
			fl_index+=1
		else:
			splits = line.split()
			n = len(splits)
			if n >= 2:
				first = splits[0]
				last = splits[n-1]
				last = '.'.join(last.split('::'))
				if first == START:
					filtered_lines.append(last)
					fl_index += 1
					print
				elif first == END:
					if filtered_lines[fl_index-1] != last:
						filtered_lines.append(last)
						fl_index+=1

print('Creating nested clusters and nodes')

def CreateNestedClustersAndNode(d, splits, i, type='normal'):
	if i == len(splits) - 1:
		if type == 'normal':
			d.node('.'.join(splits), label=splits[i])
		elif type == 'start':
			d.node('.'.join(splits), label=splits[i], fillcolor='3')
		elif type == 'end':
			d.node('.'.join(splits), label=splits[i], fillcolor='1')
	else:
		with d.subgraph(name='cluster_'+splits[i]) as s:
			CreateNestedClustersAndNode(s, splits, i+1, type)

unique_lines = list(dict.fromkeys(filtered_lines))
for line in unique_lines:
	splits = line.split('.')
	if line == filtered_lines[0]:
		CreateNestedClustersAndNode(d, splits, 0, 'start')
	elif line == filtered_lines[-1]:
		CreateNestedClustersAndNode(d, splits, 0, 'end')
	else:
		CreateNestedClustersAndNode(d, splits, 0, 'normal')

print('Creating edges')

edge_count = 0
line_prev = filtered_lines[0]
for line_current in filtered_lines[1:]:
	d.edge(line_prev, line_current, label='[' + str(edge_count) + ']')
	line_prev = line_current
	edge_count+=1

print('Generating graph')

try:
	d.render(view=True)
except:
	print('\n\nError: Graphviz unable to generate graph.')
	source_file = project_name + '_dotsource.txt'
	print('Graphviz source file exported to ', source_file)
	with open(source_file, 'w+') as f:
		f.write(d.source)