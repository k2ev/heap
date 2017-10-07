from heapArray import heapA, heapAMax
import operator
import collections
import math
import statistics

class heapAMinMax(heapA):
    def __init__(self,val=None):
        super().__init__(val)

    def sift_up(self, pos=None):
        pos = pos or len(self)
        pos_val = self.item(pos)
        pos_parent = pos >> 1
        parent_val = self.item(pos_parent)
        if parent_val is not None:
            if self.is_min_level(pos):
                if operator.gt(pos_val, parent_val):
                    self.swap(pos, pos_parent)
                    self._sift_up(pos_parent, operator.gt, 2)
                else:
                    self._sift_up(pos, operator.lt, 2)
            else:
                if operator.lt(pos_val, parent_val):
                    self.swap(pos, pos_parent)
                    self._sift_up(pos_parent, operator.lt, 2)
                else:
                    self._sift_up(pos, operator.gt, 2)

    def heapify(self, pos=1):
        if self.is_min_level(pos):
            self._heapify(pos, operator.gt)
        else:
            self._heapify(pos, operator.lt)

    def _heapify(self, pos=1, op_cmp=operator.gt):
        if pos <= self.size and self._child_exists(pos):  # atleast left child exists
            pos_val = self.item(pos)
            min_max_pos, min_max_val = self._min_max_family(pos, self.op_flip(op_cmp), 2)
            if min_max_pos in self.pos_children(pos):
                if op_cmp(pos_val, min_max_val):
                    self.swap(pos, min_max_pos)
            else:
                if min_max_val is not None and op_cmp(pos_val, min_max_val):
                    self.swap(pos, min_max_pos)
                    min_max_parent_pos = self.pos_parent(min_max_pos)
                    min_max_parent_val = self.item(min_max_parent_pos)
                    if min_max_parent_val is not None and op_cmp(min_max_parent_val, min_max_val):
                        self.swap(min_max_pos, min_max_parent_pos)
                    self._heapify(min_max_pos, op_cmp)

    def min(self):
        return self.peek()

    def max(self):
        index, val = self._min_max_family(1, operator.gt)
        return val

    def pop_max(self):
        max_item_pos, max_item = self._min_max_family(1, operator.gt)
        last_item = self.remove_last()
        self.set_item(max_item_pos, last_item)
        self.heapify(max_item_pos)

    @staticmethod
    def is_min_level(x):
        # even levels are min, root is level 0
        level = int(math.floor(math.log2(x)))
        return not (level & 1)

