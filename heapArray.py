class heapA:

    def __init__(self, val=None):
        if val is None:
            self._data_array = []
            self._size = 0
        else:
            self._data_array = [val]
            self._size = 1

    def __str__(self):
        return str(self._data_array)

    def _increment_size(self):
        self._size += 1

    def _decrement_size(self):
        self._size -= 1

    def __len__(self):
        return self._size

    def get_item(self, pos=None): #get item from end of array
        if pos is None:
            index = len(self) - 1
        else:
            index = pos - 1

        return self._data_array[index]

    def set_item(self, val, pos = 1): # set item at start of array
        index = pos - 1
        self._data_array[index] = val

    def insert(self, val):
        self._data_array.append(val)
        self._increment_size()
        self._heapify_up()
        return val

    def remove(self):
        first_item = self.get_item()
        last_item = self._data_array.pop()
        self._decrement_size()
        self.set_item(last_item)
        self._heapify_down()
        return first_item

    def _swap(self, posA, posB):
        self._data_array[posA-1], self._data_array[posB-1] = self._data_array[posB-1], self._data_array[posA-1]

    def _heapify_up(self):
        pos = len(self)
        pos_parent = pos >> 1

        while pos_parent > 0:
            if self.get_item(pos) < self.get_item(pos_parent):
                self._swap(pos, pos_parent)
                pos_parent = pos >> 1
            else:
                break

    def _heapify_down(self):
        pos = 1
        size = len(self)
        while 2 * pos <= size:
            pos_left, pos_right = 2*pos, 2*pos+1
            left, right = self.get_item(pos_left), self.get_item(pos_right)
            if right:
                pos_min_child = pos_left if left < right else pos_right
            else:
                pos_min_child = pos_left

            if self.get_item(pos) > self.get_item(pos_min_child):
                self._swap(pos, pos_min_child)
                pos = pos_min_child
            else:
                break

    @classmethod
    def from_list(cls, list_val):
        heap = cls()
        for val in list_val:
            heap.insert(val)
        return heap