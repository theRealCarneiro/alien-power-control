from g15pc import settings


def send_message(conn, msg) -> None:
    '''
    Send a message to a specific client
    '''

    msg = msg.encode('utf-8')
    msg_len = msg_len_to_str(len(msg))
    conn.sendall(msg_len)
    conn.sendall(msg)


def get_message_len(conn) -> int:
    '''
    Recives a connection, and returns the message length
    '''
    msg_len = conn.recv(settings.REQUEST_SIZE_LEN)
    if not msg_len:
        raise ValueError('Invalid message length')
    msg_len = int(msg_len.decode())
    return msg_len


def get_message(conn) -> str:
    '''
    Recives a connection, and returns a single massage
    '''

    msg_len = get_message_len(conn)
    msg = conn.recv(msg_len)
    if not msg:
        raise ValueError('Invalid message data')

    return msg.decode('utf-8')


def msg_len_to_str(msg_len: int) -> str:
    return str.encode(str(msg_len).zfill(settings.REQUEST_SIZE_LEN))
