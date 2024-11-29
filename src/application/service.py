class HelloWorldService:
    @staticmethod
    def get_message(path: str) -> str:
        return f"hello world from {path}"
