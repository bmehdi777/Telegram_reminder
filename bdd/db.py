import logging
import sqlite3

import os.path

from bdd import sql

class Database:

    def __init__(self, path):
        self.db_path = path
        self.init_db()

    def init_db(self):
        try:
            self.conn()
            cursor = self.conn.cursor()
            logging.info("Création de la base de donnée.")
            cursor.execute(sql.CREATE_TABLE_CHAT)
            logging.info("Table Chat créée.")
            cursor.execute(sql.CREATE_TABLE_ROUTINE)
            logging.info("Table Routine créée.")
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.info("Erreur : la table existe déjà.")
        except Exception as e:
            logging.info("Erreur : {}".format(e))
            self.conn.rollback()

    def conn(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)

    def insert_chat(self, chat_id, enable):
        cursor = self.conn.cursor()
        cursor.execute(sql.INSERT_CHAT,(chat_id,enable))
        self.conn.commit()

    def insert_routine(self, programme, chat_id):
        cursor = self.conn.cursor()
        cursor.execute(sql.INSERT_ROUTINE, (programme, chat_id,))
        self.conn.commit()

    def remove_routine(self, chat_id, routine_id):
        cursor = self.conn.cursor()
        cursor.execute(sql.REMOVE_ROUTINE, (chat_id, routine_id))
        self.conn.commit()

    def get_routine(self, chat_id):
        cursor = self.conn.cursor()
        cursor.execute(sql.GET_ROUTINE, (chat_id,))
        data = cursor.fetchall()
        self.conn.commit()
        return data

    def get_routines_enabled(self):
        cursor = self.conn.cursor()
        cursor.execute(sql.GET_ROUTINES_ENABLED)
        data = cursor.fetchall()
        self.conn.commit()
        return data

    def set_enable_chat(self, chat_id, enable):
        cursor = self.conn.cursor()
        cursor.execute(sql.SET_ENABLE, (enable, chat_id))
        self.conn.commit()

    def get_chat(self, chat_id):
        cursor = self.conn.cursor()
        cursor.execute(sql.GET_CHAT, (chat_id, ))
        data = cursor.fetchall()
        self.conn.commit()
        return data
    def get_chats(self):
        cursor = self.conn.cursor()
        cursor.execute(sql.GET_CHATS)
        data = cursor.fetchall()
        self.conn.commit()
        return data

    def get_chat_enable(self, chat_id):
        chat = self.get_chat(chat_id)
        return chat[0][1]

    def get_chats_with_routine(self):
        cursor = self.conn.cursor()
        cursor.execute(sql.GET_CHATS_WITH_ROUTINE)
        data = cursor.fetchall()
        self.conn.commit()
        return data

    def close_connection(self):
        self.conn.close()
