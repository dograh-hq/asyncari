"""WebSocket wrapper to add ping functionality to asyncwebsockets."""

from typing import Any
import logging
from wsproto.events import Ping, Pong

log = logging.getLogger(__name__)


class WebSocketWrapper:
    """Wrapper around asyncwebsockets WebSocket to add ping functionality."""
    
    def __init__(self, websocket):
        self._websocket = websocket
        
    async def ping(self, data: bytes = b"") -> None:
        """Send a real WebSocket ping frame.
        
        Args:
            data: Optional payload data for the ping frame
        """
        try:
            # Access the internal wsproto connection and socket
            if hasattr(self._websocket, '_connection') and hasattr(self._websocket, '_sock'):
                # Create a Ping event
                ping_event = Ping(payload=data)
                
                # Serialize the ping frame using wsproto
                frame_data = self._websocket._connection.send(event=ping_event)
                
                # Send the frame through the socket
                await self._websocket._sock.send(frame_data)
                
                log.debug(f"Sent WebSocket ping frame with {len(data)} bytes payload")
            else:
                log.warning("WebSocket doesn't have expected internal structure for sending ping")
                
        except Exception as e:
            log.error(f"Failed to send ping frame: {e}")
            
    async def pong(self, data: bytes = b"") -> None:
        """Send a WebSocket pong frame.
        
        Args:
            data: Optional payload data for the pong frame
        """
        try:
            # Access the internal wsproto connection and socket
            if hasattr(self._websocket, '_connection') and hasattr(self._websocket, '_sock'):
                # Create a Pong event
                pong_event = Pong(payload=data)
                
                # Serialize the pong frame using wsproto
                frame_data = self._websocket._connection.send(event=pong_event)
                
                # Send the frame through the socket
                await self._websocket._sock.send(frame_data)
                
                log.debug(f"Sent WebSocket pong frame with {len(data)} bytes payload")
            else:
                log.warning("WebSocket doesn't have expected internal structure for sending pong")
                
        except Exception as e:
            log.error(f"Failed to send pong frame: {e}")
            
    async def close(self, code: int = 1000, reason: str = "") -> None:
        """Close the WebSocket connection."""
        await self._websocket.close(code, reason)
        
    async def send(self, data: Any) -> None:
        """Send data through the WebSocket."""
        await self._websocket.send(data)
        
    async def send_text(self, data: str) -> None:
        """Send text data through the WebSocket."""
        if hasattr(self._websocket, 'send_text'):
            await self._websocket.send_text(data)
        else:
            await self._websocket.send(data)
            
    async def send_bytes(self, data: bytes) -> None:
        """Send binary data through the WebSocket."""
        if hasattr(self._websocket, 'send_bytes'):
            await self._websocket.send_bytes(data)
        else:
            await self._websocket.send(data)
            
    async def receive(self) -> Any:
        """Receive data from the WebSocket."""
        return await self._websocket.receive()
        
    def __aiter__(self):
        """Make the wrapper async iterable like the original WebSocket."""
        return self._websocket.__aiter__()
        
    async def __anext__(self):
        """Support async iteration."""
        return await self._websocket.__anext__()
        
    # Proxy all other attributes to the underlying WebSocket
    def __getattr__(self, name: str) -> Any:
        """Proxy attribute access to the underlying WebSocket."""
        return getattr(self._websocket, name)