import queue
from datetime import datetime

# Thread-safe queue for logs
log_queue = queue.Queue()

def send_log(agent: str, message: str, level: str = "info"):
    """
    Add a log message to the queue.
    This is called by agents running in a separate thread.
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "message": message,
        "level": level
    }
    log_queue.put(log_entry)
