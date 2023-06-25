---
title: Nei Saitou Neighbor Joining
description: one of my homework that requires me to implement Nei-Saitou Neighbor Joining algorithm to construct phylogenetic tree, as well as evaluating the bootstrap cconfidence.
tags: ["Bioinformatics", "Algorithm"]
date: 2019-04-03T11:15:00+08:00
featured: false
draft: false
---

{{< katex >}}

## 1. Background

Before diving into code, the description of NJ algorithm can be found in ![This Link](https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/1605172209524.png), where first column indicates parent node, and second column is its children node, the last column is the value of edge.

## 2. Neighbor Joining Algorithm

The Neighbor-joining Algorithm Given a distance matrix d compute an uprooted tree topology complete with edge lengths that tries to preserve the additive property: $d\_{i,m} + d\_{j,m} − d\_{i,j} = 2d\_{k,m}$ where $k$ is the k-th node on both routes from $i$ and $j$ to $m$.

1.  Let the set of clusters be called $L$ and initially $i → C_i; ∀i$ that is $| C_i | = 1$ and $L = C_1 , C_2 , . . . C_N$.
2.  $d\_{i,j}$ is the distance from the initial distance matrix.
3.  Compute “normalized distance matrix” $D\_{i,j}$ for all $i, j$ such that
    $$D\_{i,j} = d\_{i,j} − (r_i + r_j ) \\ where\\ r_i = \\frac{1}{|L|-2} \\sum\_{z \\in L} d\_{i,z}$$
    This subtracts the average distance to all other nodes than the pair involved. **Note: this is not where we use the distance identity.**
4.  Use normalized distance to $(i, j) = argmin D\_{i,j}; C_i,C_j \\in L$
5.  Merge $C_i ∪ C_j → C_k$ where $k$ is a new cluster number.
6.  Mark old clusters as used so that effectively: $L ← L − C_i − C_j$
7.  Compute a new normalized distance matrix including the new cluster $k$ and excluding $i, j$.
    $$d\_{k,z} = d\_{z,k} = (d\_{i,z} + d\_{j,,z} − d\_{i,j} ) for all z ∈ L 2$$
    This uses the additivity of the distances to compute the distance to the new cluster from each other node.
8.  Compute the length of the edges from $k$ to $i$ and $j$. Even though $C_k$has assumed the role of both $C_i$ and $C_j$ you still need the edge length to $i$ and $j$ from $k$ in order to “draw” the tree.
    $$edge\_{i,k} = (d\_{i,j} + r_i − r_j)$$
    $$edge\_{j,k} = (d\_{i,j} + r_j − r_i)$$
9.  Define height $h_k = d\_{i,j} /2$ where $h_k$ is the height of node that is the ancestor to all in $C_k$. When drawing the tree $h_k$ is the height above the baseline (where all the leaves are).
10. $L ← L ∪ C_k$
11. While there is more than two clusters left go to step 3
12. Finally, join the remaining two clusters with:
    $$edge\_{j,k} = d\_{i,j} $$

**Implementation Notes Consider this part of the computation:**
$$D\_{i,j} = d\_{i,j} − (r_i + r_j ) \\ where \\ r_i =  \\frac{1}{|L|-2} \\sum\_{z \\in L}d\_{i,z}$$
The values of r*z can be computed once each time we want to compute matrix $D$.
This saves a vast amount of time.
Furthermore, since $D*{i,j}$ is only used to find the argmin of $D\_{i,j}$ we actually don’t have to save array $D$; we only need to find the argmin of it.
So computing all the r and then combine the argmin step with the computation of $D\_{i,j}$

## 3. Implementation

I write code contained comments, and it is about 1000 lines that consumes me two whole days.
Now let me show my code with rich comments. If you have any questions or recommendation, I am very glad to communicate with you! Please feel free to reach me.

