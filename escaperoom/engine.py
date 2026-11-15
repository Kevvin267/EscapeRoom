"""V2 authority: only this module can decide legal state transitions."""
from dataclasses import dataclass, field, asdict
from copy import deepcopy
from escape_room.world import DRAWER_CODE, DESK_ANSWER, EXIT_CODE, OBJECTS

VERBS = {"look", "examine", "take", "use", "enter", "answer", "inventory", "help", "invalid"}


@dataclass
class State:
    inventory: list[str] = field(default_factory=list)
    drawer_open: bool = False
    desk_unlocked: bool = False
    desk_open: bool = False
    painting_seen: bool = False
    escaped: bool = False
    solved: list[str] = field(default_factory=list)

    def public(self):
        return asdict(self)


@dataclass(frozen=True)
class Action:
    verb: str
    target: str = ""
    value: str = ""


@dataclass
class Outcome:
    state: State
    text: str
    accepted: bool


def apply(state, action):
    """Pure transition: rejected actions return an unchanged copy, never partial state."""
    s = deepcopy(state)

    def result(text, accepted=False):
        return Outcome(s, text, accepted)

    if not isinstance(action, Action) or action.verb not in VERBS:
        return result("That is not a supported action. Try 'examine bookshelf'.")
    v, t, x = action.verb, action.target, action.value
    if s.escaped:
        return result("You have already escaped! Restart to play again.")
    if v in {"look", "help"}:
        return result("Explore the bookshelf, drawer, desk, painting and door. "
                      "Try 'examine bookshelf', 'take key', 'use key on desk', "
                      "'enter 1234 on drawer' or 'answer YOUR_ANSWER'.", True)
    if v == "inventory":
        return result("You carry: " + (", ".join(s.inventory) or "nothing") + ".", True)
    if v == "examine":
        if t == "bookshelf":
            return result("Four books: Winter = 2, Spring = 3, Autumn = 4, Summer = 1. "
                          "An inscription reads: 'Begin with spring; follow the seasons.'", True)
        if t == "drawer":
            return result("The drawer is open. " + ("You have collected its key." if "key" in s.inventory
                          else "A brass key lies inside; you can take it."), True) if s.drawer_open else result(
                          "The drawer has a four-digit combination lock.", True)
        if t == "desk":
            if not s.desk_unlocked:
                return result("The desk compartment has a brass keyhole.", True)
            if not s.desk_open:
                return result("The panel asks: 'I have hands but cannot clap; I measure "
                              "what never stops. What do I measure?'", True)
            return result("The compartment is open. " + ("You have collected its note." if "note" in s.inventory
                          else "A folded note waits inside; you can take it."), True)
        if t == "painting":
            s.painting_seen = True
            return result("The painting shows symbols from left to right: Moon, Sun, Star, Leaf. "
                          "Its caption reads: 'The order opens the way.'", True)
        if t == "note" and "note" in s.inventory:
            return result("The note reads: Moon = 5, Sun = 8, Star = 2, Leaf = 6.", True)
        if t == "key" and "key" in s.inventory:
            return result("A small brass key, matching the desk keyhole.", True)
        if t == "door":
            return result("The exit needs four digits. Its indicators track the drawer, desk "
                          "and symbol puzzles. You need the note and painting clue.", True)
        return result("That object is not available to examine.")
    if v == "take":
        if t in s.inventory:
            return result("You already carry that item.")
        if t == "key" and s.drawer_open:
            s.inventory.append("key")
            return result("You collect the brass key from the drawer.", True)
        if t == "note" and s.desk_open:
            s.inventory.append("note")
            return result("You collect the note. It reads: Moon = 5, Sun = 8, Star = 2, Leaf = 6.", True)
        return result("You cannot collect that item: it is missing, inaccessible or fixed in place.")
    if v == "use":
        if x != "key" or x not in s.inventory:
            return result("You must collect an available item before using it.")
        if t != "desk":
            return result("That item does not work on that object.")
        s.desk_unlocked = True
        return result("The brass key unlocks the desk panel. It asks: 'I have hands but cannot "
                      "clap; I measure what never stops. What do I measure?'", True)
    if v == "answer":
        if t != "desk" or not s.desk_unlocked:
            return result("You must unlock the desk panel before answering its riddle.")
        if x.strip().lower() != DESK_ANSWER:
            return result("That answer does not solve the riddle.")
        s.desk_open = True
        if "desk" not in s.solved:
            s.solved.append("desk")
        return result("Correct. The desk compartment opens, revealing a folded note. Take it.", True)
    if v == "enter" and t == "drawer":
        if x != DRAWER_CODE:
            return result("Incorrect drawer code. The lock does not change.")
        s.drawer_open = True
        if "drawer" not in s.solved:
            s.solved.append("drawer")
        return result("The drawer opens. A brass key is inside; collect it before using it.", True)
    if v == "enter" and t == "door":
        if not (s.drawer_open and s.desk_open and "note" in s.inventory and s.painting_seen):
            return result("The exit remains locked. Complete the drawer and desk puzzles, "
                          "collect the note and examine the painting first.")
        if x != EXIT_CODE:
            return result("Incorrect exit code. The door stays locked.")
        s.solved.append("symbols")
        s.escaped = True
        return result("The symbols align. The door swings open. You step into daylight. You escaped!", True)
    return result("That action is not permitted. Ask for help to see supported actions.")
