import sys
import re

'''
python version 3.9.1 
This is the function to generate a HypermetricTree from a set of ML Trees; 
Last modified at 2022.1.4
write by zhoubiaofeng.
'''

def node_level_cal(level):
    if level == 0:
        print("error , parse tree error.")
    elif level == 2:
        level = 1
    else:
        level = 1 + (level - 1) / 2
    return (level)


def get_singleLabel(l1, l2):
    for l in l1:  # l1 larger
        if l not in l2:
            return l


def nodeParse(treeSplit, max_branch_len):
    k = []
    for key in treeSplit.keys():
        k.append(key)
    k.sort(key=lambda x: len(treeSplit[x][3]),
           reverse=True)  # larger first

    def sublist_check(l1, l2):
        for l in l1:  # l1, smaller
            if l not in l2:  # not in return l1 not the sublist of l2
                return False
        return True  # true means l1 not the subset of l2
    d_comb = {}  # comb list
    n = 1
    for key in k:  # large to small
        # print(key)
        for forward in range(n, len(k), 1):
            # # has single label
            # if (sublist_check(set(treeSplit[k[forward]][3]), set(treeSplit[key][3]))) and (len(treeSplit[k[forward]][3]) + 1) == len(treeSplit[key][3]):
            if set(treeSplit[k[forward]][3]).issubset(
                    set(treeSplit[key][3])) and (
                        len(treeSplit[k[forward]][3]) + 1) == len(
                            treeSplit[key][3]):  # has single label
                #print(treeSplit[key][3])
                single_label = get_singleLabel(treeSplit[key][3],
                                               treeSplit[k[forward]][3])
                if single_label == "":
                    print("error1, teminal label null")
                #print("%s = %s + %s"%(key, k[forward], single_label))
                if key not in d_comb.keys():
                    d_comb[key] = [k[forward], single_label]
                else:
                    print("error2, node contain differ")
            # # without single lable
            # elif (sublist_check(set(treeSplit[k[forward]][3]), set(treeSplit[key][3]))) and (len(treeSplit[k[forward]][3])) == len(treeSplit[key][3]):
            elif (set(treeSplit[k[forward]][3]).issubset(
                    set(treeSplit[key][3]))
                  ):  # forward must be subset of key(larger one )
                for reverse in range(len(k) - 1, n - 1,
                                     -1):  # reverse is smaller first
                    # if not compare_list(treeSplit[k[forward]][3], treeSplit[k[reverse]][3]): # (larger, smaller) true; l1 is the subset of l2
                    if len(
                            set(treeSplit[k[forward]][3])
                            & set(treeSplit[k[reverse]][3])) == 0:
                        m_l_ = treeSplit[k[forward]][3] + treeSplit[
                            k[reverse]][3]
                        m_l_.sort()
                        m_l = list(set(m_l_))
                        m_l.sort(key=m_l_.index)
                        # if set(m_l) < set(treeSplit[key][3]) and ( ( len(m_l) == len(treeSplit[key][3]) ) or ((len(m_l) +1) == len(treeSplit[key][3]) ) ):
                        if set(m_l) == set(treeSplit[key][3]):
                            #print("%s = %s + %s"%(key, k[forward], k[reverse]))
                            if key not in d_comb.keys():
                                d_comb[key] = [
                                    k[forward], k[reverse]
                                ]  # smaller first (terminal branch first )
                            else:
                                if k[forward] in d_comb[key] and k[
                                        reverse] in d_comb[key]:
                                    continue
                                else:
                                    print("error3")
            else:
                continue
        n += 1
    # print(d_comb)  # bipartition comb, [node1 , node2] et.al
    k.sort(key=lambda x: len(treeSplit[x][3]),
           reverse=False)  # smaller to large : judge the level
    for key in k:
        if key not in d_comb.keys():  # Terminal node
            d_comb[key] = treeSplit[key][3].copy(
            )  # add contain labels, .copy()
            d_comb[key][
                0] = d_comb[key][0] + ":1"  # teminal branch length = 1
            d_comb[key][
                1] = d_comb[key][1] + ":1"  # teminal branch length = 1
            d_comb[key].append(1)  # level
            d_comb[key].append(1)  # edge length # chaoduliang
            if len(treeSplit[key][3]) > 2:
                print("this node %s may be pruned, please check ! " % key)
        else:  # not teminal node
            if d_comb[key][0] not in d_comb.keys(
            ) and d_comb[key][1] not in d_comb.keys(
            ):  # node with two Terminal node, useless
                d_comb[key].append(2)
                d_comb[key].append(1)  # edge length 
            elif d_comb[key][0] in d_comb.keys() and d_comb[key][
                    1] not in d_comb.keys():  # level = has value + 1
                # print(d_comb[d_comb[key][0]][2])
                d_comb[key].append(d_comb[d_comb[key][0]][2] + 1)
                d_comb[key].append(1)  # edge length # chaoduliang
                if not d_comb[key][1].startswith(
                        "node"):  # not node, single label
                    d_comb[key][1] = d_comb[key][1] + ":" + str(
                        d_comb[key][2])  # single edge add the level value
            elif d_comb[key][0] not in d_comb.keys(
            ) and d_comb[key][1] in d_comb.keys():  # level = has value + 1
                d_comb[key].append(d_comb[d_comb[key][1]][2] + 1)
                d_comb[key].append(1)  # edge length # chaoduliang
                if not d_comb[key][0].startswith(
                        "node"):  # not node, single label, edge length
                    d_comb[key][0] = d_comb[key][0] + ":" + str(
                        d_comb[key][2])
            else:
                if d_comb[d_comb[key][0]][2] > d_comb[d_comb[key][1]][2]:
                    d_comb[key].append(d_comb[d_comb[key][0]][2] + 1)
                    d_comb[key].append(1)  # edge length # chaoduliang
                    d_comb[d_comb[key][1]][3] = d_comb[key][2] - d_comb[
                        d_comb[key][1]][
                            2]  # change the smaller edge length  : level [key] node - level [subnode]
                else:
                    d_comb[key].append(d_comb[d_comb[key][1]][2] + 1)
                    d_comb[key].append(1)  # edge length # chaoduliang
                    d_comb[d_comb[key][0]][3] = d_comb[key][2] - d_comb[
                        d_comb[key][0]][
                            2]  # change the smaller edge length
    # print(d_comb)     # 
    max_level = max([d_comb[key][2] for key in k])  #
    # print(max_level)
    max_node = [d_comb[key] for key in k if d_comb[key][2] == max_level][0]
    scale = max_branch_len / max_level
    for key in k:
        d_comb[key].append(scale * d_comb[key][3])  # scale the edge length
    # print(d_comb)      # 
    return d_comb, max_node, scale


