from django.shortcuts import render
import re

# Create your views here.
def trace_view(request):
    if request.method == 'POST':
        title = "Not easy"
        trace = request.POST['trace']
        tree = transform(trace)
        print(tree)
        return render(request, 'trace2tree/trace_view.html', { 'title':title, 'tree':tree })
    else:
        title = "Welcome, paste your trace log to gerate a tree."
        tree = ""
        return render(request, 'trace2tree/trace_view.html', { 'title':title, 'tree':tree })

# Nodo class
class Nodo(object):
    # init
    def __init__(self, name="nodo"):
        self.name = name
        self.childs = []
        self.parent = None
        self.need_exit = False

    # add children
    def add_child(self, child):
        assert isinstance(child, Nodo)
        self.childs.append(child)

    # add parent
    def add_parent(self, parent):
        assert isinstance(parent, Nodo)
        self.parent = parent


# parse the trace
def parse_trace(trace): return re.findall("call|exit|fail|redo", trace.lower())

# define n1 as parent if not none and n2 as child
def dive(n1, n2):
    if n1 is None:
        n2.need_exit = True
    else:
        n1.need_exit = True
        n1.add_child(n2)
        n2.add_parent(n1)

# not implemented yet
def rise(n1):
    if n1 is not None:
        n1.need_exit = False

# may be used to get last nodo that need an exit
def get_nodo_need_exit(nodos):
    return list(filter(lambda x: x.need_exit, nodos))[-1]

# nodos list to controll them
nodos = []

# gerate the nodos based in the keyword "call", should be improved soon
def gerate_nodos(keywords):
    c = 0
    nodo_master = None
    nod1 = None
    for key in keywords:
        if (key=="call"):
            nod1 = Nodo(c)
            nodos.append(nod1)
            dive(nodo_master, nod1)
            nodo_master = nod1
            c += 1
        elif (key=="exit"):
            nodo_master = nod1.parent
            nod1 = nodo_master
            rise(nodo_master)
    return nodos[0]

# gerate the tree for the javascript render
def gerate_nodo_tree(nodo):
    tree = {}
    tree['name'] = nodo.name
    if(nodo.parent):
        tree['parent'] = nodo.parent.name
    else:
        tree['parent'] = "Nodo"
    tree['children'] = []
    for child in nodo.childs:
        tree['children'].append(gerate_nodo_tree(child))
    return tree

# call all
def transform(trace):
    return [gerate_nodo_tree(gerate_nodos(parse_trace(trace)))]
