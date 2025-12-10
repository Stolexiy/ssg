from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("no tag")
        if not self.children:
            raise ValueError("no children")
        attr = self.props_to_html()
        attr = " " + attr if attr else ""
        content = "".join(map(lambda ch: ch.to_html(), self.children))
        return f"<{self.tag}{attr}>{content}</{self.tag}>"
