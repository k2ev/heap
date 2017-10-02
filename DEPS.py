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

    def insert(self, val):
        if val is not None:
            if isinstance(val, collections.Sequence):
                for elem in val:
                    self.insert(elem)
            else:
                if self.min_heap.size <= self.max_heap.size:
                    pos = self.min_heap.size + 1
                    # pos_correspond is same index if total items are even numbered
                    # for odd numbered, two implementations exists
                    # in this implementation, min heap is allowed up to one more than max heap
                    # another implementation is to keep it same in both heaps, and then remaining item is in buffer
                    # in prior approach implemented here, if corresponding item doesnt exists then look up parent
                    # in later approach, no need to do so as buffer is maintained
                    pos_correspond = pos if pos == self.max_heap.size else pos // 2
                    if val > self.max_heap.item(pos_correspond):
                        temp, val = val, self.max_heap.item(pos_correspond)
                        self.max_heap.set_item(pos_correspond, temp)
                        self.max_heap.sift_up(pos_correspond)
                    self.min_heap.insert(val)
                else:
                    pos = self.max_heap.size + 1
                    pos_correspond = pos
                    if val < self.min_heap.item(pos_correspond):
                        temp, val = val, self.min_heap.item(pos_correspond)
                        self.min_heap.set_item(pos_correspond, temp)
                        self.min_heap.sift_up(pos_correspond)
                    self.max_heap.insert(val)

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
            if self.min_heap.size > self.max_heap.size:
                if pos == self.min_heap.size:
                    _ = self.min_heap.remove_last()
                else:
                    self.min_heap.swap(pos, self.min_heap.size)
                    _ = self.min_heap.remove_last()
                    if self.min_heap.item(pos) > self.max_heap.item(pos):
                        self.swap(pos)
                        self.min_heap.sift_up(pos)
            else:
                last_item = self.max_heap.remove_last()
                self.min_heap.set_item(pos, last_item)
                self.min_heap.sift_up(pos)
            return min_item
        else:
            return None

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
            if self.min_heap.size >= self.max_heap.size:
                self.swap(self.min_heap.size, pos)
                self.min_heap.remove_last()
                self.max_heap.sift_up(pos)
            else:
                self.max_heap.swap(pos, self.max_heap.size)
                self.max_heap.remove_last()
        else:
            return None

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




