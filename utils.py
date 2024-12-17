"""
@Description :   Calculate the structural similarity for XML files
@Author      :   lixiaoming
@Date        :   2024/12/11
@Contact     :   lixiaoming233@icloud.com
"""
from treelib import Tree
from bs4 import BeautifulSoup
import bs4


class DOMTree:

    def __init__(self, label, attrs):
        self.label = label
        self.attrs = attrs


class XMLParser:

    def __init__(self, xml, features):
        self.dom_id = 1
        self.dom_tree = Tree()
        self.features = features
        self.bs_xml = BeautifulSoup(xml, self.features)

    def get_dom_structure_tree(self):
        for content in self.bs_xml.contents:
            if isinstance(content, bs4.element.Tag):
                self.bs_xml = content
        self.recursive_descendants(self.bs_xml, 1)
        return self.dom_tree

    def recursive_descendants(self, descendants, parent_id):
        if self.dom_id == 1:
            self.dom_tree.create_node(descendants.name, self.dom_id, data=DOMTree(descendants.name, descendants.attrs))
            self.dom_id = self.dom_id + 1
        for child in descendants.contents:
            if isinstance(child, bs4.element.Tag):
                self.dom_tree.create_node(child.name, self.dom_id, parent_id, data=DOMTree(child.name, child.attrs))
                self.dom_id = self.dom_id + 1
                self.recursive_descendants(child, self.dom_id - 1)


class Converter:

    def __init__(self, dom_tree, dimension):
        self.dom_tree = dom_tree
        self.node_info_list = []
        self.dimension = dimension
        self.initial_weight = 1
        self.attenuation_ratio = 0.6
        self.dom_eigenvector = {}.fromkeys(range(0, dimension), 0)

    def get_eigenvector(self):
        for node_id in range(1, self.dom_tree.size() + 1):
            node = self.dom_tree.get_node(node_id)
            node_feature = self.create_feature(node)
            feature_hash = self.feature_hash(node_feature)
            node_weight = self.calculate_weight(node, node_id, feature_hash)
            self.construct_eigenvector(feature_hash, node_weight)
        return self.dom_eigenvector

    @staticmethod
    def create_feature(node):
        node_attr_list = []
        node_feature = node.data.label + '|'
        for attr in node.data.attrs.keys():
            node_attr_list.append(attr + ':' + str(node.data.attrs[attr]))
        node_feature += '|'.join(node_attr_list)
        return node_feature

    @staticmethod
    def feature_hash(node_feature):
        return abs(hash(node_feature)) % (10**8)

    def calculate_weight(self, node, node_id, feature_hash):
        brother_node_count = 0
        depth = self.dom_tree.depth(node)
        for brother_node in self.dom_tree.siblings(node_id):
            brother_node_feature_hash = self.feature_hash(self.create_feature(brother_node))
            if brother_node_feature_hash == feature_hash:
                brother_node_count = brother_node_count + 1
        if brother_node_count:
            node_weight = self.initial_weight * self.attenuation_ratio**depth * self.attenuation_ratio**brother_node_count
        else:
            node_weight = self.initial_weight * self.attenuation_ratio**depth
        return node_weight

    def construct_eigenvector(self, feature_hash, node_weight):
        feature_hash = feature_hash % self.dimension
        self.dom_eigenvector[feature_hash] += node_weight


def calculated_similarity(dom1_eigenvector, dom2_eigenvector, dimension):
    a, b = 0, 0
    for i in range(dimension):
        a += dom1_eigenvector[i] - dom2_eigenvector[i]
        if dom1_eigenvector[i] and dom2_eigenvector[i]:
            b += dom1_eigenvector[i] + dom2_eigenvector[i]
    similarity = abs(a) / b
    return similarity


def get_xml_similarity(xml_doc1, xml_doc2, tol=0.1, dimension=5000, features="xml"):
    hp1 = XMLParser(xml_doc1, features)
    xml_doc1_dom_tree = hp1.get_dom_structure_tree()
    hp2 = XMLParser(xml_doc2, features)
    xml_doc2_dom_tree = hp2.get_dom_structure_tree()
    converter = Converter(xml_doc1_dom_tree, dimension)
    dom1_eigenvector = converter.get_eigenvector()
    converter = Converter(xml_doc2_dom_tree, dimension)
    dom2_eigenvector = converter.get_eigenvector()
    value = calculated_similarity(dom1_eigenvector, dom2_eigenvector, dimension)
    if value > tol:
        return False, value
    else:
        return True, value
