########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2016, Swarthmore College
########################################

from collections import deque
from heapq import heappush, heappop

class _Queue(object):
    """Abstract base class for FIFO_Queue, LIFO_QUEUE, and Priority_Queue
    A queue supports the following operations:
        - adding items with add()
        - removing and returning items with get()
        - determining the number of items with len()
        - checking containment with 'in'
        - printing
    Child classes are required to store items in the self.contents field, but
    may use different data structures for self.contents. Child classes
    importantly differ in which item is returned by get().
    """
    def __init__(self):
        self.contents = deque()

    def add(self, item):
        """Stores item in the queue."""
        self.contents.append(item)

    def get(self):
        """Removes some item from the queue and returns it."""
        raise NotImplementedError("Child classes must implement get.")

    def __len__(self):
        """ 'len(q)' calls this method.  Passes the len() call to
        self.contents. This requires that all child classes implement
        contents as a Python type with a valid __len__.
        """
        return len(self.contents)

    def __repr__(self):
        """ 'print q' calls this method.  Passes the repr() call to
        self.contents. This requires that all child classes implement
        contents as a Python type with a valid __repr__.
        """
        return repr(self.contents)

    def __contains__(self, item):
        """ x in q' calls this method.
        Passes the containment check to self.contents. This requires that all
        child classes implement contents as a Python type with a valid
        __contains__.
        """
        return item in self.contents

class FIFO_Queue(_Queue):
    """First-in-first-out, also known as a classic 'queue', queue
    implementation.  The first call to get() returns the item from the
    first call to add(), the second returns the second, and so on.
    """
    def get(self):
        """Removes the oldest item from the queue and returns it."""
        return self.contents.popleft()

class LIFO_Queue(_Queue):
    """Last-in-first-out, also known as a 'stack', queue implementation.
    The first call to get() returns the item from the most recent call
    to add(), the second returns the next-most-recent, and so on.
    """
    def get(self):
        """Removes the newest item from the queue and returns it."""
        return self.contents.pop()

class Priority_Queue(_Queue):
    """Queue that orders items by prioirty.
    add() takes an additional argument: the item's priority.
    get() returns the item with the lowest priority.

    NOTE:   containment testing should generally not be used because
            it only works for (priority, item) pairs.
    """
    def __init__(self):
        self.contents = []

    def add(self, item, priority):
        heappush(self.contents, (priority, item))

    def get(self):
        """Removes the lowest-priority item from the queue and returns it."""
        return heappop(self.contents)[1]
