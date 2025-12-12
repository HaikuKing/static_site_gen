class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
        # plain text node
            if self.value is None:
                return ""
            else:
                return self.value

        # build opening tag (with optional props)
        if self.props:
            props = self.props_to_html()
        else:
            props = ""
        
        # if we have children, render them and ignore self.value
        if self.children is not None:
            inner_html = "".join(child.to_html() for child in self.children)
            return f"<{self.tag}{props}>{inner_html}</{self.tag}>"

        # leaf node: just value
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
    
    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for prop in self.props:
            result += f' {prop}="{self.props[prop]}"'
        return result

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value)
        self.props = props
    
    def to_html(self):
        if self.value is None:
            raise ValueError("leaf nodes must have a value")
        elif self.tag is None:
            return f"{self.value}"
        elif self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("parent node must have tag")
        if self.children is None:
            raise ValueError("parent node must have children")
        else:
            result = f'<{self.tag}{self.props_to_html()}>'
            for child in self.children:
                result += f'{child.to_html()}'
            result += f'</{self.tag}>'
            return result
