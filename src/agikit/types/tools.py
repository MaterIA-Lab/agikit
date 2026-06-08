from typing import Callable
from typing import TypedDict
from typing import Optional


class ToolMetadata(TypedDict):
    name: str
    display_name: str
    description: str
    categories: list[str]
    uses_icon: bool = False
    icon_url: Optional[str]


def tool(metadata: ToolMetadata):
    def decorator(func: Callable):
        func.__is_agikit_tool__ = True
        func.__agikit_metadata__ = metadata
        return func

    return decorator
