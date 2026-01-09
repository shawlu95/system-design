"""
Your goal is to implement a type system for a custom Toy Language. 
This system must handle primitive types, generics, nested tuples, 
and function signatures. You will implement the core data structures 
and a Type Inference engine that substitutes generics with concrete 
types. Type Definitions     
    Primitives: Lowercase strings like int, float, str, bool     
    Generics: Uppercase letters followed by numbers, e.g., T1, T2    
    Tuples: Comma-separated types inside brackets, which can be nested. Example: [int, [T1, str]].     
    
Functions: Defined by a list of parameter types and a single return type. 
Syntax: [param1, param2] -> returnType. 

Part 1: Implement to_str in Node and Function. 
Node Class: Represents a type node. It can be a leaf (primitive/generic) or a tuple (list of child nodes). 

class Node:     
    def __init__(self, node_type):         
        If node_type is a string: It is a primitive or generic.         
        If node_type is a list: It is a tuple containing other Node objects.   

    def to_str(self):         
        Primitives/Generics: Return the string name (e.g., "int").         
        Tuples: Return bracketed, comma-separated types (e.g., "[int,T1]"). 
        
class Function:        
    def __init__(self, parameters, output_type):         
        Represents a function signature.         
        parameters: A List[Node] objects.         
        output_type: A single Node object.     
    
    def to_str(self):         
        Format: (param1,param2,...) -> returnType.         
        Example: (int,T1) -> [T1,str] 
        
Part 2: Implement a function get_return_type(parameters, function) that 
determines the concrete return type of a function based on provided arguments. 

def get_return_type(parameters: List[Node], function: Function) -> Node:     
    pass 
    
Requirements:     
    Generic Resolution: Build a mapping (substitution table) by comparing the Function's 
    expected parameters to the actual parameters provided.     
    
    Substitution: Recursively replace all generics in the function's output_type with 
    the concrete types found during resolution.     
    
    Error Handling:         
    Argument Count Mismatch: Raise an error if the number of arguments doesn't match.         
    Type Mismatch: Raise an error if a concrete type (e.g., int) is expected but a different type (e.g., str) is provided.         
    Generic Conflict: Raise an error if the same generic (e.g., T1) is bound to two different concrete types in the same call. 
    
Test Examples Example 1: 
Basic Substitution     
    Function: [T1, T2, int, T1] -> [T1, T2]     
    Arguments: [int, str, int, int]     
    Logic: T1 maps to int, T2 maps to str.     
    Result: [int, str] 
    
Example 2: Nested Tuples & Complex Generics     
    Function: [[T1, float], T2, T3] -> [T3, T1]     
    Arguments: [[str, float], [int, str], int]     
    Logic: * T1 is extracted from the first tuple as str.         
    T2 maps to the tuple [int, str].         
    T3 maps to int.     
    Result: [int, str] 
    
Example 3: Conflict Error     
    Function: [T1, T1] -> T1     
    Arguments: [int, str]     
    Error: T1 cannot be both int and str.
"""

import re
from typing import List, Dict, Union

_GENERIC_RE = re.compile(r"^[A-Z]+[0-9]+$")  # e.g. T1, T2, AB12


