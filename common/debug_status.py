def view(creature):
    import types
    from mylib.data_tree import tk_tree_view

    dic = {}
    dic_keys = dir(creature)
    for att in dic_keys:
        if isinstance(getattr(creature, att), types.FunctionType):
            continue
        elif att[-2:] == "__":
            continue
        elif isinstance(getattr(type(creature), att, None), property):
            dic[att] = getattr(
                type(creature), att).__get__(creature, type(creature))
        else:
            dic[att] = getattr(creature, att, None)

    tk_tree_view(dic)
