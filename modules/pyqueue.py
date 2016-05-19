class Reference:
    def __init__(self, data, last_ref, next_ref):
        self.data, last_ref, next_ref = data, last_ref, next_ref

    def __str__(self):
        retstr = str([self.last_ref.data if self.last_ref else None, self.data, self.next_ref.data if self.next_ref else None])
        return retstr[1:-1]


class DoubleLinkedList:
    head = None
    end = None

    def __str__(self):
        if len(self) < 1:
            return '[]'
        current_ref = self.head
        retstr = '['
        while current_ref:
            retstr = retstr + str(current_ref.data) + ', '
            current_ref = current_ref.next_ref
        retstr = retstr[:len(retstr)-2] + ']'
        return retstr

    def __len__(self):
        length = 0
        current_ref = self.head
        while current_ref:
            length += 1
            current_ref = current_ref.next_ref
        return length

    def _append(self, data, left=False):
        new_ref = Reference(data, None, None)
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

    def _pop(self, left=False):
        if len(self):
            ref = self.head if left else self.end
            self.remove(ref.data, left)
            return ref.data
        raise IndexError('pop from empty dequeue')

    def pop(self, i=True):
        return self._pop(bool(i))

    def popleft(self):
        return self._pop(True)

    def remove(self, value, left=False):
        current_ref = self.head if left else self.end
        if not len(self):
            raise IndexError('remove item from empty dequeue')
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
            print(current_ref)
            current_ref = current_ref.next_ref


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
            return self.queue.pop(len(self.queue)-1)
        else:
            raise TypeError('Type must be (l) or (f)')

    def empty(self):
        return not bool(self.queue)

    def isfull(self):
        return len(self) == self.maxsize if self.maxsize <= 0 else False


class DEQueue(Queue):
    def __init__(self, queue_type='f', maxsize=None):
        Queue.__init__(self, queue_type, maxsize)
        pass
