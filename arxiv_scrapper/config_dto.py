import json
from pathlib import Path


class ConfigDTO:
    """
    Type annotations for configurations
    """

    seed_urls: list[str]
    total_articles: int
    headers: dict[str, str]
    encoding: str
    timeout: int
    should_verify_certificate: bool
    headless_mode: bool

    def __init__(
            self,
            headers: dict[str, str],
            encoding: str,
            timeout: int,
            should_verify_certificate: bool
    ):
        """
        Initializes an instance of the ConfigDTO class
        """

        self.headers = headers
        self.encoding = encoding
        self.timeout = timeout
        self.should_verify_certificate = should_verify_certificate


class Config:
    """
    Unpacks and validates configurations
    """

    def __init__(self, path_to_config: Path) -> None:
        """
        Initializes an instance of the Config class
        """

        self.path_to_config = path_to_config
        config = self._extract_config_content()
        self._headers = config.headers
        self._encoding = config.encoding
        self._timeout = config.timeout
        self._should_verify_certificate = config.should_verify_certificate

    def _extract_config_content(self) -> ConfigDTO:
        """
        Returns config values
        """
        with open(self.path_to_config, encoding="utf-8") as file:
            config = json.load(file)

        return ConfigDTO(headers=config['headers'],
                         encoding=config['encoding'],
                         timeout=config['timeout'],
                         should_verify_certificate=config['should_verify_certificate'])

    def get_seed_urls(self) -> list[str]:
        """
        Retrieve seed urls
        """
        return self._seed_urls

    def get_num_articles(self) -> int:
        """
        Retrieve total number of articles to scrape
        """
        return self._num_articles

    def get_headers(self) -> dict[str, str]:
        """
        Retrieve headers to use during requesting
        """
        return self._headers

    def get_encoding(self) -> str:
        """
        Retrieve encoding to use during parsing
        """
        return str(self._encoding)

    def get_timeout(self) -> int:
        """
        Retrieve number of seconds to wait for response
        """
        return int(self._timeout)

    def get_verify_certificate(self) -> bool:
        """
        Retrieve whether to verify certificate
        """
        return bool(self._should_verify_certificate)

    def get_headless_mode(self) -> bool:
        """
        Retrieve whether to use headless mode
        """
        return bool(self._headless_mode)
