"""Realizes a custom queue"""


class InspectedQueue:
    """Realizes a queue with a methods inspect and inspect_next"""
    def __init__(self):
        self.queue: list[object] = []

    def get(self) -> object:
        """Return and delete first element of the queue"""
        return self.queue.pop(0)

    def inspect(self) -> object:
        """Return first element of the queue"""
        return self.queue[0]

    def inspect_next(self) -> object:
        """Return second element of the queue"""
        return self.queue[1]

    def put(self, value: object):
        """Add element to the end of the queue"""
        self.queue.append(value)

    def is_empty(self) -> bool:
        """Check if the queue is empty"""
        return len(self.queue) == 0
