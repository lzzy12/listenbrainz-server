# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals
from db.testing import DatabaseTestCase
import logging
from datetime import datetime, timedelta
from tests.utils import generate_data
from webserver.postgres_connection import init_postgres_connection
import db
from db.mockdata import User, Token, Session, TOKEN_EXPIRATION_TIME
from sqlalchemy import text
import uuid


class TestAPICompatUserClass(DatabaseTestCase):

    def setUp(self):
        super(TestAPICompatUserClass, self).setUp()
        self.log = logging.getLogger(__name__)
        self.logstore = init_postgres_connection(self.config.TEST_SQLALCHEMY_DATABASE_URI)

        # Create a user
        uid = db.user.create("test")
        self.assertIsNotNone(db.user.get(uid))
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT * FROM "user" WHERE id = :id'),
                                        {"id": uid})
            self.user = User(result.fetchone())

        # Insert some listens
        date = datetime(2015, 9, 3, 0, 0, 0)
        self.log.info("Inserting test data...")
        test_data = generate_data(date, 100)
        self.logstore.insert_postgresql(test_data)
        self.log.info("Test data inserted")

    def tearDown(self):
        super(TestAPICompatUserClass, self).tearDown()

    def test_user_get_id(self):
        uid = User.get_id(self.user.name)
        self.assertEqual(uid, self.user.id)

    def test_user_load_by_name(self):
        user = User.load_by_name(self.user.name)
        assert isinstance(user, User) == True
        self.assertDictEqual(user.__dict__, self.user.__dict__)

    def test_user_load_by_id(self):
        user = User.load_by_id(self.user.id)
        assert isinstance(user, User) == True
        self.assertDictEqual(user.__dict__, self.user.__dict__)

    def test_user_load_by_apikey(self):
        user = User.load_by_apikey(self.user.api_key)
        self.assertDictEqual(user.__dict__, self.user.__dict__)

    def test_user_get_play_count(self):
        count = User.get_play_count(self.user.name)
        self.assertEqual(count, 100)



class TestAPICompatSessionClass(DatabaseTestCase):

    def setUp(self):
        super(TestAPICompatSessionClass, self).setUp()
        self.log = logging.getLogger(__name__)

    def tearDown(self):
        super(TestAPICompatSessionClass, self).tearDown()

    def test_session_create(self):
        user = User.load_by_id(db.user.create("test"))
        token = Token.generate(user.api_key)
        token.approve(user.name)
        session = Session.create(token)
        self.assertIsInstance(session, Session)
        self.assertDictEqual(user.__dict__, session.user.__dict__)

    def test_session_load(self):
        user = User.load_by_id(db.user.create("test"))
        token = Token.generate(user.api_key)
        token.approve(user.name)
        session = Session.create(token)
        self.assertIsInstance(session, Session)
        self.assertDictEqual(user.__dict__, session.user.__dict__)
        session.user = None

        # Load with session key
        session2 = Session.load(session.sid)
        self.assertDictEqual(user.__dict__, session2.__dict__['user'].__dict__)
        session2.user = None
        self.assertDictEqual(session.__dict__, session2.__dict__)

        # Load with session_key + api_key
        session3 = Session.load(session.sid, session.api_key)
        self.assertDictEqual(user.__dict__, session3.__dict__['user'].__dict__)
        session3.user = None
        self.assertDictEqual(session.__dict__, session3.__dict__)


class TestAPICompatTokenClass(DatabaseTestCase):

    def setUp(self):
        super(TestAPICompatTokenClass, self).setUp()
        self.log = logging.getLogger(__name__)

        # Create a user
        uid = db.user.create("test")
        self.assertIsNotNone(db.user.get(uid))
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT * FROM "user" WHERE id = :id'),
                                        {"id": uid})
            self.user = User(result.fetchone())

    def tearDown(self):
        super(TestAPICompatTokenClass, self).tearDown()

    def test_is_valid_api_key(self):
        self.assertTrue(Token.is_valid_api_key(self.user.api_key))
        self.assertFalse(Token.is_valid_api_key(str(uuid.uuid4())))

    def test_load(self):
        token = Token.generate(self.user.api_key)
        self.assertIsInstance(token, Token)
        self.assertIsNone(token.user)

        ##### Before approving
        # Load with token
        token1 = Token.load(token.token)
        self.assertIsNone(token1.user)
        self.assertDictEqual(token1.__dict__, token.__dict__)

        # Load with token & api_key
        token2 = Token.load(token.token, token.api_key)
        self.assertIsNone(token2.user)
        self.assertDictEqual(token2.__dict__, token.__dict__)

        token.approve(self.user.name)

        ##### After approving the token
        # Load with token
        token1 = Token.load(token.token)
        self.assertIsInstance(token1.user, User)
        self.assertDictEqual(token1.user.__dict__, token.user.__dict__)
        token_user = token.user
        token.user, token1.user = None, None
        self.assertDictEqual(token1.__dict__, token.__dict__)
        token.user = token_user

        # Load with token & api_key
        token2 = Token.load(token.token, token.api_key)
        self.assertIsInstance(token2.user, User)
        self.assertDictEqual(token2.user.__dict__, token.user.__dict__)
        token.user, token1.user = None, None
        self.assertDictEqual(token1.__dict__, token.__dict__)

    def test_generate(self):
        token = Token.generate(str(uuid.uuid4()))
        self.assertIsInstance(token, Token)

    def test_has_expired(self):
        token = Token.generate(str(uuid.uuid4()))
        self.assertFalse(token.has_expired())
        token.timestamp = token.timestamp - timedelta(minutes=TOKEN_EXPIRATION_TIME - 1)
        # This is asssertFalse because in the next 1 minute the next statement will get executed
        self.assertFalse(token.has_expired())
        token.timestamp = token.timestamp - timedelta(minutes=1)
        self.assertTrue(token.has_expired())

    def test_approve(self):
        token = Token.generate(str(uuid.uuid4()))
        self.assertIsInstance(token, Token)
        self.assertIsNone(token.user)
        before_token = token.__dict__
        before_token.pop('user')

        token.approve(self.user.name)

        after_token = token.__dict__
        self.assertIsInstance(token.user, User)
        self.assertDictEqual(token.user.__dict__, self.user.__dict__)
        after_token.pop('user')

        self.assertDictEqual(after_token, before_token)
