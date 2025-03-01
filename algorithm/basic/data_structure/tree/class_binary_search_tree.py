class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:

    def __init__(self) -> None:
        self.root = None

    def insert(self, value: int) -> None:

        if self.root is None:
            self.root = Node(value)
            return

        def _insert(node: Node, value: int) -> Node:
            if node is None:
                return Node(value)

            if value < node.value:
                node.left = _insert(node.left, value)
            else:
                node.right = _insert(node.right, value)
            return node

        _insert(self.root, value)

    def inorder(self) -> None:
        def _inorder(node: Node) -> None:
            if node is not None:
                _inorder(node.left)
                print(node.value)
                _inorder(node.right)

        _inorder(self.root)

    def search(self, value: int) -> bool:
        def _search

