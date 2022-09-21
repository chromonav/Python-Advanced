# Partial solution to above assignment. Added a Queue object which is filled by main program and drained by server.
# Server finishes draining Queue before exiting.

from threading import Thread, Event
import time
import random
from queue import Queue

work_queue = Queue()

class DatabaseServer(Thread):
    def __init__(self):
        super().__init__()
        self.done = Event()
        
    def set_done(self):
        self.done.set()
        # Print message so we know it was received. We won't shut down
        # right away if request remain in Queue.
        print('Database server asked to shut down.')
        
    def run(self):
        """Keep processing requests as long as we weren't told to quit or
           there are requests still in Queue. About 25% of the time we'll
           punt on a request and re-insert it into the Queue.
        """
        while not self.done.is_set() or work_queue.qsize():
            print(f'Queue: {list(work_queue.queue)}')
            secs = work_queue.get()
            if random.random() > 0.75:
                print(f'WARNING: server unable to handle request {secs}...requeuing')
                work_queue.put(secs)
                continue
            print(f'Database server handling request for {secs} seconds')
            time.sleep(secs)
            print('Database server successfully handled request')
        
        print('Database server shutting down.')
        
server = DatabaseServer() # create the thread object
server.start() # start the thread

while True:
    text = input('Enter integer: ')
    if text == 'quit':
        server.set_done()
        break
    print('Enqueueing:', text)
    # Handle case where user does not enter an int. Queue up a
    # random integer rather than the non-int entered by user.
    try:
        seconds = int(text)
    except ValueError:
        seconds = random.randint(10, 15)
        print(f'Invalid integer ({text}), adding {seconds} instead')
    work_queue.put(seconds) # Add request to queue
