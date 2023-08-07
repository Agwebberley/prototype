from prefect import Flow, Task
from Listeners.listeners import BaseSQSListener
import boto3
import multiprocessing
import sqlite3

@Task
class CreateQueueDatabase():
    def run(self):
        conn = sqlite3.connect("queue.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS queues (topic text, listeningto text)")
        # If the table did exist, empty it
        c.execute("DELETE FROM queues")
        conn.commit()
        conn.close()

@Task
class GetQueueUrlTask():
    def run(self):
        Queues = boto3.client("sqs").list_queues()
        return Queues["QueueUrls"]

@Task
class StartListenerTask():
    def run(self, listener):
        listener.start()
@Task
class StopListenerTask():
    def run(self):
        for process in multiprocessing.active_children():
            process.stop()

@Flow
def Listeners(Stop=False):
    # Create the database if it doesn't exist
    CreateQueueDatabase().run()
    if Stop:
        # If the flow has already been run, stop the listeners
        StopListenerTask().run()
        return
    listeners = []
    Queues = GetQueueUrlTask().run()
    QueueNames = [queue_url.split("/")[-1] for queue_url in Queues]
    num_classes = 0
    for ListenerClass in BaseSQSListener.__subclasses__(): 
        if ListenerClass.__name__[:-8] in QueueNames: num_classes + 1
    # Create a barrier to wait for all listeners to be created
    barrier = multiprocessing.Barrier(num_classes)
    for ListenerClass in BaseSQSListener.__subclasses__():
        # Each ListenerClass should be named after the queue it listens to
        # in the format <QueueName>Listener
        if ListenerClass.__name__[:-8] not in QueueNames:
            print(f"ListenerClass {ListenerClass.__name__} does not have a corresponding queue")
            continue
            #raise ValueError(f"ListenerClass {ListenerClass.__name__} does not have a corresponding queue")
        listener = ListenerClass(queue_url=Queues[QueueNames.index(ListenerClass.__name__[:-8])], barrier=barrier)
        StartListenerTask().run(listener=listener)
        listeners.append(listener)
    return listeners

if __name__ == "__main__":
    listeners = Listeners()
    # Join the listeners to the main process
    for listener in listeners:
        listener.join()
    # Listeners(Stop=True)