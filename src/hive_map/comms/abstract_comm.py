# -*- coding: utf-8 -*-

# external modules
from abc import ABC, abstractmethod
import asyncio

class AbstractComm(ABC):
    """
    The base class that represents the over arching behavior of all
    communication lines. A communication line recieves HiveMsgs and puts them
    on a buffer until get_msgs dumps them (this is done with hive_map). These
    communication lines can also send messages

    Attributes:
        msg_queue([str]): queue of messages recieved after last get_msgs
        lock(asyncio.Lock): used when modifiying the message_queue
    """

    def __init__(self):
        self.msg_queue = []
        self.lock = asyncio.Lock()

    async def get_msgs(self):
        """
        Handles the retrival of messages from the message_queue, once data is
        extracted, the message queue is wiped (hence the lock)

        Returns:
            [str]: bytes of the message queue
        """
        async with self.lock:
            msgs = self.msg_queue
            # clears the queue, that's why lock is needed
            self.msg_queue = []
        return msgs

    async def add_msg(self, msg:str):
        """
        Atomic method that adds messages to the message queue

        Args:
            msg(str): bytes of the message being added
        """
        async with self.lock:
            self.msg_queue.append(msg)

    @abstractmethod
    async def listen(self):
        """
        Listens for information to recieve and adds it to the message_queue
        """
        pass

    @abstractmethod
    async def publish(self, msg):
        """
        Publishes information based on message

        Args:
            msg(HiveMsg): Hive message that is being sent out
        """
        pass
