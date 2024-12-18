def handler(event, context):
    """Lambda handler that will get invoked by the LocalStack runtime"""

    # Wait for the debugger to get attached.
    wait_for_debug_client()

    # Print a message to log that this the handler of handler_function_one.py file.
    print("The handler of handler_function_one.py is evaluating.")

    # Print the incoming invocation event.
    print(event)

    # Return the incoming invocation event.
    return event


def wait_for_debug_client(timeout=3600):
    """Utility function to enable debugging with Visual Studio Code"""
    import time, threading
    import sys, glob
    sys.path.append(glob.glob(".venv/lib/python*/site-packages")[0])
    import debugpy

    debugpy.listen(("0.0.0.0", 19891))
    class T(threading.Thread):
        daemon = True
        def run(self):
            time.sleep(timeout)
            print("Canceling debug wait task ...")
            debugpy.wait_for_client.cancel()
    T().start()
    print("Waiting for client to attach debugger ...")
    debugpy.wait_for_client()


if __name__ == "__main__":
    handler({}, {})

