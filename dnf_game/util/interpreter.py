def interpreter(obj, actions):
    # print("\n", "#" * 6, "\n", "called INTERPRETER")
    # print(actions)
    # print("\n", "#" * 6)
    for action in actions:
        if action['type'] == "check":
            check(obj, action)
        elif action['type'] == "action":
            action(obj, action)


def check(_obj, dic):
    """Check a condition and call an action according to it."""
    results = []

    for condition in dic['conditions']:
        obj_string = condition['object']
        obj = _obj
        if obj_string != "self":
            for level in obj_string.split("."):
                obj = getattr(obj, level)
        # print("#" * 6, "\n", condition, "\n", obj, condition['attribute'])
        compared_att = getattr(obj, condition['attribute'], None)
        value = condition['value'][1]
        if condition['value'][0] == "is":
            result = compared_att == value
        elif condition['value'][0] == "not":
            result = compared_att != value
        results.append(result)

    if dic["match"] == "all":
        result = all(results)
    elif dic["match"] == "any":
        result = any(results)
    else:
        raise ValueError("check:match {}".format(dic["match"]))

    action(_obj, *dic[result])


def action(_obj, *dicts):
    """Perform action with args, both specified on dicts."""
    for dic in dicts:
        act = getattr(_obj, dic['action'], None)

        args = dic['args']

        if act is None and dic['action'] in globals():
            act = globals()[dic['action']]
            if isinstance(args, list):
                act(_obj, *args)
            elif isinstance(args, dict):
                act(_obj, **args)
        else:
            if isinstance(args, list):
                act(*args)
            elif isinstance(args, dict):
                act(**args)


def set_attribute(_obj, field, value, op=None):
    """Set the specified field with the given value."""
    if isinstance(value, str) and value.startswith("$"):
        obj = _obj
        obj_string = value[1:]
        for level in obj_string.split("."):
            obj = getattr(obj, level)
        # print("parsed $ value: ", value, obj)
        value = obj

    if op is None:
        setattr(_obj, field, value)
    elif op is "-":
        setattr(_obj, field, -value)
    else:
        raise ValueError("set_attribute:'op' () not valid".format(op))
