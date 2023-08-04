from prefect import Flow, Task
from listeners import BaseSQSListener
import boto3


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
    def run(self, listener):
        listener.join()  # Or however you decide to implement stopping the listener

@Flow
def StartListeners():
    listeners = []
    Queues = GetQueueUrlTask().run()
    QueueNames = [queue_url.split("/")[-1] for queue_url in Queues]
    print(QueueNames)
    for ListenerClass in BaseSQSListener.__subclasses__():
        # Each ListenerClass should be named after the queue it listens to
        # in the format <QueueName>Listener
        if ListenerClass.__name__[:-8] not in QueueNames:
            raise ValueError(f"ListenerClass {ListenerClass.__name__} does not have a corresponding queue")
        listener = ListenerClass(queue_url=Queues[QueueNames.index(ListenerClass.__name__[:-8])])
        StartListenersTask(listener=listener).run()
        listeners.append(listener)
    return listeners

if __name__ == "__main__":
    listeners = StartListeners()