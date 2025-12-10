
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        attr = []
        for key in self.props:
            attr.append(f"{key}=\"{self.props[key]}\"")
        return " ".join(attr)

    def __repr__(self):
        return f"{self.__class__}(tag={self.tag},value={self.value},children={self.children},props={self.props_to_html()})"