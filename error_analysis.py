# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
This script computes smatch score between two AMRs.
For detailed description of smatch, see http://www.isi.edu/natural-language/amr/smatch-13.pdf
"""
import sys
DEBUG_LOG = sys.stderr
ERROR_LOG = sys.stderr

# file2 is fold
def error_match(mapping , instance1,attribute1,relation1,instance2,attribute2,relation2, prefix1, prefix2):
    """ 
    instance : correct, extra, missing
    attribute : correct, other_wrong_attribute(no correspoding node),
    wrong_attribute_type, missing_attribute
    relation : correct, other_wrong_relation(no responding node),
    wrong_relation_type, missing_relation
    """
    # anlysis the error between amr1 amr2, amr2 is golden
    correct_instance = []
    extra_instance = []
    missing_instance = instance2[:]
    for i, m in enumerate(mapping):
        if m == -1:
            extra_instance.append(instance1[i])
        else:
            correct_instance.append(instance1[i])
            if instance2[m] in missing_instance:
                missing_instance.remove(instance2[m])
    
    print >>ERROR_LOG , "correct_instance[", len(correct_instance), "]:", correct_instance
    print >>ERROR_LOG , "extra_instance[", len(extra_instance), "]:" , extra_instance
    print >>ERROR_LOG , "missing_instance[", len(missing_instance), "]:" , missing_instance
    
    #attribute error 
    correct_attribute = []
    wrong_attribute_type = []
    other_wrong_attribute = []
    missing_attribute = attribute2[:]
    for attr in attribute1:
        nodeindex1 = int(attr[1][len(prefix1):])
        if mapping[nodeindex1] ==-1:
            if attr not in other_wrong_attribute:
                other_wrong_attribute.append(attr)
        else:
            map_node_name = '%s%d'% (prefix2, mapping[nodeindex1])
            node_in_attribute = False
            for goldattr in attribute2:
                if goldattr[1]==map_node_name and goldattr[2]==attr[2]:
                    if goldattr in missing_attribute:
                        missing_attribute.remove(goldattr)
                    if goldattr[0] == attr[0]:
                        correct_attribute.append(attr)
                    else:
                        if (goldattr,attr) not in wrong_attribute_type:
                            wrong_attribute_type.append((goldattr,attr))
                    node_in_attribute = True
                    continue
            if node_in_attribute == False:
                if attr not in other_wrong_attribute:
                    other_wrong_attribute.append(attr)

    print >>ERROR_LOG , "correct_attribute[", len(correct_attribute), "]:", correct_attribute
    print >>ERROR_LOG , "other_wrong_attribute[", len(other_wrong_attribute), "]:" , other_wrong_attribute
    print >>ERROR_LOG , "wrong_attribute_type[", len(wrong_attribute_type), "]:" , wrong_attribute_type
    print >>ERROR_LOG , "missing_attribute[", len(missing_attribute), "]:" , missing_attribute

    #relation error 
    correct_relation = []
    wrong_relation_type = []
    other_wrong_relation = []
    missing_relation = relation2[:]
    for rel in relation1:
        nodeindex1 = int(rel[1][len(prefix1):])
        nodeindex2 = int(rel[2][len(prefix1):])
        if mapping[nodeindex1] ==-1 or mapping[nodeindex2]==-1:
            if rel not in other_wrong_relation:
                other_wrong_relation.append(rel)
        else:
            map_node_name1 = '%s%d'% (prefix2, mapping[nodeindex1])
            map_node_name2 = '%s%d'% (prefix2, mapping[nodeindex2])
            node_in_relation = False
            for goldrel in relation2:
                if goldrel[1]==map_node_name1 and goldrel[2]==map_node_name2:
                    if goldrel in missing_relation:
                        missing_relation.remove(goldrel)
                    if goldrel[0] == rel[0]:
                        correct_relation.append(rel)
                    else:
                        if (goldrel,rel) not in wrong_relation_type:
                            wrong_relation_type.append((goldrel,rel))
                    node_in_relation = True
                    continue
            if node_in_relation == False:
                if attr not in other_wrong_relation:
                    other_wrong_relation.append(rel)
    print >>ERROR_LOG , "correct_relation[", len(correct_relation), "]:", correct_relation
    print >>ERROR_LOG , "other_wrong_relation[", len(other_wrong_relation), "]:" , other_wrong_relation
    print >>ERROR_LOG , "wrong_relation_type[", len(wrong_relation_type), "]:" , wrong_relation_type
    print >>ERROR_LOG , "missing_relation[", len(missing_relation), "]:" , missing_relation
    return missing_instance,extra_instance,wrong_attribute_type,other_wrong_attribute,missing_attribute,wrong_relation_type,other_wrong_relation,missing_relation 

