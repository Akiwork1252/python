from typing import Any
from collections import deque


class Queue:

    def __init__(self) -> None:
        self.queue = []

    def enqueue(self, data: Any) -> None:
        self.queue.append(data)

    def dequeue(self) -> Any:
        if self.queue:
            return self.queue.pop(0)


if __name__ == '__main__':
    # q = Queue()
    # q.enqueue(1)
    # q.enqueue(2)
    # q.enqueue(3)
    # q.enqueue(4)
    # print(q.dequeue())
    # print(q.queue)
    q = deque()
    q.append(1)
    q.append(2)
    q.append(3)
    q.append(4)
    print(q)
    print(q.popleft())
    print(q.popleft())
    print(q)
    print(q.pop())