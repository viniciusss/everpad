import sys
sys.path.insert(0, '../..')
from evernote.edam.error.ttypes import EDAMUserException
from thrift.protocol import TBinaryProtocol
from thrift.transport import THttpClient
from evernote.edam.userstore import UserStore
from evernote.edam.notestore import NoteStore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from everpad.provider.models import Base
import os
import keyring


ACTION_NONE = 0
ACTION_CREATE = 1
ACTION_DELETE = 2
ACTION_CHANGE = 3


def get_auth_token():
    return 'S=s1:U=10185:E=140109084eb:C=138b8df58eb:P=1cd:A=en-devtoken:H=5c00b8c378311fe08784fbd70d60cb27'
    return keyring.get_password('everpad', 'token')


def get_db_session(db_path=None):
    if not db_path:
        db_path = os.path.expanduser('~/.config/everpad.db')
    engine = create_engine('sqlite:///%s' % db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def get_note_store(auth_token=None):
    if not auth_token:
        auth_token = get_auth_token()
    evernote_host = "sandbox.evernote.com"
    user_store_uri = "https://" + evernote_host + "/edam/user"
    user_store_http_client = THttpClient.THttpClient(user_store_uri)
    user_store_protocol = TBinaryProtocol.TBinaryProtocol(user_store_http_client)
    user_store = UserStore.Client(user_store_protocol)
    note_store_url = user_store.getNoteStoreUrl(auth_token)
    note_store_http_client = THttpClient.THttpClient(note_store_url)
    note_store_protocol = TBinaryProtocol.TBinaryProtocol(note_store_http_client)
    return NoteStore.Client(note_store_protocol)
