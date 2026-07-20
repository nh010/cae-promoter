from pydantic import BaseModel
from typing import Literal

class Entry(BaseModel):
    tier: Literal["contributed", "community-reviewed", "certified"]
    integrations: list[
        Literal[
            "Anthropic",
            "AWS",
            "Tenable",
            "Tenable Hexa AI MCP",  # spaces + multi-word must survive
            "Wiz",
        ]
    ]

class Skill(Entry):
    compatible_platforms: list[
        Literal["Claude Code", "Cursor", "Windsurf"]
    ]
    invocation: str
