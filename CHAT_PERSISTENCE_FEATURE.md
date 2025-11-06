# AI Guide Chat Persistence Feature

## Overview

The AI Guide now includes **persistent memory** that saves conversation history across sessions. This means:
- Conversations are automatically saved to disk after each interaction
- Chat history is restored when you return to the application
- Each user role (instructor, participant by party) has separate conversation history
- Conversations persist across page refreshes and browser sessions

## How It Works

### Storage Location

Chat history is saved in JSON files located at:
```
.chat_history/
├── .gitignore              # Prevents committing chat history to git
├── instructor_instructor.json        # Instructor conversations
├── participant_PH_GOV.json          # Philippines participant conversations
├── participant_PRC_MARITIME.json    # PRC participant conversations
└── ... (one file per party)
```

### Automatic Saving

- Every time you send a question to the AI Guide, the conversation is automatically saved
- No manual action is required to preserve your chat history
- Conversations include both questions and responses with timestamps

### Conversation Loading

When you open the application:
1. The AI Guide automatically checks for existing conversation history
2. If found, previous conversations are loaded and displayed
3. You can continue the conversation from where you left off
4. The AI Guide has full context from previous interactions

## Features

### Separate History Per Role

- **Instructor (Dr. Marina Chen)**: Has a single persistent conversation across all scenarios
  - Session ID: `instructor`
  - Accessible from the instructor view sidebar

- **Participants (Ambassador Zhou Wei)**: Each party has separate conversation history
  - Session IDs: `participant_PH_GOV`, `participant_PRC_MARITIME`, `participant_VN_CG`, `participant_MY_NAVY`
  - Ensures each negotiating party maintains independent conversation context

### Display in UI

- **Recent Conversation** section shows the last 2 Q&A pairs
- Uses expandable sections (expanders) to show full responses without truncation
- Most recent conversation is expanded by default for easy reference

### Clear History

- Click the **"Clear History"** button to delete conversation history
- This removes both the in-memory conversation and the persisted file
- Useful for starting fresh or for privacy reasons

## Technical Implementation

### Core Components

1. **`persistence.py`**: Handles saving/loading chat history to JSON files
   - `ChatPersistence` class manages file operations
   - Automatic `.gitignore` creation to prevent committing private conversations
   - Thread-safe file operations

2. **`chatbot.py`**: Enhanced `AIGuide` class with persistence integration
   - `__init__`: Loads existing conversation on initialization
   - `ask()`: Auto-saves after each interaction
   - `clear_history()`: Clears both memory and disk
   - `save_conversation()`: Manual save method (called automatically)

3. **`enhanced_multi_view.py`**: UI integration
   - Initializes AI Guide with appropriate session IDs
   - Converts persisted history to UI display format
   - Maintains synchronization between session state and persistent storage

### Data Format

Each conversation file contains:
```json
{
  "session_id": "instructor",
  "persona": "dr_marina_chen",
  "last_updated": "2025-11-04T10:09:57.123456",
  "context": {
    "scenario": "scenario_A_second_thomas.json",
    "step": 3
  },
  "messages": [
    {
      "role": "user",
      "content": "What is BATNA?"
    },
    {
      "role": "assistant",
      "content": "BATNA stands for Best Alternative to Negotiated Agreement..."
    }
  ]
}
```

## Usage Examples

### For Instructors

1. Ask Dr. Marina Chen a question about peace mediation tools
2. Close the browser or refresh the page
3. Reopen the application - your conversation history is restored
4. Continue asking follow-up questions with full context

### For Participants

1. As Philippines (PH_GOV), ask Ambassador Zhou for negotiation strategy
2. Switch to another party (e.g., PRC_MARITIME)
3. Each party maintains separate conversation history
4. Switch back to Philippines - your original conversation is preserved

## Benefits

### Educational Continuity
- Students can return to complex discussions without losing context
- Instructors can reference previous explanations when needed
- Builds on previous learning across multiple sessions

### Strategic Planning
- Participants can maintain ongoing strategic discussions
- Review previous AI guidance when making decisions
- Track evolution of strategy over multiple negotiation rounds

### Privacy & Control
- Conversations stored locally on the server
- Not shared between different user roles
- Easy to clear when needed for privacy or fresh start

## Disabling Persistence (Optional)

If you need to disable persistence for testing or other reasons:

```python
# In code
guide = create_instructor_guide(enable_persistence=False)

# Or modify the UI initialization
st.session_state.ai_guide = create_instructor_guide(
    session_id="instructor",
    enable_persistence=False  # Disable persistence
)
```

## Troubleshooting

### Conversation Not Loading
- Check if `.chat_history/` directory exists
- Verify JSON file format is valid
- Check file permissions

### Old Conversations Interfering
- Use the "Clear History" button to start fresh
- Or manually delete files in `.chat_history/` directory

### Performance Issues
- Very long conversations (100+ messages) may slow loading
- Consider clearing history periodically
- Each file is typically < 100KB

## Future Enhancements

Potential improvements for future versions:
- Conversation search/filtering
- Export conversations to PDF/markdown
- Conversation sharing between instructors
- Automatic archiving of old conversations
- Conversation analytics and insights
- Multi-user support with user-specific sessions

## Files Modified

- `src/scs_mediator_sdk/ai_guide/persistence.py` - New file
- `src/scs_mediator_sdk/ai_guide/chatbot.py` - Enhanced with persistence
- `src/scs_mediator_sdk/ui/enhanced_multi_view.py` - UI integration

## Testing

The persistence module includes built-in tests:
```bash
python3 src/scs_mediator_sdk/ai_guide/persistence.py
```

This will test:
- Creating storage directory
- Saving conversations
- Loading conversations
- Listing sessions
- Clearing conversations
