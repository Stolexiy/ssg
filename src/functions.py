from leafnode import LeafNode
from textnode import TextType, TextNode

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
