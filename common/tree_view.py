import types

from mylib.data_tree import tk_tree_view

def recursive_adjustments(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = recursive_adjustments(obj[i])
    elif isinstance(obj, (dict, Tree)):
        for key in list(obj.keys()):
            obj[key] = recursive_adjustments(obj[key])
    else:
        if obj in [1, 0]:
            obj = str(bool(obj))
    return obj


def parse_node(att, obj=None, expand=[]):
    if obj is not None:
        v = getattr(obj, att, None)
        t = getattr(type(obj), att, None)
    else:
        v = att
        t = type(None)

    if isinstance(v, tuple(expand)):
        return {"type": type(v),
                "contents": Tree(v, expand)}

    elif isinstance(t, property):
        return getattr(type(obj), att).__get__(obj, type(obj))

    elif isinstance(v, types.MethodType):
        return None

    elif isinstance(v, (dict, Tree)):
        new_d = {}
        for key, value in v.items():
            if isinstance(value, tuple(expand)):
                new_d[key] = Tree(value, expand)
            else:
                new_d[key] = value
        return new_d
    else:
        return v

class Tree(dict):
    def __init__(self, obj, expand=[]):
        keys = set(dir(type(obj)) + dir(obj))
        for att in sorted(list(keys)):
            node = parse_node(att, obj, expand)
            if node is not None and not att.startswith("__"):
                self.update({att: node})


def tree_view(obj, expand=[]):
    if isinstance(obj, dict):
        _obj = type('dummy', (object,), obj)
    else:
        _obj = obj
    dic = Tree(_obj, expand)
    recursive_adjustments(dic)
    tk_tree_view(dic)

if __name__ == '__main__':
    class Node:
        dic = {"a": 0}

        @property
        def prop_1(self):
            return 1


    class Sample:
        children = {
            "c1": Node(),
            "c2": Node()
        }

    tree_view(Sample(), expand=[Node])