class HypermetricTree:

    def __init__(self, x, max_branch_len):
        self.treeSplit = x  # define the local variants
        self.max_branch_len = max_branch_len  

    def fixEdgeLength(self):  # use fix edge length  fold to 1
        max_branch_len = self.max_branch_len
        treeSplit = self.treeSplit
        d_comb, max_node, scale = nodeParse(treeSplit, max_branch_len)
        init_seed = ["("] + [max_node[0]] + [","] + [max_node[1]] + [
            "):" + str(max_node[3])
        ]  # resambling , length = :

        def taowa(result):
            #result = init_seed
            has_key = False
            for e in result:
                if e in d_comb.keys():
                    index_e = result.index(e)
                    before = result[:index_e]
                    after = result[index_e + 1:]
                    node_ass = ["("] + [d_comb[e][0]] + [","] + [
                        d_comb[e][1]
                    ] + ["):"] + [d_comb[e][3]]
                    result = before + node_ass + after
                    has_key = True
            if has_key:
                return (taowa(result))  
                # return(result)
            else:
                # print(result)
                #tree_ass = "".join([str(x) for x in result])
                # print(tree_ass)
                return (result)

        #reassembling_t = taowa(init_seed)
        return ("".join([str(x) for x in taowa(init_seed)]) + ";")

    # this function need to deal nodes brlen contain single label, multiple
    def scaledEdgeLength_notTeminal(self):  # use scaled edge len
        # resembling the tree and add scaled branch length
        # ：
        max_branch_len = self.max_branch_len
        treeSplit = self.treeSplit
        d_comb, max_node, scale = nodeParse(treeSplit, max_branch_len)
        init_seed = ["("] + [max_node[0]] + [","] + [max_node[1]] + [
            "):" + str(max_node[3])
        ]  # resambling , length = : max branch length fixed to 1

        def taowa(result):
            #result = init_seed
            has_key = False
            for e in result:
                if e in d_comb.keys():
                    index_e = result.index(e)
                    before = result[:index_e]
                    after = result[index_e + 1:]
                    node_ass = ["("] + [d_comb[e][0]] + [","] + [
                        d_comb[e][1]
                    ] + ["):" + str(d_comb[e][3] * scale)]
                    result = before + node_ass + after
                    has_key = True
                else:
                    if not e.startswith("(") and not e.startswith(
                            ",") and not e.startswith(
                                ")") and not e.startswith(
                                    " "):  # this is single lable
                        index_e = result.index(e)
                        # print(result[index_e].split(":")[1])
                        if result[index_e].split(":")[1] != "1":
                            result[result.index(e)] = " " + result[
                                result.index(e)].split(":")[0] + ":" + str(
                                    (float(result[result.index(e)].split(":")
                                           [1]) - 1) * scale + 1
                            )  # here 1 = fixed teminal branch length 1
            # print(result)
            if has_key:
                return (taowa(result)) 
                # return(result)
            else:
                #print(result)
                #tree_ass = "".join([str(x) for x in result])
                # print(tree_ass)
                return (result)

        #reassembling_t = taowa(init_seed)
        return ("".join([str(x) for x in taowa(init_seed)]) + ";")


    def scaledEdgeLength_withTeminal(self
                                     ):  
        # 
        # 
        # print(max_node)
        max_branch_len = self.max_branch_len
        treeSplit = self.treeSplit
        d_comb, max_node, scale = nodeParse(treeSplit, max_branch_len)
        init_seed = ["("] + [max_node[0]] + [","] + [max_node[1]] + [
            "):" + str(max_node[3] * scale)
        ]  # resambling , length = : max branch length fixed to 1

        def taowa(result):
            #result = init_seed
            has_key = False
            for e in result:
                if e in d_comb.keys():
                    index_e = result.index(e)
                    before = result[:index_e]
                    after = result[index_e + 1:]
                    node_ass = ["("] + [d_comb[e][0]] + [","] + [d_comb[e][1]] + ["):" + str(d_comb[e][3] * scale)]
                    result = before + node_ass + after
                    has_key = True
                else:
                    if not e.startswith("(") and not e.startswith(
                            ",") and not e.startswith(
                                ")") and not e.startswith(
                                    " "):  # this is single lable
                        index_e = result.index(e)
                        result[result.index(e)] = " " + result[result.index(
                            e)].split(":")[0] + ":" + str(
                                float(result[result.index(e)].split(":")[1]) *
                                scale
                        )  # here 1 = fixed teminal branch length 1
            # print(result)
            if has_key:
                return (taowa(result))  
                # return(result)
            else:
                # print(result)
                #tree_ass = "".join([str(x) for x in result])
                # print(tree_ass)
                return (result)


        return ("".join([str(x) for x in taowa(init_seed)]) + ";")


