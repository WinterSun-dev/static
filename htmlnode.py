class HTMLNode:
    def __init__(self, tag=None, value=None, *children, **props):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}
        print(props)

    def to_html(self):
        raise NotImplemented

    def props_to_html(self):
        return "".join(map(lambda x: f' {x[0]}="{x[1]}"', self.props.items()))

    def __repr__(self):
        return (f"tag={self.tag}, "
                f"value={self.value}, "
                f"children={", ".join(self.children)}, "
                f"props={", ".join(map(lambda x: f'{x[0]}:{x[1]}', self.props.items()))}")


