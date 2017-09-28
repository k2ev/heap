import sys
sys.path.extend(['/Users/kiki/PycharmProjects/BTrees'])
from BTree import BTreeLinked

class heapT(BTreeLinked):

    node_type = "regular"

    def __init__(self, node=None):
        super().__init__(node)
        self._num_of_nodes = 1

    def insert(self, val):
        node = self._insert_last_node(val)
        self.heapify_up(node)
        return node

    def heapify_up(self, node):
        while node.parent and node < node.parent:
            node.item, node.parent.item = node.parent.item, node.item
            node = node.parent

    def remove(self):
        if self.root:
            node = self.root
            last_node = self._last_node()
            if last_node:
                self.root.item = last_node.item # copy into root
                # remove last node
                if last_node.is_left_child():
                    last_node.parent.left = None
                else:
                    last_node.parent.right = None
                last_node.parent = None
            else:
                self.root = None
            self._decrement_num_of_nodes()
            self.heapify_down()
        else:
            node = None

        return node


    def heapify_down(self):
        if self.root:
            current = self.root
            flag_heapify = True
            while current and flag_heapify:
                min_node = current.min_child_if_exists()
                if min_node and current > min_node:
                    current.item, min_node.item = min_node.item, current.item
                    current = min_node
                else:
                    flag_heapify = False

    def push(self, val):
        return self.insert(val)

    def pop(self):
        return self.remove()

    def _increment_num_of_nodes(self):
        self._num_of_nodes = self._num_of_nodes + 1

    def _decrement_num_of_nodes(self):
        self._num_of_nodes = self._num_of_nodes - 1

    @staticmethod
    def bin_repr(num):
        bin_repr = []
        while num != 0:
            bin_repr.insert(0, num & 1) # this is bit and op.
            num = num >> 1  # this is right shift or equivalent of dividing by 2
        return bin_repr

    def _last_node(self):
        # O(logn) instead of full bft.
        # http://theoryofprogramming.com/2015/02/01/binary-heaps-and-heapsort-algorithm/
        current = self.root
        num_of_nodes_bin_repr = self.bin_repr(self._num_of_nodes)
        num_of_nodes_bin_repr.pop(0)
        for bit in  num_of_nodes_bin_repr:
            if bit:
                current = current.right
            else:
                current = current.left
        return current

    def _insert_last_node(self, val):
        node = self.get_node(val)
        self._increment_num_of_nodes()
        if not self.root:
            self.root = node
        else:
            current = self.root
            num_of_nodes_bin_repr = self.bin_repr(self._num_of_nodes)
            num_of_nodes_bin_repr.pop(0)
            last_bit = num_of_nodes_bin_repr.pop()
            for bit in num_of_nodes_bin_repr:
                if bit:
                    current = current.right
                else:
                    current = current.left
            if last_bit:
                current.right = node
            else:
                current.left = node
            node.parent = current
        return node