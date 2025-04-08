class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        attr = list(self.props.items())
        result = "".join(map(lambda item: f' {item[0]}="{item[1]}"', attr))
        return result
    
    def __repr__(self):
        return f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf Node value missing")
        if self.tag == None:
            return self.value
        attr = self.props_to_html()
        return f"<{self.tag}{attr}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag needed for Parent Node")
        if self.children == None:
            raise ValueError("Parent Nodes must have children")
        attr = self.props_to_html()
        html_children = ""
        for child in self.children:
            html_child = child.to_html()
            html_children += html_child
        return f"<{self.tag}{attr}>{html_children}</{self.tag}>"