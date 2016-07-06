class Reference:
    def __init__(self, data, next_ref):
        self.data = data
        self.next_ref = next_ref

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return hex(id(self))

    def reveal(self):
        try:
            revealed = str([self.last_ref.data if self.last_ref else None,
                            self.data,
                            self.next_ref.data if self.next_ref else None])
        except AttributeError:
            revealed = str([self.data, self.next_ref.data])
        return revealed


class SingleLinkedList:
    head = None
    end = None
    structname = 'single linked list'

    def __init__(self, iterable=()):
        self.extend(iterable)

    def __str__(self):
        if not len(self):
            return '[]'
        current_ref = self.head
        retstr = '['
        while current_ref:
            retstr += repr(current_ref.data)+', '
            current_ref = current_ref.next_ref
        return retstr[:-2]+']'

    def __len__(self):
        current_ref = self.head
        length = 0
        while current_ref:
            length += 1
            current_ref = current_ref.next_ref
        return length

    def __getitem__(self, item):
        if type(item) != int:
            raise TypeError('list indices must be integer, not {}'.format(type(item)))
        length = len(self)
        if abs(item) > length:
            raise IndexError('{} index out of range'.format(self.structname))
        if item < 0:
            item += length
        del length
        current_ref = self.head
        i = 0
        while i != item:
            current_ref = current_ref.next_ref
            i += 1
        return current_ref.data

    def __delitem__(self, item):
        self._remove(item)

    def append(self, data):
        new_ref = Reference(data, None)
        if self.head is None:
            self.head = self.end = new_ref
        else:
            self.end.next_ref = new_ref
            self.end = new_ref

    def extend(self, data):
        if not getattr(data, '__iter__'):
            raise TypeError('{} object is not iterable'.format(type(data)))
        for item in data:
            self.append(item)
        del data

    def _remove(self, item, length=None):
        length = length if length else len(self)
        if type(item) != int:
            raise TypeError('list indices must be integer, not {}'.format(type(item)))
        if item > length-1:
            raise IndexError('{} index out of range'.format(self.structname))
        current_ref = self.head
        i = 0
        while i != item:
            last_ref = current_ref
            current_ref = current_ref.next_ref
            next_ref = current_ref.next_ref
            i += 1
        data = current_ref.data
        if i == 0:
            self.head = current_ref.next_ref
        else:
            last_ref.next_ref = next_ref
        del current_ref
        return data

    def _pop(self, item=None):
        length = len(self)
        if item is None:
            item = length-1
        if type(item) != int:
            raise TypeError('list indices must be integer, not {}'.format(type(item)))
        if not length:
            raise IndexError('pop from empty {}'.format(self.structname))
        if 0 < item > length-1 or (0 > item and abs(item) > length):
            raise IndexError('pop index out of range')
        return self._remove(item, length)

    def pop(self, item=None):
        return self._pop(item)

    def popleft(self):
        return self._pop(0)


class DoubleLinkedList(SingleLinkedList):
    structname = 'double linked list'

    def __init__(self, iterable=()):
        SingleLinkedList.__init__(self, iterable)

    def __getitem__(self, item):
        length = len(self)
        left = False
        i = 0

        while True:
            if item >= 0:
                if item >= length//2:
                    item = abs(item-length+1)
                    current_ref = self.end
                else:
                    left = True
                    current_ref = self.head
                break
            else:
                item = abs(item+length)
        del length

        while current_ref:
            if i == item:
                return current_ref.data
            else:
                if left:
                    current_ref = current_ref.next_ref
                else:
                    current_ref = current_ref.last_ref
                i += 1

    def _remove(self, item, length=None):
        length = length if length else len(self)
        left = False
        i = 0

        while True:
            if item >= 0:
                if item >= length//2:
                    item = abs(item-length+1)
                    current_ref = self.end
                else:
                    left = True
                    current_ref = self.head
                break
            else:
                item = abs(item+length)
        del length

        while current_ref:
            if i == item:
                data = current_ref.data
                if current_ref.last_ref and current_ref.next_ref:
                    current_ref.last_ref.next_ref = current_ref.next_ref
                    current_ref.next_ref.last_ref = current_ref.last_ref
                else:
                    if left:
                        self.head = current_ref.next_ref
                        if current_ref.next_ref:
                            current_ref.next_ref.last_ref = None
                    else:
                        self.end = current_ref.last_ref
                        if current_ref.last_ref:
                            current_ref.last_ref.next_ref = None
                del current_ref
                return data
            else:
                if left:
                    current_ref = current_ref.next_ref
                else:
                    current_ref = current_ref.last_ref
                i += 1

    def _append(self, data, left=False):
        new_ref = Reference(data, None)
        new_ref.last_ref = None
        if self.head is None:
            self.head = self.end = new_ref
        else:
            if left:
                new_ref.next_ref = self.head
                new_ref.last_ref = None
                self.head.last_ref = new_ref
                self.head = new_ref
            else:
                new_ref.last_ref = self.end
                new_ref.next_ref = None
                self.end.next_ref = new_ref
                self.end = new_ref

    def append(self, data):
        self._append(data)
        del data

    def appendleft(self, data):
        self._append(data, True)
        del data

    def _extend(self, iterable, left=False):
        if not getattr(iterable, '__iter__'):
            raise TypeError('{} is not iterable'.format(type(iterable)))
        for item in iterable:
            self._append(item, left)
        del iterable

    def extend(self, iterable):
        self._extend(iterable)
        del iterable

    def extendleft(self, iterable):
        self._extend(iterable, True)
        del iterable

    def popright(self):
        return self._pop()

    def popleft(self):
        return self._pop(0)
