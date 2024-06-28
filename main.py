# -*- coding: utf-8 -*-
import SplitTree
import HypermetricTree
import Counts_bipartition
import sys
import re
import os
import argparse


'''
python version 3.9.1 
This is the function to parse a tree;
Last modified at 2022.1.20  
write by zhoubiaofeng.
'''


__author__      = "zhoubiaofeng"
__credits__     = "zhoubiaofeng"
__version__     = "1.0"
__email__       = "zzbbf123@163.com"
__date__        = "2022.01.04"

def calculate_bipartition(clade_d, clade_cal, treeSplit):
    for key in treeSplit.keys():
        partition = set(re.sub(r'[();]', '', treeSplit[key][2]).split(","))
        #print(partition)
        for key2 in clade_d.keys():
            if clade_d[key2] == partition:
                clade_cal[key2] += 1
    return clade_cal

def calculate_bipartition_all(tree_f, clade_info):
    #trees  = open(sys.argv[1], 'r').readlines() # trees
    trees = open(tree_f, 'r').readlines()  # trees
    calBi = Counts_bipartition.CountsBipartition("clade_information.txt")
    clade_d, clade_cal = calBi.Counts(
    )  # clade_d : each node composing, clade_cal : node composing counts(init = 0 )
    for tree in trees:
        tree = "".join([i for i in tree.strip().split(" ")])  # remove space
        treeSplit = SplitTree.splitTree(tree)
        clade_cal = calculate_bipartition(clade_d, clade_cal, treeSplit)
    print(clade_cal)

def main():
    parser = argparse.ArgumentParser(description="Parse the ML tree for different uses.")
    parser.add_argument("-i", "--input", action="store", dest="intrees", required= True, help="Name of input tree file that contains a set of trees.")
    parser.add_argument("-o", "--output", action="store", dest="outfilename", required= False, help="Prefix name for output files of all analyses.")
    ### HypermetricTree
    parser.add_argument("-ht", "--HypermetricTree", action="store_true", dest="HyTree", required= False, help="Build HypermetricTree file") # if true, then run
    ### Counts_bipartition
    parser.add_argument("-cb", "--CountBipartition", action="store_true", dest="CountBi", required= False, help="Count assigned bipartition numbers from a set of trees.") # if true, then run 
    parser.add_argument("-c", "--CladeInfo", action="store", dest="CladeInfo", required= False, help="Clade information from assigned tree.") # if true, then run 
    args = parser.parse_args()
    
    if args.CountBi:
        ''' python main.py -i intrees -cb -c clade_information.txt'''
        calculate_bipartition_all(args.intrees, args.CladeInfo)
    elif args.HyTree:
        ''' python main.py -i intrees -ht -o '''
        print("running")
        trees = open(args.intrees, 'r').readlines()
        for etree in trees:
            treeSplit = SplitTree.splitTree(etree)
            ConcatenateHypermetric = HypermetricTree.HypermetricTree(treeSplit, 10)
            HypermetricTrees = ConcatenateHypermetric.scaledEdgeLength_withTeminal()
            if args.outfilename:
                fout = open(args.outfilename + ".trees", 'a')
            else:
                fout = open(os.getcwd() + "/out.trees", 'a')
            fout.write(HypermetricTrees + "\n")
            fout.close()
    else:
        print("error: None execute..")

if __name__ == "__main__":
    main()