
class Queue:
    def __init__(self):
        self.items = []

    def AddToQueue(self, item):
        self.items.append(item)

    def Dequeue(self):
        if self.isEmpty(): return None
        item = self.items.pop(0)
        return item
    
    def isEmpty(self):
        return len(self.items) == 0
    
class FunctionQueue:
    def __init__(self):
        self.items = []

    def AddToQueue(self, function, *args):
        self.items.append((function, args))

    def dequeue(self):
        if self.isEmpty(): return None
        item, args = self.items.pop(0)
        return item, args

    def isEmpty(self):
        return len(self.items) == 0