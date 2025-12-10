from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("no tag")
        if not self.tag:
            return self.value
        attr = self.props_to_html()
        attr = " " + attr if attr else ""
        return f"<{self.tag}{attr}>{self.value}</{self.tag}>"
