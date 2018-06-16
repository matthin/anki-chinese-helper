import os
import sqlite3
from anki.hooks import addHook

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
CONN = sqlite3.connect(os.path.join(CURR_DIR, "cedict.db"))


def multiple_hanzi(note, flag):
    """ Helper function for the main matcher when multiple hanzi are used """

    for char in note["Hanzi"]:
        cursor = CONN.cursor()

        # should probably be batched, but doesn't really matter
        cursor.execute("SELECT * FROM entries WHERE simplified = ? LIMIT 1",
                       (char,))
        entry = cursor.fetchone()
        if entry is None:
            return flag
        note["Pinyin"] += entry[2] + " "

        cursor.close()
    note["Pinyin"] = note["Pinyin"].rstrip()

    return True


def on_focus_lost(flag, note, _fidx):
    """ Takes filled in hanzi field and matches empty fields with their
        respective information """

    if "Chinese" not in note.model()['name']:
        return flag
    if not note["Hanzi"] or note["Pinyin"] or note["Meaning"]:
        return flag

    cursor = CONN.cursor()
    cursor.execute("SELECT * FROM entries WHERE simplified = ? LIMIT 1",
                   (note["Hanzi"],))
    entry = cursor.fetchone()
    if entry is None:
        cursor.close()
        return multiple_hanzi(note, flag)

    note["Pinyin"] = entry[2]
    note["Meaning"] = entry[3].replace("/", "<br>")
    cursor.close()

    return True


addHook('editFocusLost', on_focus_lost)
