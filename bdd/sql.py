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

GET_ROUTINE="""
SELECT * FROM Routine
WHERE chat_id = ?
"""

GET_ROUTINES_ENABLED="""
SELECT * FROM Routine
INNER JOIN Chat ON Routine.chat_id = Chat.chat_id
WHERE Chat.bool_enable = 1
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

GET_CHATS="""
SELECT * FROM Chat
"""

GET_CHATS_WITH_ROUTINE="""
SELECT * FROM Chat
INNER JOIN Routine ON Chat.chat_id = Routine.chat_id
WHERE Chat.bool_enable = 1 GROUP BY Chat.chat_id
"""
