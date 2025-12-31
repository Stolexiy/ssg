import re

from samba.dcerpc.dcerpc import empty

from leafnode import LeafNode
from blocknode import BlockType
from parentnode import ParentNode
from src.htmlnode import HTMLNode
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

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    valid_blocks = []
    for block in blocks:
        if block:
            valid_blocks.append(block.strip())
    return valid_blocks

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if re.match("^```[\s\S]+```$", block) is not None:
        return BlockType.CODE

    lines = block.strip().split("\n")
    if len(lines) > 0:
        if lines[0].startswith("> "):
            for line in lines[1:]:
                if not line.startswith("> "):
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE

        if lines[0].startswith("- "):
            for line in lines[1:]:
                if not line.startswith("- "):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST

        if lines[0].startswith("1. "):
            count = 2
            for line in lines[1:]:
                if not line.startswith(f"{count}. "):
                    return BlockType.PARAGRAPH
                count += 1
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(ParentNode("p", text_to_children(block)))
            case BlockType.HEADING:
                h_size = 0
                for chr in block:
                    if chr == '#':
                        h_size += 1
                    if h_size >= 6:
                        break
                children.append(ParentNode(f"h{h_size}", text_to_children(block[h_size + 1:])))
            case BlockType.CODE:
                children.append(ParentNode("pre", [LeafNode("code", block[3:-3].lstrip())]))
            case BlockType.QUOTE:
                children.append(ParentNode("blockquote", text_to_children(block[2:].replace("> ", "<br />"))))
            case BlockType.UNORDERED_LIST:
                items = block.split("\n")
                ul = ParentNode("ul", [])
                for item in items:
                    if item:
                        ul.children.append(HTMLNode("li", None, text_to_children(item.replace("- ", "").strip())))
                children.append(ul)
            case BlockType.ORDERED_LIST:
                lines = block.strip().split("\n")
                ol = ParentNode("ol", [])
                num = 1
                for line in lines:
                    if line.startswith(f"{num}. "):
                        ol.children.append(HTMLNode("li", None, text_to_children(line.replace(f"{num}. ", "").strip())))
                        num += 1
                children.append(ol)

    return ParentNode("div", children)
