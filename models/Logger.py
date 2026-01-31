class Logger:
    RESET = "\033[0m"

    COLORS = {
        "INFO": "\033[94m",     # Azul
        "SUCCESS": "\033[92m",  # Verde
        "WARNING": "\033[93m",  # Amarelo
        "ERROR": "\033[91m",    # Vermelho
        "DEBUG": "\033[90m",    # Cinza
    }

    @classmethod
    def _log(cls, level: str, message: str):
        color = cls.COLORS.get(level, "")
        print(f"{color}[{level}] {message}{cls.RESET}")

    @classmethod
    def info(cls, message: str):
        cls._log("INFO", message)

    @classmethod
    def success(cls, message: str):
        cls._log("SUCCESS", message)

    @classmethod
    def warning(cls, message: str):
        cls._log("WARNING", message)

    @classmethod
    def error(cls, message: str):
        cls._log("ERROR", message)

    @classmethod
    def debug(cls, message: str):
        cls._log("DEBUG", message)
