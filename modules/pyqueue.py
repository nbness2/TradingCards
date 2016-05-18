class Reference:

    def __init__(self, data, last_val, next_val):
        self.data = data
        self.last_val = last_val
        self.next_val = next_val


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
            current_ref = current_ref.next_val
        retstr = retstr[:len(retstr)-2] + ']'
        return retstr

    def __len__(self):
        length = 0
        current_ref = self.head
        while current_ref:
            length += 1
            current_ref = current_ref.next_val
        return length

    def append(self, data):
        new_ref = Reference(data, None, None)
        if self.head is None:
            self.head = self.end = new_ref
        else:
            new_ref.last_val, new_ref.next_val = self.end, None
            self.end.next_val, self.end = new_ref, new_ref

    def remove(self, value, left=False):
        #removes leftmost\rightmost value, depending on the left parameter.
        current_ref = self.head if left else self.end
        while current_ref:
            if current_ref.data == value:
                if current_ref.last_val and current_ref.next_val:
                    current_ref.last_val.next_val = current_ref.next_val
                    current_ref.next_val.last_val = current_ref.last_val
                else:
                    if left:
                        self.head = current_ref.next_val
                        current_ref.next_val.last_val = None
                    else:
                        self.end = current_ref.last_val
                        current_ref.last_val.next_val = None
            else:
                current_ref = current_ref.next_val if left else current_ref.last_val
            break

    def reveal(self):
        current_ref = self.head
        while current_ref:
            print(current_ref.last_val.data if current_ref.last_val else None,
                  current_ref.data,
                  current_ref.next_val.data if current_ref.next_val else None)
            current_ref = current_ref.next_val


class Queue:
    def __init__(self, qtype='f', maxsize=None):
        if qtype.lower()[0] in 'lf':
            self.qtype = qtype
        else:
            raise TypeError('qtype must be (l) or (f)')
        if maxsize:
            self.maxsize = maxsize
        else:
            self.maxsize = 0
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def put(self, item):
        if self.maxsize > 0:
            if self.isfull():
                raise ValueError('Queue is full')
        self.queue.append(item)

    def get(self):
        if self.qtype == 'f':
            return self.queue.pop(0)
        elif self.qtype == 'l':
            return self.queue.pop(len(self.queue)-1)
        else:
            raise TypeError('Type must be (l) or (f)')

    def empty(self):
        return not bool(self.queue)

    def isfull(self):
        return len(self) == self.maxsize if self.maxsize <= 0 else False


class DEQueue(Queue):
    def __init__(self, qtype='f', maxsize=None):
        Queue.__init__(self, qtype, maxsize)
        pass