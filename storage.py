import threading
from collections import deque

class ThreadSafeKVStore:
    #key-value store.
    #threading.Lock to prevent race condition when multiple workers try to read or write simultaneouslyu

    def __init__(self):
        self._store = {}
        #only one thread can access dictionary at a time
        self._lock = threading.Lock()

    def put(self, key, value):
        #'with' acquires the lock, executes the block, and releases the lock
        with self._lock:
            self._store[key] = value

    def get(self, key):
        #readers also need to have the lock to prevent reading incomplete data
        with self._lock:
            return self._store.get(key, None)

class ThreadSafeTaskQueue:
    #thrading.Condition allows workers to wait efficiently for new task without burning CPU cycles

    def __init__(self):
        #double ended queue optimized for appends and pops
        self._queue = deque()
        self._condition = threading.Condition()

    def enqueue(self, task):
        with self._condition:
            self._queue.append(task)
            #wake up a worker that is currently blocked in dequeue
            self._condition.notify()

    def dequeue(self):
        with self._condition:
            while not self._queue:
                self._condition.wait() # Block until notified
            return self._queue.popleft()