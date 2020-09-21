#bool_enable -> 0 false / 1 true
CREATE_TABLE_CHAT="""
CREATE TABLE IF NOT EXISTS Chat(
    chat_id INTEGER PRIMARY KEY,
    bool_enable INTEGER
)
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
