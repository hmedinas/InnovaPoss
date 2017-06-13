import socket
import logging
import uuid
from _thread import start_new_thread
from time import sleep
from typing import Callable, Any


class TCPDataAdapter():
    def __init__(self):
        """
        TCPDataAdapter constructor
        
        """
        self.read_stop_byte = str.encode('/n')
        self.sock: socket.socket = None
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Adapter instantiated")
        self.incoming_msg_handler: Callable[[Any, str], str] = None
        self._is_opened_ = False

    def open(self) -> None:
        """
        Initializes a new connection

        :return: None
        :rtype: None
        """
        self.logger.debug("Opening connection")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", 3000))
        self.sock.settimeout(1)
        self.logger.debug("Connection opened")
        self._is_opened_ = True

    def bind_and_setup_listening(self):
        """
        Binds the passed port for new connections
        
        :return: None
        :rtype: None
        """
        self.logger.debug("Binding port")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("localhost", 3001))
        self.logger.debug("Port binding done")
        self.sock.listen()
        start_new_thread(self.accept_new_connections_loop, ())
        self.logger.debug("Port bound and listener started")

    def set_message_handler(self, handler: Callable[[Any, str], str]):
        """
        Sets the handler function for messages received on the listened port
        
        :param handler: handler function for incoming messages on bound port. only required if you will be \
            listening on that specific port in order to be able to notify whoever it may interest. 
            
            The handler function may return a value. That value will be used to reply to the received message. \
            If the returned value is None, no message will be sent
        :type handler: Callable[[Any, str], str]
        :return: 
        :rtype: 
        """
        self.incoming_msg_handler = handler

    def send_message(self, message: str):
        self.logger.debug(f"Sending message '{message}'")
        self.sock.send(str.encode(f'{message}\n'))

    def receive_message_with_stop_byte(self) -> str:
        """
        Reads a message from the TCP stream until it encounters the stop byte
        :return: read message 
        :rtype: str
        """
        self.logger.debug(f"Starting to read reply")
        reply = self.__read_until_stop_byte_or_timeout__(self.sock)
        self.logger.debug(f"Reply length - {len(reply)}. Reply - '{reply}'")
        return reply

    def transact_message(self, message: str) -> str:
        """
        Sends a message and receives an answer until stopbyte is received
        :param message: message to send
        :type message: str
        :return: received answer
        :rtype: str
        """
        self.logger.debug(f"Transacting message {message}")
        self.send_message(message)
        sleep(1)
        reply = self.receive_message_with_stop_byte()
        return reply

    def accept_new_connections_loop(self):
        while self._is_opened_:
            conn, address = self.sock.accept()
            self.logger.debug(f"Accepted a new connection on {address}. Starting handler thread")
            start_new_thread(self.handle_client_messages_loop, (conn, address))

    def handle_client_messages_loop(self, connection, address):
        while self._is_opened_:
            result = self.__read_until_stop_byte_or_timeout__(connection)
            if result and self.incoming_msg_handler is not None:
                # self.logger.debug(f"New message on port {address}: {result} ")
                reply_to_send = self.incoming_msg_handler(result)
                if reply_to_send:
                    self.logger.debug(f"Callback returned {reply_to_send}. Replying")
                    connection.send(str.encode(reply_to_send))
            else:
                sleep(0.5)

    def close(self) -> None:
        self._is_opened_ = False
        if self.sock is not None:
            self.sock.close()
        self.sock = None

    def __read_until_stop_byte_or_timeout__(self, connection: socket.socket) -> str:
        """
        Reads the TCP stream until the end char is met
        :return: full response
        :rtype: str
        """
        result: str = ""
        while True:
            try:
                current_char = connection.recv(1)
                if current_char == self.read_stop_byte: # /n /r
                    break
                result += bytes.decode(current_char)
            except TimeoutError:
                break
            except OSError:
                break
        return result

