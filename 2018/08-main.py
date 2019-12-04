#!/usr/bin/env python3

data = None

with open('./08-data.txt') as f:
    data = [int(x) for x in f.read().split()]

def part1(data):
    md_counts  = []
    child_counts = []
    msum = 0
    i = 0
    while i < len(data):
        c_count = data[i]
        i += 1
        md_count = data[i]
        i += 1

        while c_count == 0:
            mdend = i + md_count
            while i < mdend:
                msum += data[i]
                i += 1
            if len(child_counts) > 0:
                c_count = child_counts.pop() - 1
                md_count = md_counts.pop()
            else:
                break

        child_counts.append(c_count)
        md_counts.append(md_count)

    print('metadatas:', msum)


def nodename(i):
    return f'0000000{hex(i)}'[-6:]
    
def part2(data):
    nodeidx = 0
    debug = False
    children_remaining = [1]
    child_values = [[]]
    child_count = []
    md_count = []
    i = 0
    node = []
    while i < len(data):
        if debug:
            print('-------------------------------------------------------------------')
            print(f'node: {node}')
            print(f'child values: {child_values}')
            print(f'children remaining: {children_remaining}')
            print(f'md counts: {md_count}\n')

        if children_remaining[-1] > 0: # we are processing a new child
            cc = data[i]
            mc = data[i+1]
            nn = nodename(nodeidx)
            if debug: print(f'NEW node[{nn}] | {cc} children | {mc} metadatas | raw: {data[i:]}')
            node.append(nn)
            nodeidx += 1
            child_count.append(cc)
            children_remaining.append(cc)

            md_count.append(mc)
            
            child_values.append([])
            
            i += 2
            continue

        # we are not processing a new child, determine how to handle metadata
        if debug: print(f'node [{node[-1]}]: processing metadata')
        
        cc = child_count.pop()
        mc = md_count.pop()
        cv = child_values.pop()
        node.pop()

        children_remaining.pop()

        # tell parent that it has one less child to process
        children_remaining[-1] -= 1
        v = 0
        if cc == 0: # processing metadata for a node with 0 children
            # remove my metadata count, child values list, child count, and child remaining count
            if debug: print(f' - for a childless node')

            # value is sum of metadata
            
            while mc > 0:
                v += data[i]
                if debug: print(f'     + {data[i]}')
                mc -= 1
                i += 1
            if debug: print(f' - next: {data[i:]}')
            
            

        else: # processing metadata for a node with children
            if debug: print(f' - for a parent node')
            while mc > 0:
                cid = data[i] - 1
                i += 1
                mc -= 1
                if cid < len(cv):
                    if debug: print(f'     + {cv[cid]}')
                    v += cv[cid]
                else:
                    if debug: print(f'     ! out of bounds')

        # store my value in parent's child values list
        child_values[-1].append(v)

    print(f'root value: {child_values[0]}')
    
# part1(data[:])
part2(data[:])