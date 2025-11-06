"""
AI Guide Module for SCS Mediator SDK v2
Provides persona-based assistance for instructors and participants
"""

from .chatbot import (
    AIGuide,
    GuidePersona,
    ChatMessage,
    create_instructor_guide,
    create_participant_guide
)

__all__ = [
    "AIGuide",
    "GuidePersona",
    "ChatMessage",
    "create_instructor_guide",
    "create_participant_guide"
]
