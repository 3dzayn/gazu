from gazu.exception import AuthFailedException


def init():
    """
    Init configuration for SocketIO client.

    Returns:
        Event client that will be able to set listeners.
    """
    from socketIO_client import SocketIO, BaseNamespace
    from . import get_event_host
    from gazu.client import make_auth_header

    path = get_event_host()
    socketIO = SocketIO(path, None, headers=make_auth_header())
    main_namespace = socketIO.define(BaseNamespace, "/events")
    socketIO.main_namespace = main_namespace
    socketIO.on('error', connect_error)
    return socketIO


def connect_error(data):
    print("The connection failed!")
    return data


def add_listener(event_client, event_name, event_handler):
    """
    Set a listener that reacts to a given event.
    """
    event_client.main_namespace.on(event_name, event_handler)
    return event_client


def run_client(event_client):
    """
    Run event client (it blocks current thread). It listens to all events
    configured.
    """
    try:
        event_client.wait()
    except TypeError:
        raise AuthFailedException
    return event_client