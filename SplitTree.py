import sys
import re

'''
python version 3.9.1 
This is the function to split a tree into bipartitions;
Last modified at 2022.1.4
write by zhoubiaofeng.
'''

def splitTree(tree):
    left = [each.start() for each in re.finditer('\(', tree)]  # left
    right = [each.start() for each in re.finditer('\)', tree)]  # left
    edge_number = 0

    if len(left) != len(right):
        print("Tree file format error, please check!")
    else:
        #
        #inter_node = [ each.start() + 1 for each in re.finditer(',\(', tree) ]
        #teminal_node = [ each.start() + 1 for each in re.finditer(',[A-Za-z0-9_]', tree) ]
        #node_list= inter_node + teminal_node
        # split using ","
        node_list = [each.start() for each in re.finditer(',', tree)]
        node_list.sort()
    # print(node_list)

    treeSplit = {}
    #treeSplit["node0"] = tree
    node_n = 1
    for node in node_list:
        left_branch = tree[0: node]
        right_branch = tree[node + 1: len(tree)]
        left_string = ""
        right_string = ""
        # print(left_branch)
        # print(right_branch)
        break_check = False
        # 
        for n in range(len(left_branch) - 1, 0, -1):
            # only terminal branch
            if (left_branch[n:len(left_branch)].count("(") == 1) and (left_branch[n:len(left_branch)].count(")") == 0):
                left_string = left_branch[n:len(left_branch)]
                #print("left if 1 out: " +  left_string)
                break_check = True  # 
            # 
            elif left_branch[n:len(left_branch)].count("(") == left_branch[n:len(left_branch)].count(")"):
                # situation : ((1,2),(3,4)) muliti node
                if left_branch[len(left_branch) - 1] == ")":
                    left_string = left_branch[n:len(left_branch)]
                    #print("left if 2 out: " +  left_string)
                    break_check = True
            else:
                continue
            if break_check:
                break

        break_check = False
        # be careful, list[0:0] = null, so start with 1
        for n in range(1, len(right_branch), 1):
            if right_branch[0] == "(":  # muliti node
                # 
                if right_branch[:n].count(")") == right_branch[:n].count("("):
                    # be careful, list[0:0] = null
                    right_string = right_branch[:n]
                    #print("right if 2 out: " +  right_branch[:n] + " " + str(n))
                    break_check = True
            else:
                # this is terminal branch
                if (right_branch[:n].count(")") == 1) and (right_branch[:n].count("(") == 0):
                    right_string = right_branch[:n - 1]
                    #print("right if 1 out: " +  right_string+ " " + str(n))
                    break_check = True  # 
            if break_check:
                break

        node_string = "(" + left_string + "," + right_string + ")"
        label = [x for x in re.split("[,()]", node_string) if x != ""]
        # bipartion 1, bipartition 2, node newick, contain labels
        treeSplit["node" + str(node_n)] = [left_string,
                                           right_string, node_string, label]
        node_n += 1
    # print(treeSplit)

    fout = open("bipartition.txt", 'w')
    for key in treeSplit.keys():
        #fout.write(key + ":" + ",".join(treeSplit[key][3]) + "\n")
        fout.write(key + ":" + treeSplit[key][2] + "\n")
    fout.close()

    fout = open("bipartition2.txt", 'w')
    for key in treeSplit.keys():
        #fout.write(key + ":" + ",".join(treeSplit[key][3]) + "\n")
        if treeSplit[key][0] == "" or treeSplit[key][1] == "":
            # print(key)
            continue
        else:
            fout.write(key + ":" + treeSplit[key]
                       [0] + "\t" + treeSplit[key][1] + "\n")
    fout.close()

    return treeSplit
