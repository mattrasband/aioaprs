import asyncio
import dataclasses
import logging
from typing import Any, Dict, List, Optional

import aprslib

from .filters import Filter

logger = logging.getLogger(__name__)


DELIMITER = b"\r\n"


@dataclasses.dataclass
class Client:
    """
    Read-only APRS client, this must be used as a context manager to
    ensure resources are set up and cleaned up properly.

    >>> async with Client("KD0VTE") as client:
    >>>     # this will be a logged in client
    >>>     async for packet in client:
    >>>         print(packet)
    """
    call: str
    filters: Optional[List[Filter]] = dataclasses.field(default_factory=list)
    host: str = "rotate.aprs2.net"
    port: int = 14580

    _reader: asyncio.StreamReader = dataclasses.field(init=False, default=None)
    _writer: asyncio.StreamWriter = dataclasses.field(init=False, default=None)

    async def _connect(self):
        if self._reader is None or self._writer is None:
            logger.debug("Not connected, establishing a new connection")
            self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
            await self._login()

    async def _login(self) -> None:
        """
        Perform the login routine. This must only be called by _connect, as
        it assumes a fresh connection in which the server is expecting a command.
        """
        logger.debug("Logging in as %s", self.call)

        server_hello = await self._readline()
        if server_hello.startswith(b"# aprsc "):
            auth_str = f"user {self.call} pass -1"
            if self.filters:
                auth_str += " filter " + " ".join((str(x) for x in self.filters))
            await self._writeline(auth_str)
        else:
            raise ValueError(f"Server did not greet! {server_hello}")

        result = await self._readline()
        if not result.startswith(f"# logresp {self.call} unverified".encode()):
            raise ValueError(f"Read-only login not confirmed: {result}")

    async def _readline(self) -> bytes:
        """
        Read a line from the connection, returning the raw response minus
        the terminating bytes (\r\n)
        """
        return (await self._reader.readuntil(DELIMITER)).strip()

    async def _writeline(self, line: str) -> None:
        """
        Write a line to the connection, automatically encoding the line
        and appending the terminating bytes (\r\n)
        :param line: Line to write
        """
        self._writer.write(line.encode() + DELIMITER)
        await self._writer.drain()

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, *args, **kwargs):
        self._writer.close()
        self._reader = self._writer = None

    async def __aiter__(self):
        while not self._reader.at_eof():
            message = (await self._reader.readuntil(DELIMITER)).strip()

            if message.startswith(b"# aprsc "):  # server message
                logger.debug("Server message: %r", message)
            else:
                yield self.parse(message)

    def parse(self, message: bytes) -> Dict[str, Any]:
        try:
            return aprslib.parse(message)
        except aprslib.exceptions.UnknownFormat:
            logger.error("Unknown format: %s", message)
