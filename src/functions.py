import re

from samba.dcerpc.dcerpc import empty

from leafnode import LeafNode
from textnode import TextType, TextNode


def text_to_textnodes(text):
    if text is None or text == "":
        return []

    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unknown text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text
        delimiter_open = False
        while split_text:
            result = split_text.split(delimiter, 1)
            if len(result) == 2:
                if result[0]:
                    new_nodes.append(TextNode(result[0], text_type if delimiter_open else TextType.TEXT))
                delimiter_open = not delimiter_open
                split_text = result[1]
            else:
                new_nodes.append(TextNode(result[0], TextType.TEXT))
                split_text = ""

        if delimiter_open:
            raise Exception(f"Invalid Markdown syntax for {text_type}, missed closing tag")

    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_by_pattern(old_nodes, extract_markdown_images, "![{}]({})", TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes_by_pattern(old_nodes, extract_markdown_links, "[{}]({})", TextType.LINK)

def split_nodes_by_pattern(old_nodes, splitter, pattern, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text
        parts = splitter(node.text)
        for part in parts:
            delimiter = pattern.format(part[0], part[1])
            result = split_text.split(delimiter, 1)
            if len(result) == 2:
                if result[0]:
                  new_nodes.append(TextNode(result[0], TextType.TEXT))

                new_nodes.append(TextNode(part[0], text_type, part[1]))

                if result[1]:
                  split_text = result[1]
                else:
                    split_text = ""

        if split_text:
            new_nodes.append(TextNode(split_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    pattern = r"\!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)
