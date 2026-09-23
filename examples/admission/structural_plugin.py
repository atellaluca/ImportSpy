"""A statically described plugin with no top-level side effects."""

__version__ = "1.0"
MODE: str = "production"


def process(amount: int) -> str:
    return str(amount)


class Plugin:
    name: str = "payments"

    def run(self, request: str) -> str:
        return request
