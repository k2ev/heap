import operator
import collections
import math

class heapA:

    # based on array whose size is tracked. array index starts with 0. array pos starts with 1
    # if n is pos of parent then left child is 2*n and right child is 2*n+1
    # if m is index of parent then left child is 2*m+1 and right child is 2*m+2
    # 1 | 2 3 | 4 5 - 6 7 | 8 9 - 10 11 - 12 13 - 14 15 |
    # 0 | 1 2 | 3 4 - 5 6 | 7 8 -  9 10 - 11 12 - 13 14 |
    # as can be seen child node for node at pos 6 are at pos 12 and 13
    # similarly, child node for node at index 5 are at index 11 and 12

    def __init__(self, val=None):
        if val is None:
            self._data_array = []
            self._size = 0
        else:
            self._data_array = [val]
            self._size = 1

    @property
    def data_array(self):
        return self._data_array

    @property
    def size(self):
        return self._size

    def __repr__(self):
        return str(self._data_array)

    def __str__(self):
        if self.size:
            data = self._data_array
            max_level = self.level(self.size)
            max_items = 2**(max_level+1)-1
            pos, level, heap_str, width = 1, 0, "", 2
            space_str, pad_str= ' ' * width, '_' * width
            while level <= max_level:
                items_at_level = 2**level
                intra_items = 2**(max_level-level)//2
                inter_items = divmod(max_items, items_at_level)[0] - 2*intra_items
                stub_items = (max_items - items_at_level - inter_items * (items_at_level-1) - 2*intra_items*items_at_level) // 2
                intra_items = 2**(max_level-level-1) if level < max_level else 0
                heap_str = heap_str + space_str * stub_items
                for current in range(0,items_at_level):
                    item = self.item(pos + current)
                    item_align= '>' if (pos+current)%2 else '<'
                    item_fmt = '{:{align}{width}}'.format(str(item if item is not None else space_str), align=item_align, width=width)
                    item_str = pad_str*intra_items+item_fmt+pad_str*intra_items
                    heap_str = heap_str + item_str + space_str * inter_items
                heap_str = heap_str.rstrip() + space_str * stub_items + "\n"
                pos, level = pos+items_at_level, level+1
            return heap_str
        else:
            return ""

    def increment_size(self):
        self._size += 1

    def decrement_size(self):
        self._size -= 1

    def __len__(self):
        return self._size

    def item(self, pos=None): #get item from end of array
        first, last = 0, len(self) - 1
        index = pos - 1 if pos else last
        return self._data_array[index] if index >= first and index <= last else None

    def set_item(self, pos = 1, val=None): # set item at start of array
        index = pos - 1
        self._data_array[index] = val

    def insert(self, val=None):
        if val is not None:
            if isinstance(val, collections.Sequence):
                for elem in val:
                    self.insert(elem)
            else:
                self._data_array.append(val)
                self.increment_size()
                self.sift_up()
        return val

    def remove_last(self):
        if self.size:
            last_item = self._data_array.pop()
            self.decrement_size()
            return last_item
        else:
            raise Exception

    def remove(self):
        if self.size:
            first_item = self.peek()
            last_item = self.remove_last()
            self.set_item(1, last_item)
            self.heapify()
            return first_item
        else:
            return None

    def swap(self, posA, posB):
        self._data_array[posA-1], self._data_array[posB-1] = self._data_array[posB-1], self._data_array[posA-1]

    def sift_up(self, pos=None):
        pos = pos or len(self)
        self._sift_up(pos, operator.lt)

    def heapify(self, pos=1):
        self._heapify(pos, operator.gt)

    def _sift_up(self, pos=None, op_cmp=operator.lt, shift=1):
        pos = pos or len(self)
        pos_parent = self.pos_parent(pos, shift)

        while pos_parent > 0:
            if op_cmp(self.item(pos), self.item(pos_parent)):
                self.swap(pos, pos_parent)
                pos = pos_parent
                pos_parent = self.pos_parent(pos, shift)
            else:
                break

    def _heapify_w_info(self, pos=1, op_cmp=operator.gt):
        if pos <= self.size and self._child_exists(pos): # at-least have one child
            pos_val = self.item(pos)
            min_max_pos, min_max_val = self._min_max_family(pos, self.op_flip(op_cmp))
            if min_max_val is not None and op_cmp(pos_val, min_max_val):
                self.swap(pos, min_max_pos)
                pos = min_max_pos
                return self._heapify_w_info(pos, op_cmp)
        return pos

    def _heapify(self, pos=1, op_cmp=operator.gt):
        _ = self._heapify_w_info(pos, op_cmp)

    def _child_exists(self, pos):
        return False if 2*pos > self.size else True

    def pop(self):
        return self.remove()

    def push(self, val):
        return self.insert(val)

    def peek(self):
        return self.item(1)

    def min(self):
        return self.peek(self)

    def max(self):
        raise Exception

    def is_empty(self):
        return False if self.size > 0 else True

    @classmethod
    def merge(cls, heapA, heapB):
        heapA_data = heapA.data_array
        heapB_data = heapB.data_array
        heapA_data.extend(heapB_data)
        return cls.from_list(heapA_data)

    @classmethod
    def from_list(cls, list_val):
        heap = cls()
        if isinstance(list_val, collections.Sequence):
            heap._data_array = list_val
            heap._size = len(list_val)
            parent_pos = cls.pos_parent(heap._size)
            while parent_pos > 0:
                heap.heapify(parent_pos)
                parent_pos = parent_pos - 1
        return heap

    @classmethod
    def pos_children(cls, pos):
        return [2*pos, 2*pos+1]

    @classmethod
    def pos_parent(cls, pos, shift=1):
        return pos >> shift

    def _min_max_family(self, pos, op_cmp=operator.lt, num_levels = 1):
        family = family_current = self.pos_children(pos)
        current_level = 1
        while current_level < num_levels:
            family_next = []
            for p in family_current:
                family_next.extend(self.pos_children(p))
            family.extend(family_next)
            family_current = family_next
            current_level += 1

        pos, val = None, None
        for current in family:
            current_val = self.item(current)
            if current_val is not None and (val is None or op_cmp(current_val, val)):
                pos, val = current, current_val

        return pos, val

    @classmethod
    def op_flip(cls, op):
        if op is operator.gt:
            return operator.lt
        elif op is operator.lt:
            return operator.gt
        else:
            raise Exception

    @staticmethod
    def level(x):
        return int(math.floor(math.log2(x)))

class heapAMax(heapA):
    def __init__(self,val=None):
        super().__init__(val)

    def sift_up(self, pos=None):
        super()._sift_up(pos, operator.gt)

    def heapify(self, pos=1):
        super()._heapify(pos, operator.lt)

    def _heapify(self, pos=1, op_cmp=operator.lt):
        _ = self._heapify_w_info(pos, op_cmp)

    def _heapify_w_info(self, pos=1, op_cmp=operator.lt):
         return super()._heapify_w_info(pos, op_cmp)

    def max(self):
        return self.peek()

    def min(self):
        raise Exception

