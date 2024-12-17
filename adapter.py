"""
@Description :   Calculate the structural similarity for json files from Droidbot
@Author      :   lixiaoming
@Date        :   2024/12/17
@Contact     :   lixiaoming233@icloud.com
"""
import xml.etree.ElementTree as ET
import json
import io


def json2view(json_file: str):

    with open(json_file, 'r') as file:
        data = json.load(file)
    views = data['views']

    return views


def view2tree(views: list):

    root = ET.Element("hierarchy")

    node_dict = {}
    for view in views:
        if view["parent"] == -1:
            new_node = ET.SubElement(root, "node")
        else:
            new_node = ET.SubElement(node_dict[view["parent"]], "node")
        if view["package"]:
            new_node.set("package", view["package"])
        if view["class"]:
            new_node.set("class", view["class"])
        if view["resource_id"]:
            new_node.set("resource_id", view["resource_id"])
        if view["visible"]:
            new_node.set("visible", str(view["visible"]))
        if view["checked"]:
            new_node.set("checked", str(view["checked"]))
        if view["selected"]:
            new_node.set("selected", str(view["selected"]))
        if view["content_description"]:
            new_node.set("content_description", view["content_description"])
        if view["text"]:
            new_node.text = view["text"]
        node_dict[view["temp_id"]] = new_node

    tree = ET.ElementTree(root)
    # with open("output.xml", "wb") as file:
    #     tree.write(file, encoding="utf-8", xml_declaration=True)

    return tree


def json2xml(json_file: str):

    tree = view2tree(json2view(json_file))
    root = tree.getroot()

    return ET.tostring(root, encoding='utf-8')


if __name__ == "__main__":
    print(json2xml("path/to/json"))