class heapATwin:
    def __init__(self, h1=None, h2=None):
        self._min_heap = heapA() if h1 is None else heapA.from_list(h1)
        self._max_heap = heapAMax() if h2 is None else heapAMax.from_list(h2)

    def __repr__(self):
        return [repr(self.min_heap), repr(self.max_heap)]

    def __str__(self):
        if self.min_heap.size:
            return str(self.min_heap) + "\n*\n" + str(self.max_heap)
        else:
            return ""

    @property
    def min_heap(self):
        return self._min_heap

    @property
    def max_heap(self):
        return self._max_heap

    def size(self):
        return self.min_heap.size + self.max_heap.size

    def _pos_last(self):
        if self._last_in_min_heap():
            return self.max_heap._pos_last()
        else:
            return self.min_heap._pos_last()

    def _last_in_min_heap(self):
        if self.size():
            return self.min_heap.size > self.max_heap.size
        else:
            return False

    def _pos_correspond(self, pos):
        corresponding = pos
        if self.min_heap.size > self.max_heap.size:
            if pos == self.min_heap._pos_last():
                corresponding =  pos // 2
        return corresponding

    def _swap_cross_heap_info(self, pos):
        pos_correspond = self._pos_correspond(pos)
        temp_1, temp_2 = self.min_heap.item(pos), self.max_heap.item(pos_correspond)
        if self.min_heap.item(pos) > self.max_heap.item(pos_correspond):
            self.min_heap.set_item(pos, temp_2)
            self.max_heap.set_item(pos_correspond, temp_1)
            return True, pos_correspond
        else:
            return False, pos

    def _swap_cross_heap(self, pos):
        return self._swap_cross_heap(pos)[1]

    def insert(self, val):
        if val is not None:
            if isinstance(val, collections.Sequence):
                for elem in val:
                    self.insert(elem)
            else:
                # pos_correspond is same index if total items are even numbered
                # for odd numbered, two implementations exists
                # in this implementation, min heap is allowed up to one more than max heap
                # another implementation is to keep it same in both heaps, and then remaining item is in buffer
                # in prior approach implemented here, if corresponding item doesnt exists then look up parent
                # in later approach, no need to do so as buffer is maintained
                if self.size() == 0:
                    self.min_heap.insert(val)
                else:
                    if self._last_in_min_heap():
                        heap_select, heap_alt = self.max_heap, self.min_heap
                    else:
                        heap_select, heap_alt = self.min_heap, self.max_heap

                    heap_select.insert(val)
                    pos = heap_select.size
                    swap_flag, swap_pos = self._swap_cross_heap_info(pos)

                    if swap_flag:
                        heap_alt.sift_up(swap_pos)
                    else:
                        heap_select.sift_up(swap_pos)


    def swap(self, posA, posB=None):
        posB = posB or posA
        temp_x, temp_y = self.min_heap.item(posA), self.max_heap.item(posB)
        self.min_heap.set_item(posA, temp_y)
        self.max_heap.set_item(posB, temp_x)

    def remove(self):
        if self.min_heap.size:
            min_item = self.min_heap.peek()
            self.min_heap.set_item(1, math.inf)
            pos = self.min_heap._heapify_w_info()
            if pos == self._pos_last():
                self.min_heap.remove_last()
                return min_item
            else:
                if self.min_heap.size > self.max_heap.size:
                    last_item = self.max_heap.remove_last()
                else:
                    last_item = self.min_heap.remove_last()
                self.min_heap.set_item(pos, last_item)

                swap_flag, swap_pos = self._swap_cross_heap_info(pos)
                if swap_flag:
                    self.max_heap.sift_up(swap_pos)
                else:
                    self.min_heap.sift_up(swap_pos)
            return min_item
        else:
            return None

    def peek(self):
        return self.min()

    def min(self):
        if self.min_heap.size:
            return self.min_heap.peek()
        else:
            return None

    def max(self):
        if self.max_heap.size:
            return self.max_heap.peek()
        elif self.min_heap.size:
            return self.min_heap.peek()
        else:
            return None

    def push(self, val):
        return self.insert(val)

    def pop(self):
        return self.remove()

    def pop_max(self):
        if self.max_heap.size:
            max_item = self.max_heap.peek()
            self.max_heap.set_item(1, -math.inf)
            pos = self.max_heap._heapify_w_info()

            if pos == self._pos_last():
                self.max_heap.remove_last()
                return max_item
            else:
                if self.min_heap.size > self.max_heap.size:
                    last_item = self.min_heap.remove_last()
                else:
                    last_item = self.max_heap.remove_last()
                self.max_heap.set_item(pos, last_item)

                swap_flag, swap_pos = self._swap_cross_heap_info(pos)
                if swap_flag:
                    self.min_heap.sift_up(swap_pos)
                else:
                    self.max_heap.sift_up(swap_pos)
            return max_item
        elif self.min_heap.size:
            return self.pop()
        else:
            return None

    def is_valid(self):
        is_valid = True
        # size
        if self.min_heap.size != self.max_heap.size and self.min_heap.size != self.max_heap.size + 1:
            return False

        if self.size() != self.min_heap.size + self.max_heap.size:
            return False

        for key, val in enumerate(self.min_heap):
            if key < self.max_heap.size and val > self.max_heap.item(key+1):
                return False

        return is_valid


    @classmethod
    def from_list(cls, list_val):
        if isinstance(list_val, collections.Sequence):
            median = statistics.median(list_val)  # this can be optimized to be O(N)
            min_h, max_h = [], []
            for val in list_val:
                if val <= median:
                    min_h.append(val)
                else:
                    max_h.append(val)
            return cls(min_h, max_h)
        else:
            return cls()


