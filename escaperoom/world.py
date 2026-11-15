"""Author-owned puzzle rules. These are game spoilers, not credentials."""
INTRO = (
    "You wake in a locked library. Rain taps the windows. A bookshelf, a locked "
    "drawer, a desk, a painting and an exit door surround you. Solve three "
    "puzzles to escape. Start by examining the bookshelf."
)
DRAWER_CODE = "3142"
DESK_ANSWER = "time"
EXIT_CODE = "5826"
OBJECTS = ["bookshelf", "drawer", "desk", "painting", "door"]
RULES = """
Room: a locked library. Only five fixtures exist: bookshelf, drawer, desk,
painting, exit door. No other tools or escape routes exist.
Puzzle 1: examine bookshelf: books read Winter=2, Spring=3, Autumn=4, Summer=1.
An inscription says 'Begin with spring; follow the seasons.' Code is 3142.
Opening the drawer requires this code; it reveals a brass key. The player must
explicitly collect the key. Puzzle 2: use collected key on the desk. Its panel
asks 'I have hands but cannot clap; I measure what never stops. What do I measure?'
Answer 'time' opens the compartment and reveals a note: 'Moon 5, Sun 8, Star 2,
Leaf 6'. Player must collect note. Puzzle 3: examine painting to discover order
'Moon, Sun, Star, Leaf'; combine with note for exit code 5826.
Door opens only after drawer and desk puzzles are solved, note is collected,
painting examined and correct door code supplied. Remember collected items and
completed puzzles. Never give solutions before the player works through clues.
Describe only the effects of the player's action. Explicitly report escape only
when the final conditions hold. On escape end your response with [ESCAPED].
"""
