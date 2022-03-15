import sys
import importlib
import inspect
import ast
import textwrap
import difflib


class rename_all(ast.NodeTransformer):

    def visit_Name(self, node):
        node.id = '_'
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        node.name = '_'
        self.generic_visit(node)
        return node

    def visit_arg(self, node):
        node.arg = '_'
        self.generic_visit(node)
        return node
 
    def visit_Attribute(self, node):
        #node.value = '_'
        node.attr = '_'
        self.generic_visit(node)
        return node

def inspect_classes(module_name: str, module, data: dict):
    for class_key, class_value in inspect.getmembers(module, inspect.isclass):
        for method_key, method_value in inspect.getmembers(class_value, inspect.isfunction):
            data[module_name + '.' + class_key + '.' + method_key] = method_value

        for subcls_key, subcls_value in inspect.getmembers(class_value, inspect.isclass):
            if not subcls_key.startswith('_'):
                inspect_classes(module_name, subcls_value, data)

    for key, value in inspect.getmembers(module, inspect.isfunction):
        data[module_name + '.' + key] = value


data = dict()
first = sys.argv[1]
first_module = importlib.import_module(first)
inspect_classes(first, first_module, data)


second_module = None
if len(sys.argv) == 3:
    second = sys.argv[2]
    second_module = importlib.import_module(second)
    inspect_classes(second, second_module, data)

for key in data.keys():
    txt = textwrap.dedent(inspect.getsource(data[key]))
    T = ast.parse(txt)
    new_code = ast.unparse(rename_all().visit(T))
    data[key] = new_code

keys = list(data.keys())
sorted_list = []

for i in range(len(keys)):
    for key2 in keys[i+1:]:
        #print(keys[i], key2, difflib.SequenceMatcher(None, data[keys[i]], data[key2]).ratio())
        if keys[i].split('.')[0] == key2.split('.')[0] and difflib.SequenceMatcher(None, data[keys[i]], data[key2]).ratio() > 0.95\
        or keys[i].split('.')[0] != key2.split('.')[0] and difflib.SequenceMatcher(None, data[keys[i]], data[key2]).ratio() == 1:
            sorted_list.append((keys[i], key2))

sorted_list.sort(key=lambda x: x[0])
for val1, val2 in sorted_list:
    print(val1, val2)

