from __future__ import annotations
import typing as t
from unittest import TestCase

import pytest

from piccolo.engine.finder import engine_finder
from piccolo.engine.postgres import PostgresEngine
from piccolo.engine.sqlite import SQLiteEngine
from piccolo.table import Table


ENGINE = engine_finder()


postgres_only = pytest.mark.skipif(
    not isinstance(ENGINE, PostgresEngine), reason="Only running for Postgres"
)


sqlite_only = pytest.mark.skipif(
    not isinstance(ENGINE, SQLiteEngine), reason="Only running for SQLite"
)


class DBTestCase(TestCase):
    """
    Using raw SQL where possible, otherwise the tests are too reliant on other
    Piccolo code.
    """

    def run_sync(self, query):
        _Table = type("_Table", (Table,), {})
        return _Table.raw(query).run_sync()

    def table_exists(self, tablename: str):
        _Table: t.Type[Table] = type(tablename.upper(), (Table,), {})
        _Table._meta.tablename = tablename
        return _Table.table_exists().run_sync()

    def create_tables(self):
        if ENGINE.engine_type == "postgres":
            self.run_sync(
                """
                CREATE TABLE manager (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50)
                );"""
            )
            self.run_sync(
                """
                CREATE TABLE band (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    manager INTEGER REFERENCES manager,
                    popularity SMALLINT
                );"""
            )
            self.run_sync(
                """
                CREATE TABLE ticket (
                    id SERIAL PRIMARY KEY,
                    price NUMERIC(5,2)
                );"""
            )
            self.run_sync(
                """
                CREATE TABLE poster (
                    id SERIAL PRIMARY KEY,
                    content TEXT
                );"""
            )
        elif ENGINE.engine_type == "sqlite":
            self.run_sync(
                """
                CREATE TABLE manager (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(50)
                );"""
            )
            self.run_sync(
                """
                CREATE TABLE band (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(50),
                    manager INTEGER REFERENCES manager,
                    popularity SMALLINT
                );"""
            )
            self.run_sync(
                """
                CREATE TABLE ticket (
                    id SERIAL PRIMARY KEY,
                    price NUMERIC(5,2)
                );"""
            )
            self.run_sync(
                """
                CREATE TABLE poster (
                    id SERIAL PRIMARY KEY,
                    content TEXT
                );"""
            )
        else:
            raise Exception("Unrecognised engine")

    def insert_row(self):
        self.run_sync(
            """
            INSERT INTO manager (
                name
            ) VALUES (
                'Guido'
            );"""
        )
        self.run_sync(
            """
            INSERT INTO band (
                name,
                manager,
                popularity
            ) VALUES (
                'Pythonistas',
                1,
                1000
            );"""
        )

    def insert_rows(self):
        self.run_sync(
            """
            INSERT INTO manager (
                name
            ) VALUES (
                'Guido'
            ),(
                'Graydon'
            ),(
                'Mads'
            );"""
        )
        self.run_sync(
            """
            INSERT INTO band (
                name,
                manager,
                popularity
            ) VALUES (
                'Pythonistas',
                1,
                1000
            ),(
                'Rustaceans',
                2,
                2000
            ),(
                'CSharps',
                3,
                10
            );"""
        )

    def insert_many_rows(self, row_count=10000):
        """
        Insert lots of data - for testing retrieval of large numbers of rows.
        """
        values = ["('name_{}')".format(i) for i in range(row_count)]
        values_string = ",".join(values)
        self.run_sync(f"INSERT INTO manager (name) VALUES {values_string};")

    def drop_tables(self):
        if ENGINE.engine_type == "postgres":
            self.run_sync("DROP TABLE IF EXISTS band CASCADE;")
            self.run_sync("DROP TABLE IF EXISTS manager CASCADE;")
            self.run_sync("DROP TABLE IF EXISTS ticket CASCADE;")
            self.run_sync("DROP TABLE IF EXISTS poster CASCADE;")
        elif ENGINE.engine_type == "sqlite":
            self.run_sync("DROP TABLE IF EXISTS band;")
            self.run_sync("DROP TABLE IF EXISTS manager;")
            self.run_sync("DROP TABLE IF EXISTS ticket;")
            self.run_sync("DROP TABLE IF EXISTS poster;")

    def setUp(self):
        self.create_tables()

    def tearDown(self):
        self.drop_tables()
