# Below you will find several functions I attempted to invent

## 1. sequential_map
### This functions takes any amount of functions and a container as an input
### It returns a list of values from initial container modified by consequent use of functions from input

def sequential_map(*args):
    def apply(func, container):
        return [func(item) for item in container]
    data = args[-1]
    for func in args[:(len(args)-1)]:
        data = apply(func, data)
    return data

## 2. consensus_filter
### This functions takes any amount of functions (which return True or False) and a container as an input
### It returns a list of values from initial container which are returned with True from functions from input

def consensus_filter(*args):
    data_changed = dict.fromkeys(args[-1], [])
    res = []
    funcs = []
    for func in args[:len(args)-1]:
        funcs += [func]
    def funappl(*args):
        return [func(args[-1]) for func in funcs]
    data = args[-1]
    for el in data:
        elem = el
        data_changed[elem] = funappl(funcs, elem)
    for key in data_changed:
        if False not in data_changed[key]:
            res += [key]
    return res
    
## 3. conditional_reduce
### This functions takes 2 functions (first one returns True or False, second one acts as the reduce function) and a container as an input
### It returns a value received from second function used only on values from initial container which are returned with True from the first function

def conditional_reduce(*args):
    data_true = []
    func1 = args[0]
    func2 = args[1]
    cont = args[2]
    for elem in cont:
        if func1(elem) == True:
            data_true += [elem]
    while len(data_true) > 1:
        data_true[0] = func2(data_true[0], data_true[1])
        data_true.pop(1)
    return data_true

## 4. func_chain
### This functions takes any amount of functions
### It returns a function uniting all given functions by condequent using one after another

def func_chain(*args):
    def reduce_funcs(func1, func2):
        return lambda x: func2(func1(x))
    funcs = [*args]
    print(funcs)
    while len(funcs) > 1:
        funcs[1] = reduce_funcs(funcs[0], funcs[1])
        funcs.pop(0)
    return funcs[0]

## 5. sequential_map_chain
### This functions does the same as the sequential_map function but it uses the func_chain function to unite all given functions consequently
### It returns a list of values from initial container modified by consequent use of functions from input

def sequential_map_chain(*args):
    def apply(func, container):
        return [func(item) for item in container]
    def func_chain(*args):
        def reduce_funcs(func1, func2):
            return lambda x: func2(func1(x))
        funcs = list(*args)
        while len(funcs) > 1:
            funcs[1] = reduce_funcs(funcs[0], funcs[1])
            funcs.pop(0)
        return funcs[0]
    data = args[-1]
    return apply(func_chain(args[:-1]), data)
