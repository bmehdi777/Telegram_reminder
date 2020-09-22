#bool_enable -> 0 false / 1 true
CREATE_TABLE_CHAT="""
CREATE TABLE IF NOT EXISTS Chat(
    chat_id INTEGER PRIMARY KEY,
    bool_enable INTEGER
)
"""
CREATE_TABLE_ROUTINE="""
CREATE TABLE IF NOT EXISTS Routine(
    routine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    programme TEXT,
    chat_id INTEGER,
    FOREIGN KEY (chat_id) REFERENCES Chat(chat_id)
)
"""

INSERT_ROUTINE="""
INSERT OR REPLACE INTO Routine(programme, chat_id)
VALUES (?, ?)
"""

REMOVE_ROUTINE="""
DELETE FROM Routine
WHERE chat_id = ? AND routine_id = ?
"""

GET_ROUTINES="""
SELECT * FROM Routine
WHERE chat_id = ?
"""

INSERT_CHAT = """
INSERT OR REPLACE INTO Chat(chat_id, bool_enable)
VALUES (?,?);
"""

SET_ENABLE = """
UPDATE Chat
SET bool_enable = ?
WHERE chat_id = ?;
"""

GET_CHAT= """
SELECT *
FROM Chat
WHERE chat_id = ?;
"""