class Node:
    """
    Represents a type node:
      - leaf: primitive or generic  (node_type is a string)
      - tuple: list of child Nodes  (node_type is a list)
    """

    def __init__(self, node_type: Union[str, list, "Node"]):
        if isinstance(node_type, Node):
            # Copy-constructor
            self.name = node_type.name if node_type.is_leaf() else None
            self.children = [Node(ch) for ch in node_type.children] if not node_type.is_leaf() else None
        elif isinstance(node_type, str):
            self.name = node_type
            self.children = None
        elif isinstance(node_type, list):
            self.name = None
            self.children = [Node(x) for x in node_type]
        else:
            raise TypeError("node_type must be a str, list, or Node")

    def is_leaf(self) -> bool:
        return self.children is None

    def is_tuple(self) -> bool:
        return self.children is not None

    def is_generic(self) -> bool:
        return self.is_leaf() and _GENERIC_RE.match(self.name) is not None

    def to_str(self) -> str:
        # Primitives/Generics
        if self.is_leaf():
            return self.name
        # Tuples (possibly nested)
        return "[" + ",".join(child.to_str() for child in self.children) + "]"

    def copy(self) -> "Node":
        return Node(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False
        if self.is_leaf() != other.is_leaf():
            return False
        if self.is_leaf():
            return self.name == other.name
        return self.children == other.children

    def substitute(self, mapping: Dict[str, "Node"]) -> "Node":
        """
        Recursively replace generics using the mapping.
        Returns a NEW Node (no mutation).
        """
        if self.is_leaf():
            if self.is_generic() and self.name in mapping:
                return mapping[self.name].copy()
            return self.copy()
        return Node([child.substitute(mapping) for child in self.children])


class Function:
    """
    Represents a function signature:
      parameters: List[Node]
      output_type: Node
    """

    def __init__(self, parameters: List[Node], output_type: Node):
        self.parameters = [Node(p) for p in parameters]
        self.output_type = Node(output_type)

    def to_str(self) -> str:
        return "(" + ",".join(p.to_str() for p in self.parameters) + ") -> " + self.output_type.to_str()


def _unify(expected: Node, actual: Node, subst: Dict[str, Node]) -> None:
    """
    Compare expected vs actual, building subst for generics.
    Raises on mismatches/conflicts.
    """
    # Leaf expected: primitive/generic
    if expected.is_leaf():
        if expected.is_generic():
            g = expected.name
            if g in subst:
                if subst[g] != actual:
                    raise TypeError(
                        f"Generic conflict: {g} cannot be both {subst[g].to_str()} and {actual.to_str()}"
                    )
            else:
                subst[g] = actual.copy()
            return

        # Primitive (or any concrete leaf)
        if actual.is_leaf() and expected.name == actual.name:
            return
        raise TypeError(f"Type mismatch: expected {expected.to_str()}, got {actual.to_str()}")

    # Tuple expected
    if not actual.is_tuple():
        raise TypeError(f"Type mismatch: expected {expected.to_str()}, got {actual.to_str()}")
    if len(expected.children) != len(actual.children):
        raise TypeError(f"Tuple arity mismatch: expected {expected.to_str()}, got {actual.to_str()}")

    for e_child, a_child in zip(expected.children, actual.children):
        _unify(e_child, a_child, subst)


def get_return_type(parameters: List[Node], function: Function) -> Node:
    """
    Determines the concrete return type for a call with given argument types.
    Steps:
      1) Build generic substitution table by unifying function.parameters with parameters
      2) Substitute into function.output_type
    """
    args = [Node(p) for p in parameters]

    # Error: argument count mismatch
    if len(args) != len(function.parameters):
        raise ValueError(f"Argument count mismatch: expected {len(function.parameters)}, got {len(args)}")

    subst: Dict[str, Node] = {}
    for expected, actual in zip(function.parameters, args):
        _unify(expected, actual, subst)

    return function.output_type.substitute(subst)


# -------------------------
# Quick examples (from prompt)
# -------------------------
if __name__ == "__main__":
    # Example 1
    f1 = Function(["T1", "T2", "int", "T1"], ["T1", "T2"])
    args1 = ["int", "str", "int", "int"]
    print(f1.to_str(), "=>", get_return_type(args1, f1).to_str())  # [int,str]

    # Example 2
    f2 = Function([["T1", "float"], "T2", "T3"], ["T3", "T1"])
    args2 = [["str", "float"], ["int", "str"], "int"]
    print(f2.to_str(), "=>", get_return_type(args2, f2).to_str())  # [int,str]

    # Example 3 (conflict)
    f3 = Function(["T1", "T1"], "T1")
    try:
        get_return_type(["int", "str"], f3)
    except Exception as e:
        print("Error:", e)
