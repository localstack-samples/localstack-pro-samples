
def handler(event, context):
    """Lambda handler that will get invoked by the LocalStack runtime"""

    # wait for the debugger to get attached
    wait_for_debug_client()
    # print the incoming invocation event
    print(event)


def wait_for_debug_client(timeout=15):
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
