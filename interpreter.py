from env import GlobalEnv, LocalEnv

genv = GlobalEnv.empty_env()
result = 0


def eval_tree(tree):
    """ The top level function.
        Args:
            tree (ast.Module): The ast abstract syntax tree- the root is a Module node object. The children are contained in a list.
        Returns:
            integer or float: the result of any value returned by the program, 0 by default.
    """
    global genv
    global result
    # Here, get the list of children nodes. Iterate over that list, calling eval_node on each node.
    genv = GlobalEnv.empty_env()
    result = eval_nodes(tree.body, genv)
    return result


def eval_nodes(node_list, env):
    if len(node_list) == 0:
        return None
    elif len(node_list) == 1:
        return eval_node(node_list[0], env)
    else:
        _, new_env = eval_node(node_list[0], env)
        return eval_nodes(node_list[1:], new_env)


def node_name(node):
    return type(node).__name__


def eval_node(node, env):
    """ Evaluates a Node object in the abstract syntax tree.
        Args:
            node (ast.Node): The node to evaluate.
            env (GlobalEnv | LocalEnv): An environment data type.
        Returns:
            (integer or float, environment): A tuple, where the first element is the result of any
            value computed at this node, and the second value is either a GlobalEnv or LocalEnv object.
    """
    global genv
    global result
    node_type = node_name(node)
    if node_type == 'Expr':
        return eval_node(node.value, env)
    elif node_type == 'Assign':
        return assign(node, env)
    elif node_type == 'BinOp':
        return bin_op(node, env)
    elif node_type == 'FunctionDef':
        return function_def(node, env)
    elif node_type == 'Call':
        return call(node, env)
    elif node_type == 'Return':
        return retrn(node, env)
    elif node_type == 'Name':
        return name(node, env)
    elif node_type == 'Num':
        return node.n, env


def assign(node, env):
    # extract the variable name, evaluate the right hand side, then extend the environment.
    # looks like:
    # {'targets': [<_ast.Name object at 0x021AA910>], 'value': <_ast.Num object at 0x021AA990>}
    var_names = list(map(lambda x: x.id, node.targets))
    value = eval_node(node.value, env)[0]
    values = [value for i in range(0, len(var_names))]
    new_env = env.extend(var_names, values)
    return None, new_env


def bin_op(node, env):
    # get the left and right operands (we use only single operands) and the operator.
    # evaluate the operands and apply the operator. return the number, env.
    # node.value is a binop object that looks like:
    # {'left': <_ast.Num object at 0x021AA9D0>,
    # 'op': <_ast.Add object at 0x0218F030>,
    # 'right': <_ast.Num object at 0x021AAA10>}
    # Add, Sub, Mult, Div, Mod
    ops = {
        "Add": lambda x, y: x + y,
        "Sub": lambda x, y: x - y,
        "Mult": lambda x, y: x * y,
        "Div": lambda x, y: x / y,
        "Mod": lambda x, y: x % y
    }
    return ops[node_name(node.op)](eval_node(node.left, env)[0], eval_node(node.right, env)[0]), env


def function_def(node, env):
    # need the function id (name), args, and body. Extend the environment.
    # you can leave the args wrapped in the ast class and the body and unpack them when the function is called.
    fn_id = node.name
    args = node.args
    body = node.body
    return None, env.extend([fn_id], [(args, body)])


def call(node, env):
    # get any values passed in to the function from the Call object.
    # get the fxn name and look up its parameters, if any, and body from the env.
    # get lists for parameter names and values and extend a LocalEnv with those bindings.
    # evaluate the body in the local env, return the value, env.
    arg_vals = [eval_node(arg, env)[0] for arg in node.args]
    if node_name(node.func) == "Call":
        n_node, _ = call(node.func, env)
        packed_args, fn_body = n_node
    else:
        function_name = node.func.id
        packed_args, fn_body = env.lookup(function_name)
    fn_args = list(map(lambda x: x.arg, packed_args.args))
    fn_env = LocalEnv(None, env, fn_args, arg_vals)
    final_val = eval_nodes(fn_body, fn_env)[0]
    return final_val, env


def retrn(node, env):
    # evaluate the node, return the value, env.
    return eval_node(node.value, env)[0], env


def name(node, env):
    # Name(identifier id)- lookup the value binding in the env
    # return the value, env
    return env.lookup(node.id), env
