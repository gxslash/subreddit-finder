from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy import TEXT
from sqlalchemy import select
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from dataclasses import dataclass
import pandas as pd
import requests.auth
import requests

class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"SubredditPosts(id={self.id!r}, name={self.author!r})"


class Subreddit(Base):
    __tablename__ = 'subreddit'

    id: Mapped[int] = mapped_column(primary_key=True)
    subreddit: Mapped[str] = mapped_column(String(50))

    # TODO: asdasdasd
    def __repr__(self) -> str:
        return f"SubredditPosts(id={self.id!r}, name={self.author!r})"


class User(Base):
    __tablename__ = 'user'

class Comment(Base):
    __tablename__ = 'comment'



""" @dataclass
class SubredditPost:
    
    subreddit: str
    upvote: int
 """

class SqliteManager:

    
    def __init__(self):
        self._engine = create_engine("sqlite://", echo=True)
        Base.metadata.create_all(self._engine)

    def _manage_session(func) -> Session:
        def wrap_func(self, *args, **kwargs):
            session = Session(self._engine)
            func(self, session, *args, **kwargs)
            session.close()
        return wrap_func             

    @_manage_session
    def add_model(self, session: Session, model):
        # session = self._create_session()
        session.add_all(model)
        session.commit()

    @_manage_session
    def delete_model(self, session: Session, model):
        session.delete(model)

    def get_data(self, className):
        with Session(self._engine) as session:
            results = select(className)
        return results
    
@dataclass
class RedditCredentials():

    client_id: str
    client_secret: str
    username: str
    password: str

    def get_post_data(self):
        return {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password
        }

class RedditManager:

    CLIENT_ID = 'EodJ6NZLHH4AxWTATZv1jQ'
    CLIENT_SECRET = '0-ewpG7prMR-lbfUxGO_PwA9ikipgA'
    USERNAME = 'gxslash'
    PASSWORD = 'ynsrmgndz'
    POST_DATA = {
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD
    }

    def __init__(self) -> None:
        self._headers = {'User-Agent': 'script:data-analysis-test:v0.0.1 by /u/gxslash'}
        self._set_header()


    def _set_header(self):
        client_auth = requests.auth.HTTPBasicAuth(self.CLIENT_ID, self.CLIENT_SECRET)
        response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=self.POST_DATA, headers=self._headers)
        result = response.json()
        access_token = result['access_token']
        self._headers['Authorization'] = f'bearer {access_token}'


    def get_sr_posts_new(self, subreddit_name):
        res = requests.get(f'https://oauth.reddit.com/r/{subreddit_name}/new', headers=self._headers, params={'limit':100}).json()
        mdf = pd.DataFrame(res)
        for _ in range(60):
            author = res.get('data').get('children')[-1].get('data').get('name')
            res = requests.get(f'https://oauth.reddit.com/r/{subreddit_name}/new', headers=self._headers, params={'after':f'{author}', 'limit':100})
            mdf = mdf.concat(res)
        mdf.counts()
        return mdf
    

    def get_user_comments():
        ...

    def get_user_posts():
        ...

    def get_sr_about():
        ...



sr1 = Subreddit(author='hammockcamping')
sr2 = Subreddit(author='anothersubreddit')

manager = SqliteManager()
manager.add_model(model=sr1)
data = manager.get_data(Subreddit)

# pd.DataFrame().to_sql()



        
