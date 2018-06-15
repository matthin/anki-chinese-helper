from anki.hooks import addHook
from aqt import mw
import os, sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)), "cedict.db"))

def multiple_hanzi(conn, n, flag):
    for char in n["Hanzi"]:
        c = conn.cursor()

        t = (char,)
        c.execute("SELECT * FROM entries WHERE simplified = ? LIMIT 1", t)
        entry = c.fetchone()
        if entry is None:
            return flag
        n["Pinyin"] += entry[2] + " "

        c.close()
    n["Pinyin"] = n["Pinyin"].rstrip()

    return True

# Can't use tab or select another field. You must click outside of a field for this hook to work.
def on_focus_lost(flag, n, fidx):
    if "Chinese" not in n.model()['name']:
        return flag
    if n["Hanzi"] is "" or n["Pinyin"] is not "" or n["Meaning"] is not "":
        return flag

    c = conn.cursor()
    t = (n["Hanzi"],)
    c.execute("SELECT * FROM entries WHERE simplified = ? LIMIT 1", t)
    entry = c.fetchone()
    if entry is None:
        return multiple_hanzi(conn, n, flag)

    n["Pinyin"] = entry[2]
    n["Meaning"] = entry[3].replace("/", "<br>")
    c.close()

    return True

addHook('editFocusLost', on_focus_lost)
