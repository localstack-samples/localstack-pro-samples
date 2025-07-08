def handler(event, context):
    """Lambda handler that will get invoked by the LocalStack runtime"""

    # Print the incoming invocation event.
    print(event)

    # Return the incoming invocation event.
    return event


def wait_for_debug_client(port: int=19891, timeout: int=3600):
    """Utility function to enable debugging with Visual Studio Code"""

    import time, threading
    import sys, glob
    sys.path.append(glob.glob(".venv/lib/python*/site-packages")[0])
    import debugpy

    if not hasattr(wait_for_debug_client, "_debugpy_listening"):
        wait_for_debug_client._debugpy_listening = False

    if not wait_for_debug_client._debugpy_listening:
        try:
            debugpy.listen(("0.0.0.0", port))
            wait_for_debug_client._debugpy_listening = True
            print(f"debugpy is now listening on port {port}")
        except RuntimeError as e:
            print(f"debugpy.listen() failed or already active: {e}")

    if not debugpy.is_client_connected():
        print("Waiting for client to attach debugger...")

        def cancel_wait():
            time.sleep(timeout)
            print("Canceling debug wait task after timeout...")
            debugpy.wait_for_client.cancel()

        threading.Thread(target=cancel_wait, daemon=True).start()
        debugpy.wait_for_client()
    else:
        print("Debugger already attached.")

wait_for_debug_client()
