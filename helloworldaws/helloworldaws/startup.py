from CRUD.listener import SQSListener, LogListener
import threading

def thread_listeners():
    print('Starting SQS listeners...')
    LogListenerUrl = 'https://sqs.us-west-2.amazonaws.com/710141730058/CustomerLog'
    
    LogListenerTask = LogListener(LogListenerUrl)

    LogListenerTask.start()


t = threading.Thread(target=thread_listeners)
t.daemon = True
t.start()