"""Configuration management for propact."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False


@dataclass
class OpenAIConfig:
    """OpenAI API configuration."""
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4-vision-preview"
    max_tokens: int = 500
    temperature: float = 0.2


@dataclass
class GRPCConfig:
    """gRPC configuration."""
    host: str = "localhost"
    port: int = 50051
    timeout: int = 30
    insecure: bool = True


@dataclass
class MQTTConfig:
    """MQTT configuration."""
    host: str = "localhost"
    port: int = 1883
    username: str = ""
    password: str = ""
    client_id: str = "propact_client"
    keepalive: int = 60
    qos: int = 1


@dataclass
class SMTPConfig:
    """SMTP configuration for email."""
    host: str = "smtp.gmail.com"
    port: int = 587
    username: str = ""
    password: str = ""
    from_email: str = "propact@example.com"
    use_tls: bool = True


@dataclass
class WebSocketConfig:
    """WebSocket configuration."""
    host: str = "localhost"
    port: int = 8080
    path: str = "/"
    timeout: int = 60


@dataclass
class ServerConfig:
    """Server configuration."""
    host: str = "0.0.0.0"
    port: int = 8080
    workers: int = 1
    reload: bool = False


@dataclass
class MCPConfig:
    """MCP configuration."""
    host: str = "localhost"
    port: int = 8080
    path: str = "/mcp"


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None


@dataclass
class PathConfig:
    """Path configuration."""
    data_dir: Path = field(default_factory=lambda: Path("./data"))
    cache_dir: Path = field(default_factory=lambda: Path("./cache"))
    temp_dir: Path = field(default_factory=lambda: Path("./temp"))


@dataclass
class SecurityConfig:
    """Security configuration."""
    cors_origins: str = "*"
    api_key: str = ""
    jwt_secret: str = ""
    rate_limit_requests: int = 100
    rate_limit_window: int = 60


@dataclass
class Config:
    """Main configuration class."""
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    grpc: GRPCConfig = field(default_factory=GRPCConfig)
    mqtt: MQTTConfig = field(default_factory=MQTTConfig)
    smtp: SMTPConfig = field(default_factory=SMTPConfig)
    websocket: WebSocketConfig = field(default_factory=WebSocketConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    mcp: MCPConfig = field(default_factory=MCPConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    debug: bool = False
    test_mode: bool = False
    request_timeout: int = 30


class ConfigManager:
    """Manages configuration loading and access."""
    
    def __init__(self, env_file: Optional[Path] = None):
        """Initialize configuration manager.
        
        Args:
            env_file: Path to .env file (auto-detects if None)
        """
        self._config: Optional[Config] = None
        self._env_file = env_file or self._find_env_file()
        self._load_env()
    
    def _find_env_file(self) -> Optional[Path]:
        """Find .env file in project directory."""
        current = Path.cwd()
        
        # Look for .env in current and parent directories
        while current != current.parent:
            env_file = current / ".env"
            if env_file.exists():
                return env_file
            current = current.parent
        
        return None
    
    def _load_env(self) -> None:
        """Load environment variables from .env file."""
        if HAS_DOTENV and self._env_file:
            load_dotenv(self._env_file)
    
    def _get_env_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean value from environment."""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def _get_env_int(self, key: str, default: int) -> int:
        """Get integer value from environment."""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            return default
    
    def _get_env_path(self, key: str, default: str) -> Path:
        """Get Path value from environment."""
        return Path(os.getenv(key, default))
    
    @property
    def config(self) -> Config:
        """Get configuration (lazy-loaded)."""
        if self._config is None:
            self._config = self._load_config()
        return self._config
    
    def _load_config(self) -> Config:
        """Load configuration from environment variables."""
        # OpenAI Config
        openai = OpenAIConfig(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            model=os.getenv("OPENAI_MODEL", "gpt-4-vision-preview"),
            max_tokens=self._get_env_int("OPENAI_MAX_TOKENS", 500),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.2"))
        )
        
        # gRPC Config
        grpc = GRPCConfig(
            host=os.getenv("GRPC_HOST", "localhost"),
            port=self._get_env_int("GRPC_PORT", 50051),
            timeout=self._get_env_int("GRPC_TIMEOUT", 30),
            insecure=self._get_env_bool("GRPC_INSECURE", True)
        )
        
        # MQTT Config
        mqtt = MQTTConfig(
            host=os.getenv("MQTT_HOST", "localhost"),
            port=self._get_env_int("MQTT_PORT", 1883),
            username=os.getenv("MQTT_USERNAME", ""),
            password=os.getenv("MQTT_PASSWORD", ""),
            client_id=os.getenv("MQTT_CLIENT_ID", "propact_client"),
            keepalive=self._get_env_int("MQTT_KEEPALIVE", 60),
            qos=self._get_env_int("MQTT_QOS", 1)
        )
        
        # SMTP Config
        smtp = SMTPConfig(
            host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
            port=self._get_env_int("SMTP_PORT", 587),
            username=os.getenv("SMTP_USERNAME", ""),
            password=os.getenv("SMTP_PASSWORD", ""),
            from_email=os.getenv("SMTP_FROM", "propact@example.com"),
            use_tls=self._get_env_bool("SMTP_USE_TLS", True)
        )
        
        # WebSocket Config
        websocket = WebSocketConfig(
            host=os.getenv("WS_HOST", "localhost"),
            port=self._get_env_int("WS_PORT", 8080),
            path=os.getenv("WS_PATH", "/"),
            timeout=self._get_env_int("WEBSOCKET_TIMEOUT", 60)
        )
        
        # Server Config
        server = ServerConfig(
            host=os.getenv("SERVER_HOST", "0.0.0.0"),
            port=self._get_env_int("SERVER_PORT", 8080),
            workers=self._get_env_int("SERVER_WORKERS", 1),
            reload=self._get_env_bool("SERVER_RELOAD", False)
        )
        
        # MCP Config
        mcp = MCPConfig(
            host=os.getenv("MCP_HOST", "localhost"),
            port=self._get_env_int("MCP_PORT", 8080),
            path=os.getenv("MCP_PATH", "/mcp")
        )
        
        # Logging Config
        logging = LoggingConfig(
            level=os.getenv("LOG_LEVEL", "INFO"),
            format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            file=os.getenv("LOG_FILE")
        )
        
        # Path Config
        paths = PathConfig(
            data_dir=self._get_env_path("DATA_DIR", "./data"),
            cache_dir=self._get_env_path("CACHE_DIR", "./cache"),
            temp_dir=self._get_env_path("TEMP_DIR", "./temp")
        )
        
        # Security Config
        security = SecurityConfig(
            cors_origins=os.getenv("CORS_ORIGINS", "*"),
            api_key=os.getenv("API_KEY", ""),
            jwt_secret=os.getenv("JWT_SECRET", ""),
            rate_limit_requests=self._get_env_int("RATE_LIMIT_REQUESTS", 100),
            rate_limit_window=self._get_env_int("RATE_LIMIT_WINDOW", 60)
        )
        
        # Main Config
        return Config(
            openai=openai,
            grpc=grpc,
            mqtt=mqtt,
            smtp=smtp,
            websocket=websocket,
            server=server,
            mcp=mcp,
            logging=logging,
            paths=paths,
            security=security,
            debug=self._get_env_bool("DEBUG", False),
            test_mode=self._get_env_bool("TEST_MODE", False),
            request_timeout=self._get_env_int("REQUEST_TIMEOUT", 30)
        )
    
    def reload(self) -> None:
        """Reload configuration from environment."""
        self._config = None
        self._load_env()