```python
# -*- coding: UTF-8 -*-
# Time 20201109
"""
This code integrate bootstrap, getting edge_file and tree_file

USAGE: python -i fa_file -d out_distance_matrix -e out_edge -t out_tree -b number_bootstrap
"""
# import needed library
import argparse
import logging
import random
import time
from collections import defaultdict, namedtuple

import pandas as pd


class Timer:
    """[construct  Timer to show working time of tasks]"""

    def __init__(self, func=time.perf_counter):
        """[init values]

        Args:
            func : Defaults to time.perf_counter.
        """
        self.elapsed = 0.0

        self._func = func

        self._start = None

    def start(self):
        """[start a task]

        Raises:
            RuntimeError:[if task has started then raise error]
        """

        if self._start is not None:
            raise RuntimeError("Already started")

        self._start = self._func()

    def stop(self):
        """[end a task]

        Raises:
            RuntimeError[if task has not started then raise error]
        """
        if self._start is None:
            raise RuntimeError("Not started")

        end = self._func()

        self.elapsed += end - self._start

        self._start = None

    def reset(self):
        """[reset the working time]"""
        self.elapsed = 0

    def running(self):
        """[check if task is running]

        Returns:
            bool
        """

        return self._start is not None

    def __enter__(self):
        """[function used to address 'with text']"""

        self.start()

        return self

    def __exit__(self, *args):
        """[function used to address 'with text']"""

        self.stop()


class TreeNode:
    """[class of tree node]"""

    def __init__(self, key=None):
        """[init values of tree node]

        Args:
            key ([str, float], optional): [node_label, edge]. Defaults to None.

            self.index: node_index
        """
        self.left, self.right = None, None

        self.key = key

        self.parent, self.index = None, None

        self.LIST = []

    def insert_left_children(self, left_object):
        """[insert left children]

        Args:
            left_object ([str, float]): [node_label, edge]
        """
        # create a new node
        temp = TreeNode(left_object)
        # if left children exist
        if self.left:

            temp.left = self.left

            self.left = temp
        # if left children does not exist
        else:
            self.left = temp

    def insert_right_children(self, right_object):
        """[insert right children]

        Args:
            right_object ([str, float]): [node_label, edge]
        """
        # create a new node
        temp = TreeNode(right_object)
        # if right children exist
        if self.right:

            temp.right = self.right

            self.right = temp
        # if right children does not exist
        else:
            self.right = temp

    def isRoot(self):
        """[check if the node is Root node]

        Returns:
            [bool]: [if node is Root return True]
        """

        handle = False

        if self.key[0] == "root":

            handle = True

        return handle

    def isLeaf(self):
        """check if the node is Leaf node

        Returns:
            bool: if the node is Leaf return True
        """

        handle = False

        if not self.left and not self.right:

            handle = True

        return handle

    def catch_leaf(self):
        """show the partition list of leafs below the node, and mainly used to debug

        Returns:
            list: a list contained all leaf below the node
        """

        LIST = []

        # check if the node is leaf
        if self.isLeaf():

            LIST.append(self.index)

        if self.left:

            LIST.extend(self.left.catch_leaf())

        if self.right:

            LIST.extend(self.right.catch_leaf())

        return LIST

    def postorder(self):
        """[tree traversal with postorder, and mainly used to debug]"""
        if self.left:

            self.left.postorder()

        if self.right:

            self.right.postorder()

        print(self.key)


def get_parser() -> dict:
    """[function used to parse parameters from command line and set log]

    Returns:
        [dict]: [return a dict stored parameters]
    """
    # set logging
    logging.basicConfig(
        level=logging.DEBUG, format="%(levelname)s:%(asctime)s:%(message)s"
    )

    # set parser
    parser = argparse.ArgumentParser(
        prog="PROG",
        description="Program designed to condcut NJ ",
        formatter_class=argparse.MetavarTypeHelpFormatter,
    )

    # add parameter for input of fa file
    parser.add_argument(
        "-i", "--input", help="The input file (fasta format)", required=True, type=str
    )

    # add parameter for output of edge file
    parser.add_argument(
        "-e",
        "--edge",
        help="The output file of edges matrix. Default: edges.txt",
        default="edges.txt",
        type=str,
    )

    # add parameter for output of tree file
    parser.add_argument(
        "-t",
        "--tree",
        help="The output file of newick tree. Default: tree.txt",
        default="tree.txt",
        type=str,
    )

    # add parameter for output of distance matrix
    parser.add_argument(
        "-d",
        "--distance",
        help="The output file of distance matrix. Default: genetic_distance.txt",
        default="genetic_distance.txt",
        type=str,
    )

    # add parameter for number of bootstrap; Default: not conduct bootstrap
    parser.add_argument(
        "-b",
        "--bootstrap",
        help="The number of bootstrap. Result will be stored in 'bootstrap.txt'",
        default=None,
        type=int,
    )

    # get parameters
    args = parser.parse_args()

    return args


##############################################
# CELL FOR GETTING GENETIC DISTANCE MATRIX
##############################################


def read_input(input: str) -> dict:
    """[read input of fa file and return a dict whose value is nametuple stored information]

    Args:
        input (str): [fasta file]

    Returns:
        dict: [seq_label: (seq,index )]
    """
    #  create namedtuple to store information
    seqs, seq = {}, namedtuple("info", ["seq", "index"])

    # open file as a list
    content = open(input).readlines()

    # init index of sequence
    read_index = 1

    # read seq into the dict
    for index, line in enumerate(content):
        # check header
        if line.startswith(">"):

            seqs[line.strip(">\n")] = seq(content[index + 1].strip(), read_index)
            read_index += 1

    return seqs


def genetic_distance(seq1: str, seq2: str) -> float:
    """[calculate genetic distance of seq1 and seqw]

    Args:
        seq1 (str): [sequences of seq1]
        seq2 (str): [sequences of seq2]

    Returns:
        float: [genetic distance]
    """
    # get length of sequences
    length = len(seq1)

    # init mismatch
    mismatch = 0

    # begin to calculate
    for s1, s2 in zip(seq1, seq2):

        if s1 != s2:

            mismatch += 1

    return mismatch / length


def fetch_distance(seq1_index: str, seq2_index: str, matrix: dict) -> float or None:
    """[fetch distance from distance matrix in case comupute pair distance repeatedly]

    Args:
        seq1_index (str): [seq1 label]
        seq2_index (str): [seq2 label]
        matrix (dict): [store distances that is calculated]

    Returns:
        float or None: [if distance has calculated return value otherwise None]
    """
    # init value
    distance = None

    # check if the distance is already calculated
    if (seq1_index, seq2_index) in matrix:

        distance = matrix[(seq1_index, seq2_index)]

    elif (seq2_index, seq1_index) in matrix:

        distance = matrix[(seq2_index, seq1_index)]

    return distance


def get_distance_matrix(seqs: dict, out: str) -> dict:
    """[write distance matrix to file]

    Args:
        seqs (dict): [store information of seqs like {seq_label: (seq:, index:)}]
        out (str): [the name of genetic distance file]

    Returns:
        dict: [{(seq1_label,seq2_label):genetic_distance}]
    """
    # open new file
    out_put = open(out, "w")

    # init dict
    distance_map = {}

    # write header
    header = "\t".join(seqs.keys())
    out_put.write(f"\t{header}\n")

    # begin to calculate distance and write to file
    for seq1_label, seq1_info in seqs.items():
        # init list to store distance of every line
        line = []

        for seq2_label, seq2_info in seqs.items():
            # check if the distance is already computed
            distance = fetch_distance(seq1_label, seq2_label, distance_map)

            if not distance:
                # if not exist then calculate it and store
                distance = genetic_distance(seq1_info.seq, seq2_info.seq)

                distance_map[(seq1_label, seq2_label)] = distance

            line.append(distance)
        # write every line
        line = "\t".join([str(element) for element in line])
        out_put.write(f"{seq1_label}\t{line}\n")

    out_put.close()

    return distance_map


##############################################
#                            NJ ALGORITHM
##############################################


def cacl_sum_distance(taxa: str, leaf_set: set, distance_matrix: dict) -> float:
    """[calculate sum distance of node away from other nodes]

    Args:
        taxa ([str]): [label for one node]
        leaf_set ([set]): [a set store current nodes needed to be merged]
        distance_matrix ([dict]): [{(seq1_label,seq2_label):genetic_distance}]

    Returns:
        [float]: [sum distance of node away from others]
    """
    # init value
    result = 0
    # calculate sum distance
    for other_taxa in leaf_set - set([taxa]):
        # fectch genetic distance
        result += fetch_distance(taxa, other_taxa, distance_matrix)

    return result


def find_qmin(leaf_set: set, distance_matrix: dict) -> dict:
    """[ calculate min q_value and get information]

    Args:
        leaf_set ([set]): [current nodes needed to be merged]
        distance_matrix ([dict]): [dict stored genetic distance of current nodes]

    Returns:
        [dict]:  [value, combination,taxa1_sum, taxa2_sum]
    """
    # init dict
    qmin = {
        "combination": None,  # combination of node for merging
        "q_value": None,  # min Q value
        "taxa1_sum": None,  # sum distance of node away from others
        "taxa2_sum": None,
    }

    # calculate  Q value every combinatin of nodes
    for combination, distance in distance_matrix.items():

        taxa1, taxa2 = combination
        # calculate sum distance of node away from others
        taxa1_sum, taxa2_sum = cacl_sum_distance(
            taxa1, leaf_set, distance_matrix
        ), cacl_sum_distance(taxa2, leaf_set, distance_matrix)
        # get Q value
        value = (len(leaf_set) - 2) * distance - taxa1_sum - taxa2_sum
        # compare Q value
        if not qmin["q_value"]:
            # if Q value does not exist then store related information
            (
                qmin["q_value"],
                qmin["combination"],
                qmin["taxa1_sum"],
                qmin["taxa2_sum"],
            ) = (value, combination, taxa1_sum, taxa2_sum)
        # if Q value exist then compare to choose minimum value
        else:
            if value < qmin["q_value"]:

                (
                    qmin["q_value"],
                    qmin["combination"],
                    qmin["taxa1_sum"],
                    qmin["taxa2_sum"],
                ) = (value, combination, taxa1_sum, taxa2_sum)

    return qmin


def help_nj(leaf_set: set, distance_matrix: dict):
    """[helper function to conduct neighbor joining]

    Args:
        leaf_set ([set]): [current nodes needed to be merged]
        distance_matrix ([dict]): [store pair distance of current nodes]

    Returns:
        TREEDICT: a dict stored node that has been merged in binary tree format
        final_leaf_set: final twos node after finishing NJ
        final_matrix:  genetic distances of final two nodes
    """
    # init dict to store nodes that has been merged in format of Binary Tree
    TREEDICT = {}

    def neighbor_joining(leaf_set: set, distance_matrix: dict):
        """[implementation of neighbors joining]

        Args:
            leaf_set ([set]): [current nodes needed to be merged]
            distance_matrix ([dict]): [store genetic distance of current nodes]
        """
        # get nonlocal value
        nonlocal TREEDICT

        # the rule to end the recursion
        if len(leaf_set) < 3:

            return (leaf_set, distance_matrix)
        # enter recursion
        else:
            # find min Q value
            qmin_info = find_qmin(leaf_set, distance_matrix)
            # get nodes needed to be merged
            taxa1, taxa2 = qmin_info["combination"]
            # edge from taxa1 to new node
            edge_taxa1_node = 0.5 * distance_matrix[qmin_info["combination"]] + (
                qmin_info["taxa1_sum"] - qmin_info["taxa2_sum"]
            ) / (2 * (len(leaf_set) - 2))
            # edge from taxa1 to new node
            edge_taxa2_node = (
                distance_matrix[qmin_info["combination"]] - edge_taxa1_node
            )

            # init dict to update genetic matrix
            matrix = {}
            # create label for new node
            new_node = f"{taxa1}_{taxa2}"
            # calculate distance from new node to other nodes
            for node in leaf_set - set(qmin_info["combination"]):
                # store in new genetic matrix with information of old genetic matrix
                matrix[(new_node, node)] = (
                    fetch_distance(taxa1, node, distance_matrix)
                    + fetch_distance(taxa2, node, distance_matrix)
                    - distance_matrix[(taxa1, taxa2)]
                ) * 0.5

            # store genetic distances of other nodes in new genetic matrix
            for combination, distance in distance_matrix.items():

                if (taxa1 not in combination) and (taxa2 not in combination):

                    matrix[combination] = distance

            # store phylogenetic nodes that has been merged in Binary Tree format
            # create a tree node that linked two merged nodes in Binary Tree

            # if one of merged nodes has been in Binary Tree then add edges
            # taxa1 is always regarded as left children
            if taxa1 in TREEDICT:

                left = TREEDICT.pop(taxa1)
                left.key[1] = edge_taxa1_node

            # if one of merged nodes is not stored in Binary Tree
            else:
                # create a Tree node and store its label and edge
                left = TreeNode([taxa1, edge_taxa1_node])

            # taxa2 is same with taxa1
            # taxa2 is always regarded as right children
            if taxa2 in TREEDICT:

                right = TREEDICT.pop(taxa2)
                right.key[1] = edge_taxa2_node

            else:

                right = TreeNode([taxa2, edge_taxa2_node])

            # create a new_node linked two merged nodes in Binary Tree
            # the new_node has no edge
            internal_node = TreeNode([new_node, None])
            # add paraent information for two merged nodes
            left.parent, right.parent = internal_node, internal_node
            # link two merged nodes as children in Binary Tree
            internal_node.left, internal_node.right = left, right
            # add new node to dict
            TREEDICT[new_node] = internal_node
            # update genetic distance matrix
            distance_matrix = matrix
            # update current phylogenetic nodes needed to be merged
            leaf_set -= set(qmin_info["combination"])
            leaf_set.add(new_node)

            return neighbor_joining(leaf_set, distance_matrix)

    # begin to compute until two phylogenetic nodes left
    final_leaf_set, final_matrix = neighbor_joining(leaf_set, distance_matrix)

    return TREEDICT, final_leaf_set, final_matrix


##############################################
#               PREORDER TREE AND ADD INDEX
##############################################


def my_tree(TREEDICT: dict, final_distance_matrix: dict, seqs: dict):
    """function to create Binary tree but it has fake root
            because phylogenetic node has three children
            hence create a fake node as root to get a Binary Tree
            all following behaviors related Binary Tree usually consider this situation

            for binary_tree.key:

            key[0] -> label ; key[1] -> edge

    Args:
        TREEDICT ([dict]): [store information of binary tree ]
        final_distance_matrix ([dict]): [distance of final two nodes]
        seqs ([dict]): [store information of seqs]

    Returns:
        [binary tree]: [binary tree with fake root]
    """
    # 'merged node' means nodes have been changed as binary tree
    # init value to find if node is 'merged node'  in final two nodes after NJ
    last_node_label = None
    last_node_edges = None

    for index, value in final_distance_matrix.items():

        # get edge
        last_node_edges = value

        # check if node is 'merged node'
        for label in index:
            # if not
            if label in seqs:
                # get label
                last_node_label = label

    # create a fake root with label 'root'
    fake_root = TreeNode(("root", " "))
    # get node label of final two nodes after NJ
    current_node_index = list(TREEDICT.keys())
    # if final two nodes are merged node
    if not last_node_label:

        # add last edge to right children of fake root
        # because the left children of fake root is "TRUE root", which has three childerns
        # the right children of fake root is linked to left children of it in real
        # so the edge indicates the distance between left children and right children
        # even though right children is linked to fake root in binary_tree
        TREEDICT[current_node_index[1]].key[1] = last_node_edges

        # create tree structure
        fake_root.left = TREEDICT[current_node_index[0]]
        fake_root.right = TREEDICT[current_node_index[1]]

    # if one of final two nodes is merged node
    else:

        # set node that is not merged node as tree structure
        right_node = TreeNode([last_node_label, last_node_edges])

        # set one of final two nodes, a merged node, as left children of fake root
        fake_root.left = TREEDICT[current_node_index[0]]

        # add right children
        fake_root.right = right_node

    return fake_root


def help_edge_matrix(tree, seqs: dict, edge_file: str):
    """[help function to do preorder traversal in order to get edge file]

    Args:
        tree ([Binary Tree])
        seqs (dict): [store information about label, seq, and index of seqs]
        edge_file (str): [output of edge]

    Returns:
        [Binary Tree]: [Binary Tree whose internal node has index]
    """
    # init index for internal node
    N = len(seqs) + 1
    # open new file
    EDGE_FILE = open(edge_file, "w")  # changes

    def edge_matrix(tree):
        # get nonlocal value
        nonlocal N
        # preorder tree
        if tree:
            # index of fake root is None
            if tree.isRoot():

                tree.index = None
            # tree.key[0] is label of node
            # if it not in seqs then it is internal node
            elif tree.key[0] not in seqs:
                # set index for internal node
                tree.index = N
                N += 1

            else:
                # get index of leaf node
                tree.index = seqs[tree.key[0]].index
            # write information of parent and children
            # left and right children of fake root have no parent : None
            if tree.parent:

                EDGE_FILE.write(f"{tree.parent.index}\t{tree.index}\t{tree.key[1]}\n")
            edge_matrix(tree.left)
            edge_matrix(tree.right)

    edge_matrix(tree)

    # add the TRUE ROOT and its children
    EDGE_FILE.write(f"{tree.left.index}\t{tree.right.index}\t{tree.right.key[1]}\n")

    EDGE_FILE.close()
    return tree


##############################################
#                         POSTORDER TREE
# WARNING: MUST CONDUCT AFTER PREODER
##############################################


def help_newick_parse(tree, tree_file: str):
    """[help function to do postorder traversal in order to get tree file]

    Args:
        tree ([Binary Tree])
        tree_file (str): [output of tree]
    """
    # open tree file
    TREE_FILE = open(tree_file, "w")
    # get true root label (left children of fake root)
    true_root_label = tree.left.key[0]

    def newick_parse(tree):
        # get nonlocal value
        nonlocal true_root_label
        # postorder tree
        if tree:

            left = newick_parse(tree.left)
            right = newick_parse(tree.right)
            # if node is internal node
            if left and right:
                # check if node is true node
                if tree.key[0] == true_root_label:
                    # not add '( )' so as to have three children finally
                    return f"{left},{right}"
                # check if node is root
                elif tree.isRoot():
                    # add '()' finally
                    return f"({left},{right})"
                # if node is internal node
                else:
                    return f"({left},{right}):{tree.key[1]}"
            # if node is leaf node
            else:
                return f"{tree.key[0]}:{tree.key[1]}"

    newick = newick_parse(tree)

    TREE_FILE.write(f"{newick};")

    TREE_FILE.close()


##############################################
#                         BOOTSTRAP
##############################################


def bootstrap(original_seqs: dict):
    """bootstrap original seqs and return bootstrap sample and bootstrap seqs

    Args:
        original_seqs (dict): original seqs

    Returns:
        tree_root_with_node_index: bootstrap sample whose node has index
        seqs_bootstrap : bootstrap seqs contained information like index, label, and sequences
    """
    # change data structure in order to use pandas:
    #               0 1 2  (column_number)
    # label 1
    # label 2
    # ...
    seqs_pd = {index: list(value.seq) for index, value in original_seqs.items()}
    df = pd.DataFrame(seqs_pd).T

    # using random to resample
    df_bootstrap = df.loc[:, random.choices(range(df.shape[1]), k=df.shape[1])]

    # get bootstrap information
    seqs_bootstrap = original_seqs.copy()
    # change sequences to bootstrap sequences
    for index, value in df_bootstrap.iterrows():
        seqs_bootstrap[index] = seqs_bootstrap[index]._replace(
            seq="".join(value.values)
        )

    # get nodes needed to be coudcted NJ
    leaf_set = set(seqs_bootstrap.keys())
    # calculate genetic_distance for bootstrap samples
    distance_map = {}
    for seq1_label, seq1_info in seqs_bootstrap.items():

        for seq2_label, seq2_info in seqs_bootstrap.items():

            if seq1_label != seq2_label:

                distance = fetch_distance(seq1_label, seq2_label, distance_map)

                if not distance:

                    distance = genetic_distance(seq1_info.seq, seq2_info.seq)

                    distance_map[(seq1_label, seq2_label)] = distance
    # conduct NJ
    TREEDICT, _, final_distance_matrix = help_nj(leaf_set, distance_map)
    # construct binary_tree
    # get edge file for  last bootstrap (NOT USED)
    tree_root = my_tree(TREEDICT, final_distance_matrix, seqs_bootstrap)
    tree_root_with_node_index = help_edge_matrix(
        tree_root, seqs_bootstrap, "last_bootstrap.edge"
    )
    return tree_root_with_node_index, seqs_bootstrap


def help_find_partion(tree) -> dict:
    """function to partition list for internal nodes in a binary tree

    Args:
        tree (binary_tree): [binary_tree with fake root

    Returns:
        dict: node_index: partition list
    """
    # init dict to store index and its partition list
    internal_node_partion = defaultdict(list)

    # postorder traversal to find leafs for every internal node
    def find_partion(tree):

        LIST = []
        # begin
        if tree:

            left = find_partion(tree.left)
            right = find_partion(tree.right)

            if tree.isLeaf():

                LIST.append(tree.index)

            else:
                # flatten list
                LIST.extend([*left, *right])

                internal_node_partion[tree.index].extend(sorted([*left, *right]))

            return LIST

    # change partition list of fake root to true root
    find_partion(tree)
    internal_node_partion[tree.left.index] = internal_node_partion.pop(tree.index)

    return internal_node_partion


def get_bootstrap_value(
    bootstrap_number: int,
    original_seqs: dict,
    original_tree,
    bootstrap_file: str = "bootstrap.txt",
):
    """[function to integrate relation methods to get bootstrap values for original tree]

    Args:
        bootstrap_number (int): [number for bootstrap. default = None]
        original_seqs (dict): [information of original sequences]
        original_tree ([type]): [binary tree of original sequences]
        bootstrap_file (str): [output of bootstrap]
    """
    # init list to store bootstrap value for every internal node
    internal_node_bootstrap_value = [0] * (len(original_seqs) - 2)
    # get partition list of every internal node in original tree
    original_partion_dict = help_find_partion(original_tree)
    # init list to store dict contained bootstrap_partion and its node_index
    bootstrap_partion_list = []
    # begin to bootstrap and consruct binary tree

    for number in range(bootstrap_number):
        logging.info(f"BOOTSTRAP NUMBER : {number+1}")
        bootstrap_tree, _ = bootstrap(original_seqs)
        bootstrap_partion_list.append(help_find_partion(bootstrap_tree))

    # compare partition list to update bootstrap value
    for internal_node_index, partion_conent in original_partion_dict.items():

        for bootstrap_partion in bootstrap_partion_list:

            if partion_conent in bootstrap_partion.values():

                internal_node_bootstrap_value[
                    internal_node_index - len(original_seqs) - 1
                ] += 1
    # change format for the bootstrap values
    result = [f"{value/bootstrap_number}\n" for value in internal_node_bootstrap_value]
    # write to file
    with open(bootstrap_file, "w") as file:
        file.writelines(result)


##############################################
#                                  MAIN
##############################################


def worker(args: dict):
    """[function to integrate all above method to conduct NJ and output tree and edge file]

    Args:
        args ([dict]): [parameters getting from command line]

    Returns:
        tree_root_with_index : binary tree whose node has index
        seq : information of sequences
    """
    # read fa file and parse it
    seqs = read_input(args.input)
    # get labels of sequences
    leaf_set = set(seqs.keys())
    # get pair genetic distance
    distance_matrix = get_distance_matrix(seqs, args.distance)
    # delete distances between same sequences
    distance_matrix = {
        item: value for item, value in distance_matrix.items() if value != 0
    }
    # get TREEDICT and distance of final two nodes
    TREEDICT, _, final_distance_matrix = help_nj(leaf_set, distance_matrix)
    # construct binary tree REMEMBER it has fake root
    # left children of fake root is regarded as true root
    tree_root = my_tree(TREEDICT, final_distance_matrix, seqs)
    # get edge file and add index for every node in binary tree
    tree_root_with_index = help_edge_matrix(tree_root, seqs, args.edge)
    # get tree file REMEMBER it must conduct after getting edge files
    # because it need index of node
    help_newick_parse(tree_root_with_index, args.tree)

    return tree_root_with_index, seqs


def main():
    args = get_parser()

    with Timer() as t:
        logging.info(f"Neighbor Joining begin.......")
        tree_root_with_index, seqs = worker(args)

    logging.info(f"Neighbor Joining  DONE : TIME {t.elapsed:.2f}s\n")

    if args.bootstrap:
        with Timer() as t:
            get_bootstrap_value(args.bootstrap, seqs, tree_root_with_index)
        logging.info(f"BOOTSTRAP IS DONE : TIME {t.elapsed:.2f}s\n")
    else:
        logging.info(f"BOOTSTRAP IS NOT DONE")

    logging.info(f"EDGE_FILE : {args.edge}")
    logging.info(f"TREE_FILE :  {args.tree}")
    logging.info(f"DISTANCE_FILE: {args.distance}")


if __name__ == "__main__":
    main()
```

**Thanks for your reading! Hopefully helpful!**
