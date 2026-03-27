"""Test suite for protocol implementations."""

import pytest
import asyncio
from propact.protocols import ShellProtocol, MCPProtocol, RESTProtocol, WebSocketProtocol
from propact.protocols.rest import HTTPMethod, RESTRequest, RESTResponse


class TestShellProtocol:
    """Test cases for ShellProtocol."""
    
    @pytest.mark.asyncio
    async def test_execute_simple_command(self):
        """Test executing a simple shell command."""
        protocol = ShellProtocol()
        result = await protocol.execute("echo 'test'")
        
        assert result["success"] is True
        assert result["returncode"] == 0
        assert "test" in result["stdout"]
        
    @pytest.mark.asyncio
    async def test_execute_failing_command(self):
        """Test executing a command that fails."""
        protocol = ShellProtocol()
        result = await protocol.execute("exit 1")
        
        assert result["success"] is False
        assert result["returncode"] == 1


class TestMCPProtocol:
    """Test cases for MCPProtocol."""
    
    def test_register_tool(self):
        """Test registering a tool."""
        protocol = MCPProtocol()
        protocol.register_tool(
            name="test_tool",
            description="A test tool",
            input_schema={"type": "object", "properties": {}}
        )
        
        assert len(protocol.tools) == 1
        assert protocol.tools[0]["name"] == "test_tool"
        
    def test_register_resource(self):
        """Test registering a resource."""
        protocol = MCPProtocol()
        protocol.register_resource(
            uri="test://resource",
            name="Test Resource",
            description="A test resource"
        )
        
        assert len(protocol.resources) == 1
        assert protocol.resources[0]["uri"] == "test://resource"
        
    @pytest.mark.asyncio
    async def test_execute_tool_not_implemented(self):
        """Test executing a tool (not implemented)."""
        protocol = MCPProtocol()
        result = await protocol.execute_tool("test_tool", {"arg": "value"})
        
        assert result["success"] is False
        assert "not implemented" in result["error"]


class TestRESTProtocol:
    """Test cases for RESTProtocol."""
    
    def test_rest_request_creation(self):
        """Test creating REST requests."""
        request = RESTRequest(
            method=HTTPMethod.GET,
            url="https://api.example.com/test",
            headers={"Content-Type": "application/json"}
        )
        
        assert request.method == HTTPMethod.GET
        assert request.url == "https://api.example.com/test"
        assert request.headers["Content-Type"] == "application/json"
        
    @pytest.mark.asyncio
    async def test_execute_get_request(self):
        """Test executing a GET request."""
        protocol = RESTProtocol()
        request = RESTRequest(
            method=HTTPMethod.GET,
            url="https://api.example.com/data"
        )
        
        response = await protocol.execute(request)
        
        assert isinstance(response, RESTResponse)
        assert response.status_code == 200
        assert response.success is True
        
    @pytest.mark.asyncio
    async def test_get_method(self):
        """Test GET method shortcut."""
        protocol = RESTProtocol()
        response = await protocol.get("https://api.example.com/data")
        
        assert response.status_code == 200
        assert response.success is True
        
    @pytest.mark.asyncio
    async def test_post_method(self):
        """Test POST method shortcut."""
        protocol = RESTProtocol()
        response = await protocol.post(
            "https://api.example.com/data",
            body={"key": "value"}
        )
        
        assert response.status_code == 200
        assert response.success is True


class TestWebSocketProtocol:
    """Test cases for WebSocketProtocol."""
    
    def test_websocket_creation(self):
        """Test creating WebSocket protocol."""
        protocol = WebSocketProtocol("ws://localhost:8080")
        
        assert protocol.url == "ws://localhost:8080"
        assert protocol.state.value == "closed"
        
    @pytest.mark.asyncio
    async def test_connect_disconnect(self):
        """Test WebSocket connect/disconnect cycle."""
        protocol = WebSocketProtocol("ws://localhost:8080")
        
        connect_result = await protocol.connect()
        assert connect_result["success"] is True
        assert protocol.state.value == "open"
        
        disconnect_result = await protocol.disconnect()
        assert disconnect_result["success"] is True
        assert protocol.state.value == "closed"
        
    @pytest.mark.asyncio
    async def test_send_message(self):
        """Test sending a message."""
        protocol = WebSocketProtocol("ws://localhost:8080")
        await protocol.connect()
        
        result = await protocol.send({"type": "test", "data": "hello"})
        assert result["success"] is True
        
    @pytest.mark.asyncio
    async def test_receive_message(self):
        """Test receiving a message."""
        protocol = WebSocketProtocol("ws://localhost:8080")
        await protocol.connect()
        
        message = await protocol.receive()
        assert message is not None
        assert message.type == "message"