class Deap(heapA):
    _offset = 1

    def __init__(self):
        self._data_array = [None]
        self._size = 0

    def _swap_cross_heap(self, pos_current):
        pos_alt = self._corresponding_pos(pos_current)
        if self.in_min_heap(pos_current):
            if self.item(pos_alt) is not None and self.item(pos_current) > self.item(pos_alt):
                self.swap(pos_current, pos_alt)
                pos_current = pos_alt
        else:
            if self.item(pos_alt) is not None and self.item(pos_current) < self.item(pos_alt):
                    self.swap(pos_current, pos_alt)
                    pos_current = pos_alt
        return pos_current

    def sift_up(self, pos=None):
        pos_current = pos or self._pos_last()
        pos_current = self._swap_cross_heap(pos_current)

        if self.in_min_heap(pos_current):
            return super()._sift_up(pos_current, operator.lt)
        else:
            return super()._sift_up(pos_current, operator.gt)

    def sift_up_partial(self, pos=None, pos_root=1):
        pos_current = pos or self._pos_last()
        pos_current = self._swap_cross_heap(pos_current)

        if self.in_min_heap(pos_current):
            return super()._sift_up(pos_current, operator.lt, 1, pos_root)
        else:
            return super()._sift_up(pos_current, operator.gt, 1, pos_root)

    def insert(self, val=None):
        if val is not None:
            if isinstance(val, collections.Sequence):
                for elem in val:
                    self.insert(elem)
            else:
                self._data_array.append(val)
                self.increment_size()
                pos_current = self._pos_last()
                self.sift_up(pos_current)

    def _remove(self, pos=None):
        pos = pos or self._pos_first()
        if self.size:
            if pos == self._pos_last():
                last_item = self.remove_last()
                return last_item
            else:
                first_item = self.item(pos)
                pos_first_item = pos
                last_item = self.remove_last()
                if self.size:
                    if self.in_min_heap(pos):
                        self.set_item(pos_first_item, math.inf)
                        pos_current = self._heapify_w_info(pos_first_item, operator.gt)
                    else:
                        self.set_item(pos_first_item, -math.inf)
                        pos_current = self._heapify_w_info(pos_first_item, operator.lt)
                    self.set_item(pos_current, last_item)  # reinsert last item at a leaf position
                    self.sift_up(pos_current)
                return first_item
        else:
            return None

    def remove(self):
        return self._remove()

    def pop_max(self):
        if self.size:
            if self.size == 1:
                return self._remove()
            else:
                pos_first_item = self._pos_first() + 1
                return self._remove(pos_first_item)
        else:
            return None

    def max(self):
        if self.size:
            if self.size == 1:
                return self.peek()
            else:
                return self.item(self._pos_first()+1)

    def min(self):
        if self.size:
            return self._pos_first()

    def _heapify_w_info(self, pos=None, op_cmp=None):
        pos = pos or self._pos_last()
        if self.in_min_heap(pos):
            return super()._heapify_w_info(pos, operator.gt)
        else:
            return super()._heapify_w_info(pos, operator.lt)

    def _heapify(self, pos=None, op_cmp=operator.gt):
        pos = pos or self._pos_last()
        _ = self._heapify_w_info(pos)

    def _corresponding_pos(self, pos):
        corresponding_pos = self._corresponding_pos_all(pos)
        max_pos, max_val = None, None
        for p in corresponding_pos:
            if max_pos is None or self.item(p) > max_val:
                max_pos, max_val = p, self.item(p)
        return max_pos


    def _corresponding_pos_all(self, pos):
        level = self.level(pos)
        nodes_at_prior_level = self.nodes_at_level(level - 1)
        pos_last_node = self._pos_last()
        # This deviates from original paper. There are more stringent situations to ensure
        # algorithm works for edge cases.
        if self.in_min_heap(pos):
            corresponding_node = pos + nodes_at_prior_level
            if  corresponding_node > pos_last_node:
                parent = self.pos_parent(corresponding_node)
                # this is a stricter condition that makes last node as corresponding node
                if self._child_exists(parent):
                    left_child = self.pos_left_child(pos)
                    return [left_child]
                else:
                    return [parent]
            else:
                return [corresponding_node]
        else: # in max heap
            corresponding_node =  pos - nodes_at_prior_level
            # this deviates from paper. Node in max heap can have more than one correspondence
            # first case is when its a last node that's also left. In that case, choose all children of
            # parent of corresponding node i.e. choose sibling of corresponding node
            # second case is when corresponding node is a parent. In that case, choose all children.
            all_nodes = []
            if pos is self._pos_last() and pos == self.pos_left_child(self.pos_parent(pos)):
                parent_corresponding_node = self.pos_parent(corresponding_node)
                for p in self.pos_children(parent_corresponding_node):
                    if p <= pos_last_node:
                        all_nodes.append(p)
                return all_nodes
            elif self._child_exists(corresponding_node):
                for p in self.pos_children(corresponding_node):
                    if p <= pos_last_node:
                        all_nodes.append(p)
                return all_nodes
            else:
                return [corresponding_node]


    def is_valid(self):
        is_valid = True


        for index, val in enumerate(self._data_array):
            pos = index + self._offset

            if pos == 1:
                if val is not None:
                    return False
            else:
                if self.in_min_heap(pos):
                    _, min_child = self._min_max_family(pos, operator.lt)
                    if min_child is not None and val > min_child:
                        return False

                    alt_pos = self._corresponding_pos(pos)
                    if( self.item(alt_pos) < val ):
                        return False
                else:
                    _, max_child = self._min_max_family(pos, operator.gt)
                    if max_child is not None and val < max_child:
                        return False

        if self.size != len(self._data_array) - self._offset:
            return False

        return is_valid

    @classmethod
    def in_min_heap(cls, pos):
        level = cls.level(pos)
        nodes_at_prior_level = cls.nodes_at_level(level-1)
        if cls.level(nodes_at_prior_level + pos) == level:
            return True
        else:
            return False

    @staticmethod
    def partition(list_val, pivot_index):
        list_size = len(list_val)
        pivot = list_val[pivot_index]
        # swap pivot with last element
        list_val[pivot_index], list_val[list_size - 1] = list_val[list_size - 1], list_val[pivot_index]
        # i is boundary of partition with smaller elements; j is boundary of partition with higher elements.
        # in between i and j is the working area
        i, j = 0, list_size - 1
        while j > i:
            if list_val[j - 1] > pivot:
                list_val[j] = list_val[j - 1]
                j = j - 1
            else:
                list_val[i], list_val[j - 1] = list_val[j - 1], list_val[i]
                i = i + 1
        list_val[j] = pivot
        return j

    @classmethod
    def from_list(cls, list_val):
        heap = cls()
        if isinstance(list_val, collections.Sequence):
            heap._data_array.extend(list_val)
            heap._size = len(list_val)
            pos_first = heap._pos_first()
            pos_last = pos_first + heap._size - 1
            # original paper is very cryptic about this part. There are various interpretations
            # but after a lot of iterations this works. Start backwards from node that may have last node as
            # corresponding node.
            pos_current = max(heap._corresponding_pos_all(heap._pos_last()))
            while pos_current >= pos_first:
                current, current_val = pos_current, heap.item(pos_current)
                if heap.in_min_heap(current):
                    heap.set_item(current, math.inf)
                    current = heap._heapify_w_info(current, operator.gt)
                else:
                    heap.set_item(current, -math.inf)
                    current = heap._heapify_w_info(current, operator.lt)
                heap.set_item(current, current_val)
                # this is also unique as this restricts location to which you should sift.
                # in general think of it as that sifting is fixing the heaps.
                # At any given time you are interested in only fixing that heap upto the node
                # or corresponding sub-heap that came before it. Also, something that original implementation
                # conveniently ignored
                heap.sift_up_partial(current, pos_current)
                pos_current = pos_current - 1
            return heap






