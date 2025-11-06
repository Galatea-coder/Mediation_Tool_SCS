"""
Persistence layer for AI Guide chat history
Saves and loads conversation history to/from JSON files
"""

import os
import json
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

# Handle both module import and direct execution
try:
    from .chatbot import ChatMessage
except ImportError:
    # For direct execution, define ChatMessage locally
    @dataclass
    class ChatMessage:
        """A single message in the chat history"""
        role: str  # "user" or "assistant"
        content: str


class ChatPersistence:
    """
    Manages persistent storage of chat conversations
    Uses JSON files in .chat_history directory
    """

    def __init__(self, storage_dir: str = None):
        """
        Initialize persistence layer

        Args:
            storage_dir: Directory to store chat history (defaults to .chat_history in project root)
        """
        if storage_dir is None:
            # Default to .chat_history in project root
            project_root = Path(__file__).parent.parent.parent.parent
            self.storage_dir = project_root / ".chat_history"
        else:
            self.storage_dir = Path(storage_dir)

        # Create storage directory if it doesn't exist
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Add .gitignore to prevent committing chat history
        gitignore_path = self.storage_dir / ".gitignore"
        if not gitignore_path.exists():
            with open(gitignore_path, 'w') as f:
                f.write("# Ignore all chat history files\n*.json\n")

    def _get_file_path(self, session_id: str, persona: str) -> Path:
        """
        Get file path for a specific session and persona

        Args:
            session_id: Unique session identifier (e.g., "instructor" or "participant_PH_GOV")
            persona: Persona type ("instructor" or "participant")

        Returns:
            Path to the chat history file
        """
        filename = f"{persona}_{session_id}.json"
        return self.storage_dir / filename

    def save_conversation(
        self,
        session_id: str,
        persona: str,
        conversation_history: List[ChatMessage],
        context: Dict = None
    ) -> bool:
        """
        Save conversation history to file

        Args:
            session_id: Unique session identifier
            persona: Persona type
            conversation_history: List of chat messages
            context: Optional session context

        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = self._get_file_path(session_id, persona)

            # Convert ChatMessage objects to dictionaries
            messages_dict = [
                {"role": msg.role, "content": msg.content}
                for msg in conversation_history
            ]

            data = {
                "session_id": session_id,
                "persona": persona,
                "last_updated": datetime.now().isoformat(),
                "context": context or {},
                "messages": messages_dict
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False

    def load_conversation(
        self,
        session_id: str,
        persona: str
    ) -> tuple[List[ChatMessage], Dict]:
        """
        Load conversation history from file

        Args:
            session_id: Unique session identifier
            persona: Persona type

        Returns:
            Tuple of (conversation_history, context)
            Returns ([], {}) if file doesn't exist or can't be loaded
        """
        try:
            file_path = self._get_file_path(session_id, persona)

            if not file_path.exists():
                return [], {}

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Convert dictionaries back to ChatMessage objects
            messages = [
                ChatMessage(role=msg["role"], content=msg["content"])
                for msg in data.get("messages", [])
            ]

            context = data.get("context", {})

            return messages, context

        except Exception as e:
            print(f"Error loading conversation: {e}")
            return [], {}

    def clear_conversation(self, session_id: str, persona: str) -> bool:
        """
        Clear (delete) conversation history file

        Args:
            session_id: Unique session identifier
            persona: Persona type

        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = self._get_file_path(session_id, persona)

            if file_path.exists():
                file_path.unlink()

            return True

        except Exception as e:
            print(f"Error clearing conversation: {e}")
            return False

    def list_sessions(self, persona: str = None) -> List[str]:
        """
        List all available session IDs

        Args:
            persona: Optional filter by persona type

        Returns:
            List of session IDs
        """
        try:
            sessions = []

            for file_path in self.storage_dir.glob("*.json"):
                if file_path.name == ".gitignore":
                    continue

                parts = file_path.stem.split("_", 1)
                if len(parts) == 2:
                    file_persona, session_id = parts

                    if persona is None or file_persona == persona:
                        sessions.append(session_id)

            return sorted(sessions)

        except Exception as e:
            print(f"Error listing sessions: {e}")
            return []


# Convenience function
def create_persistence(storage_dir: str = None) -> ChatPersistence:
    """Create chat persistence instance"""
    return ChatPersistence(storage_dir)


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Chat Persistence")
    print("=" * 60)

    # Create persistence instance
    persistence = create_persistence()
    print(f"\nStorage directory: {persistence.storage_dir}")

    # Test saving conversation
    test_history = [
        ChatMessage(role="user", content="What is BATNA?"),
        ChatMessage(role="assistant", content="BATNA stands for Best Alternative to Negotiated Agreement...")
    ]

    test_context = {
        "scenario": "scenario_A_second_thomas.json",
        "step": 3
    }

    print("\n1. Saving test conversation...")
    success = persistence.save_conversation(
        session_id="test_session",
        persona="instructor",
        conversation_history=test_history,
        context=test_context
    )
    print(f"   Save successful: {success}")

    # Test loading conversation
    print("\n2. Loading conversation...")
    loaded_history, loaded_context = persistence.load_conversation(
        session_id="test_session",
        persona="instructor"
    )
    print(f"   Loaded {len(loaded_history)} messages")
    print(f"   Context: {loaded_context}")

    # Test listing sessions
    print("\n3. Listing all sessions...")
    sessions = persistence.list_sessions()
    print(f"   Found sessions: {sessions}")

    # Test clearing
    print("\n4. Clearing test conversation...")
    success = persistence.clear_conversation(
        session_id="test_session",
        persona="instructor"
    )
    print(f"   Clear successful: {success}")

    print("\n" + "=" * 60)
    print("Persistence tests complete!")
    print("=" * 60)