# Global configuration manager instance
_config_manager: Optional[ConfigManager] = None


def get_config() -> Config:
    """Get global configuration."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager.config


def init_config(env_file: Optional[Path] = None) -> Config:
    """Initialize configuration with custom env file."""
    global _config_manager
    _config_manager = ConfigManager(env_file)
    return _config_manager.config


def reload_config() -> None:
    """Reload global configuration."""
    global _config_manager
    if _config_manager:
        _config_manager.reload()


# Convenience functions for common config access
def get_openai_config() -> OpenAIConfig:
    """Get OpenAI configuration."""
    return get_config().openai


def get_grpc_config() -> GRPCConfig:
    """Get gRPC configuration."""
    return get_config().grpc


def get_mqtt_config() -> MQTTConfig:
    """Get MQTT configuration."""
    return get_config().mqtt


def get_smtp_config() -> SMTPConfig:
    """Get SMTP configuration."""
    return get_config().smtp


def get_websocket_config() -> WebSocketConfig:
    """Get WebSocket configuration."""
    return get_config().websocket


def get_server_config() -> ServerConfig:
    """Get server configuration."""
    return get_config().server


def is_debug() -> bool:
    """Check if debug mode is enabled."""
    return get_config().debug


def is_test_mode() -> bool:
    """Check if test mode is enabled."""
    return get_config().test_mode
