"""Protocol adapters for extended protocols in Propact."""

from typing import Dict, Any, Optional, Union
import asyncio
from pathlib import Path

# Import optional dependencies with graceful fallback
try:
    import grpc
    from grpc import aio as aio_grpc
    HAS_GRPC = True
except ImportError:
    HAS_GRPC = False

try:
    from gql import gql, Client
    from gql.transport.aiohttp import AIOHTTPTransport
    HAS_GQL = True
except ImportError:
    HAS_GQL = False

try:
    import paho.mqtt.client as mqtt
    HAS_MQTT = True
except ImportError:
    HAS_MQTT = False

try:
    from zeep import Client as ZeepClient
    from zeep.asyncio import AsyncClient
    HAS_ZEEP = True
except ImportError:
    HAS_ZEEP = False

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json


class BaseProtocolAdapter:
    """Base class for protocol adapters."""
    
    def __init__(self, endpoint: str, **kwargs):
        self.endpoint = endpoint
        self.config = kwargs
        
    async def send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send payload through the protocol."""
        raise NotImplementedError
    
    def is_available(self) -> bool:
        """Check if required dependencies are available."""
        return True


class GRPCAdapter(BaseProtocolAdapter):
    """Adapter for gRPC protocol."""
    
    def __init__(self, endpoint: str, **kwargs):
        super().__init__(endpoint, **kwargs)
        self.proto_file = kwargs.get('proto_file')
        self.service = kwargs.get('service')
        self.method = kwargs.get('method')
        
    def is_available(self) -> bool:
        return HAS_GRPC
    
    async def send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send gRPC request."""
        if not HAS_GRPC:
            return {"error": "gRPC dependencies not installed. Install with: pip install propact[grpc]"}
        
        try:
            # Parse endpoint (format: grpc://host:port/service/method)
            parts = self.endpoint.replace('grpc://', '').split('/')
            if len(parts) < 3:
                return {"error": "Invalid gRPC endpoint format. Use: grpc://host:port/service/method"}
            
            host_port = parts[0]
            service = parts[1] if not self.service else self.service
            method = parts[2] if not self.method else self.method
            
            # Create channel
            channel = aio_grpc.insecure_channel(host_port)
            
            # Load proto (simplified - in production, use generated stubs)
            # This is a placeholder for actual gRPC implementation
            stub = channel  # Replace with actual stub
            
            # Prepare request message
            request_data = payload.get('data', {})
            
            # Call method (placeholder)
            response = await stub[method](request_data)
            
            await channel.close()
            
            return {
                "success": True,
                "response": str(response),
                "metadata": {"service": service, "method": method}
            }
            
        except Exception as e:
            return {"error": f"gRPC request failed: {str(e)}"}


class GraphQLAdapter(BaseProtocolAdapter):
    """Adapter for GraphQL protocol."""
    
    def is_available(self) -> bool:
        return HAS_GQL
    
    async def send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send GraphQL request."""
        if not HAS_GQL:
            return {"error": "GraphQL dependencies not installed. Install with: pip install propact[graphql]"}
        
        try:
            # Parse endpoint (format: gql://host:port/graphql or just https://host/graphql)
            endpoint = self.endpoint.replace('gql://', 'https://') if self.endpoint.startswith('gql://') else self.endpoint
            
            # Create transport and client
            transport = AIOHTTPTransport(url=endpoint)
            client = Client(transport=transport, fetch_schema_from_transport=True)
            
            # Extract query and variables from payload
            data = payload.get('data', {})
            query = data.get('query', data.get('graphql', ''))
            variables = data.get('variables', {})
            
            if not query:
                return {"error": "No GraphQL query found in payload"}
            
            # Execute query
            result = await client.execute(gql(query), variable_values=variables)
            
            return {
                "success": True,
                "data": result,
                "metadata": {"endpoint": endpoint}
            }
            
        except Exception as e:
            return {"error": f"GraphQL request failed: {str(e)}"}


class MQTTAdapter(BaseProtocolAdapter):
    """Adapter for MQTT protocol."""
    
    def __init__(self, endpoint: str, **kwargs):
        super().__init__(endpoint, **kwargs)
        self.client_id = kwargs.get('client_id', 'propact_client')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.qos = kwargs.get('qos', 1)
        
    def is_available(self) -> bool:
        return HAS_MQTT
    
    async def send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send MQTT message."""
        if not HAS_MQTT:
            return {"error": "MQTT dependencies not installed. Install with: pip install propact[mqtt]"}
        
        try:
            # Parse endpoint (format: mqtt://host:port/topic)
            parts = self.endpoint.replace('mqtt://', '').split('/', 1)
            host_port = parts[0]
            topic = parts[1] if len(parts) > 1 else 'propact/default'
            
            host, port = host_port.split(':') if ':' in host_port else (host_port, 1883)
            
            # Create client
            client = mqtt.Client(client_id=self.client_id)
            
            # Set credentials if provided
            if self.username and self.password:
                client.username_pw_set(self.username, self.password)
            
            # Connect
            client.connect(host, int(port), 60)
            
            # Prepare message
            message_data = {
                "text": payload.get('text', ''),
                "data": payload.get('data', {}),
                "timestamp": payload.get('timestamp', '')
            }
            
            message = json.dumps(message_data)
            
            # Publish
            result = client.publish(topic, message, qos=self.qos)
            
            # Wait for publish
            result.wait_for_publish()
            
            client.disconnect()
            
            return {
                "success": True,
                "message_id": result.mid,
                "metadata": {"topic": topic, "qos": self.qos}
            }
            
        except Exception as e:
            return {"error": f"MQTT publish failed: {str(e)}"}


