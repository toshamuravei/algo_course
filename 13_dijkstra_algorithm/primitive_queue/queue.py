
class PrimitivePriorityQueue:
    def __init__(self):
        self.priorities = []
        self.values = []
        self.priorities_stored = 0
        self.values_stored = 0

    def enqueue(self, priority, value):
        if priority in self.priorities:
            queue_index = self.priorities.index(priority)
        else:
            queue_index = self.place_new_priority(priority)
            self.initiate_queue_with_index(queue_index)
            self.priorities_stored += 1

        self.values[queue_index].append(value)
        self.values_stored += 1

    def place_new_priority(self, priority):
        for current_priority in self.priorities:
            if priority < current_priority:
                queue_index = self.priorities.index(current_priority)
                self.priorities.insert(queue_index, priority)
                break
        else:
            self.priorities.append(priority)
            queue_index = len(self.priorities) - 1
        return queue_index

    def initiate_queue_with_index(self, index):
        if index > self.priorities_stored:
            raise ValueError(f"Can't store values at non-existing idx: {index}")
        else:
            for i in range(0, self.priorities_stored):
                if index <= i:
                    self.values.insert(i, [])
                    return
            else:
                self.values.append([])

    def dequeue(self):
        if self.values_stored == 0:
            raise ValueError("Cannot dequeue from empty queue!")

        found_value = None
        for queue_idx in range(0, self.priorities_stored):
            queue = self.values[queue_idx]
            if queue:
                found_value = queue[0]
                del queue[0]
                self.values_stored -= 1
                return found_value

    def empty(self):
        return self.values_stored == 0

