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

    def __init__(self, iterable=[]):
        self.extend(iterable)

    def __str__(self):
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
        length = len(self)
        if abs(item) > length:
            raise IndexError('single linked list index out of range')
        if item < 0:
            item += length
        current_ref = self.head
        i = 0
        while i != item:
            current_ref = current_ref.next_ref
            i += 1
        return current_ref.data

    def __delitem__(self, item):
        if item > len(self)-1:
            raise IndexError('single linked list index out of range')
        current_ref = self.head
        i = 0
        while i != item:
            last_ref = current_ref
            current_ref = current_ref.next_ref
            next_ref = current_ref.next_ref
            i += 1
        if i == 0:
            self.head = current_ref.next_ref
        else:
            last_ref.next_ref = next_ref
        del current_ref

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

    def remove(self, item):
        del self[item]

    def pop(self, item):
        if item > len(self)-1:
            raise IndexError('pop from empty single linked list')
        return (self[item], self.remove(item))[0]



class DoubleLinkedList:
    head = None
    end = None

    def __init__(self, iterable=[]):
        self.extend(iterable)

    def __str__(self):
        if len(self) < 1:
            return '[]'
        current_ref = self.head
        retstr = '['
        while current_ref:
            retstr = retstr + repr(current_ref.data) + ', '
            current_ref = current_ref.next_ref
        return retstr[:-2]+']'

    def __len__(self):
        length = 0
        current_ref = self.head
        while current_ref:
            length += 1
            current_ref = current_ref.next_ref
        return length

    def __getitem__(self, item):
        i = 0
        neg = False
        if abs(item) > len(self):
            raise IndexError('double list index out of range')
        if item >= 0:
            current_ref = self.head
        else:
            neg = True
            current_ref = self.end
            item = -item
            i = 1
        while i != item:
            if not neg:
                current_ref = current_ref.next_ref
            else:
                current_ref = current_ref.last_ref
            i += 1
        return current_ref.data

    def _append(self, data, left=False):
        new_ref = Reference(data, None)
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

    def appendleft(self, data):
        self._append(data, True)

    def _extend(self, data, left=False):
        if not getattr(data, '__iter__'):
            raise TypeError('{} is not iterable'.format(type(data)))
        for item in data:
            self._append(item, left)

    def extend(self, data):
        self._extend(data)

    def extendleft(self, data):
        self._extend(data, True)

    def _pop(self, left=False):
        if len(self):
            ref = self.head if left else self.end
            self.remove(ref.data, left)
            return ref.data
        raise IndexError('pop from empty double list')

    def pop(self, i=True):
        return self._pop(bool(i))

    def popleft(self):
        return self._pop(True)

    def remove(self, value, left=False):
        current_ref = self.head if left else self.end
        if not len(self):
            raise IndexError('remove item from empty double list')
        while current_ref:
            if current_ref.data == value:
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
                break
            else:
                current_ref = current_ref.next_ref if left else current_ref.last_ref

    def reveal(self):
        current_ref = self.head
        while current_ref:
            print(current_ref.reveal(), end='\n')
            current_ref = current_ref.next_ref

#test = DoubleLinkedList()
#for x in range(128):
#    test.append(x)


class Queue:
    def __init__(self, queue_type='f', maxsize=None):
        if queue_type.lower()[0] in 'lf':
            self.queue_type = queue_type
        else:
            raise TypeError('queue_type must be (l) or (f)')
        if maxsize:
            self.maxsize = maxsize
        else:
            self.maxsize = 0
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def put(self, item):
        if self.isfull():
            raise ValueError('Queue is full')
        self.queue.append(item)

    def get(self):
        if self.queue_type == 'f':
            return self.queue.pop(0)
        elif self.queue_type == 'l':
            return self.queue.pop()
        else:
            raise TypeError('Type must be (l) or (f)')

    def empty(self):
        return not bool(self.queue)

    def isfull(self):
        return len(self) == self.maxsize if self.maxsize > 0 else False


class DEQueue(Queue):
    def __init__(self, queue_type='f', maxsize=None):
        Queue.__init__(self, queue_type, maxsize)
        self.queue = DoubleLinkedList()