class SOAPAdapter(BaseProtocolAdapter):
    """Adapter for SOAP protocol."""
    
    def __init__(self, endpoint: str, **kwargs):
        super().__init__(endpoint, **kwargs)
        self.wsdl = kwargs.get('wsdl', endpoint)
        
    def is_available(self) -> bool:
        return HAS_ZEEP
    
    async def send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send SOAP request."""
        if not HAS_ZEEP:
            return {"error": "SOAP dependencies not installed. Install with: pip install propact[soap]"}
        
        try:
            # Create async client
            async with AsyncClient(self.wsdl) as client:
                # Extract service and operation from payload
                data = payload.get('data', {})
                service_name = data.get('service')
                operation = data.get('operation')
                
                if not operation:
                    return {"error": "No SOAP operation specified in payload"}
                
                # Get service
                service = client.service if not service_name else getattr(client.service, service_name)
                
                # Get operation
                operation_func = getattr(service, operation)
                
                # Prepare parameters
                params = data.get('params', {})
                
                # Call operation
                result = await operation_func(**params)
                
                # Convert result to dict (Zeep objects are complex)
                if hasattr(result, '__dict__'):
                    result_dict = result.__dict__
                else:
                    result_dict = {"result": str(result)}
                
                return {
                    "success": True,
                    "data": result_dict,
                    "metadata": {"service": service_name, "operation": operation}
                }
                
        except Exception as e:
            return {"error": f"SOAP request failed: {str(e)}"}


class EmailAdapter(BaseProtocolAdapter):
    """Adapter for Email protocol."""
    
    def __init__(self, endpoint: str, **kwargs):
        super().__init__(endpoint, **kwargs)
        self.smtp_server = kwargs.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = kwargs.get('smtp_port', 587)
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.from_email = kwargs.get('from_email')
        self.to_email = kwargs.get('to_email')
        
    async def send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send email."""
        try:
            # Parse endpoint for email addresses (format: smtp://user:pass@server?to=recipient@example.com)
            if self.endpoint.startswith('smtp://'):
                # Parse SMTP URL
                import urllib.parse
                parsed = urllib.parse.urlparse(self.endpoint)
                self.smtp_server = parsed.hostname
                self.smtp_port = parsed.port or 587
                self.username = parsed.username
                self.password = parsed.password
                query = urllib.parse.parse_qs(parsed.query)
                self.to_email = query.get('to', [None])[0]
            
            if not self.to_email:
                return {"error": "No recipient email specified"}
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email or self.username
            msg['To'] = self.to_email
            msg['Subject'] = payload.get('data', {}).get('subject', 'Message from Propact')
            
            # Add text body
            text_content = payload.get('text', '')
            if text_content:
                msg.attach(MIMEText(text_content, 'plain'))
            
            # Add HTML content if present
            if 'html' in payload.get('data', {}):
                html_content = payload['data']['html']
                msg.attach(MIMEText(html_content, 'html'))
            
            # Add attachments
            for filename, file_data in payload.get('files', {}).items():
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file_data)
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}'
                )
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            if self.username and self.password:
                server.login(self.username, self.password)
            
            text = msg.as_string()
            server.sendmail(self.from_email or self.username, self.to_email, text)
            server.quit()
            
            return {
                "success": True,
                "message": "Email sent successfully",
                "metadata": {"to": self.to_email, "from": self.from_email or self.username}
            }
            
        except Exception as e:
            return {"error": f"Email send failed: {str(e)}"}


# Protocol adapter registry
PROTOCOL_ADAPTERS = {
    'grpc': GRPCAdapter,
    'gql': GraphQLAdapter,
    'graphql': GraphQLAdapter,
    'mqtt': MQTTAdapter,
    'soap': SOAPAdapter,
    'smtp': EmailAdapter,
    'email': EmailAdapter,
}


def get_protocol_adapter(protocol: str, endpoint: str, **kwargs) -> BaseProtocolAdapter:
    """Get appropriate protocol adapter."""
    adapter_class = PROTOCOL_ADAPTERS.get(protocol.lower())
    if not adapter_class:
        raise ValueError(f"Unsupported protocol: {protocol}")
    
    return adapter_class(endpoint, **kwargs)
