#!/usr/bin/env python3

data = None

with open('./06-data.txt') as f:
    data = [x.split(')') for x in f.read().splitlines()]

class Node(object):
    def __init__(self, id, parent_id=None):
        self.id = id
        self.parent_id = parent_id
        self.parent = None
        self.children = []
    
    def create_child(self, cid):
        cn = next((x for x in self.children if x.id == cid), None)
        if cn is None:
            cn = Node(cid, parent_id=self.id)
            cn.parent = self
            self.children.append(cn)
        return cn

    def set_parent(self, parent):
        self.parent = parent
        return self

    def add_children(self, children):
        self.children += children
        

def find_node(id, root):
    to_check = [root]
    while len(to_check) > 0:
        n = to_check.pop(0)
        if n.id == id:
            return n
        to_check += n.children
    return None

def build_tree(d):
    # create all nodes first
    nodes = [Node(orbiter, center) for center,orbiter in d]
    root = Node('COM')
    check = [root]
    while len(check) > 0:
        n = check.pop(0)
        children = [x.set_parent(n) for x in nodes if x.parent_id == n.id]
        n.add_children(children)
        check += children

    return root

def find_leaves(root):
    leaves = []
    to_check = [root]
    while len(to_check) > 0:
        n = to_check.pop(0)
        if len(n.children) == 0:
            leaves.append(n)
        else:
            to_check += n.children
    return leaves

def compute_checksum(root):
    nodes = find_leaves(root)
    val = 0
    checked = []
    while len(nodes) > 0:
        n = nodes.pop(0)
        while n.parent is not None:
            val += 1
            checked.append(n.id)
            n = n.parent
            if n is not None and n.id not in checked:
                nodes.append(n)
    return val

def get_lineage(n):
    lin = []
    while n.parent is not None:
        n = n.parent
        lin.append(n.id)
    return lin

def get_orbital_transfer_count(root):
    me = find_node('YOU', root)
    san = find_node('SAN', root)
    my_lineage = get_lineage(me)
    san_lineage = get_lineage(san)[::-1]
    # print(f'my {my_lineage}')
    # print(f'san: {san_lineage}')
    c = 0
    for i in my_lineage:
        if i in san_lineage:
            while san_lineage[0] != i:
                san_lineage.pop(0)
            return c + len(san_lineage) - 1
        else:
            c += 1
    return 0

root = build_tree(data[:])
# s = compute_checksum(root)
# print(f'checksum = {s}')

c = get_orbital_transfer_count(root)
print(f'transfers = {c}')

