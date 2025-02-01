from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base

database = create_engine('postgresql+psycopg2://postgres:ONK88Xw0My67lLyO@secretly-feminine-mink.data-1.use1.tembo.io:5432/postgres')
Base = declarative_base()

class Music(Base):
    __tablename__ = "Musics"

    id = Column("ID", String, primary_key=True, unique=True, nullable=False)
    title = Column("Title", String, nullable=False)
    artists = Column("Artists", String, nullable=False)
    duration = Column("Duration", Integer, nullable=False)
    albumImgUrl = Column("AlbumImgUrl", String, nullable=False)

    def __init__(self, id, title, artists, duration, albumImgUrl):
        self.id = id
        self.title = title
        self.artists = artists
        self.duration = duration
        self.albumImgUrl = albumImgUrl

class Executions(Base):
    __tablename__ = "Executions"

    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    musicId = Column("MusciID", ForeignKey(Music.id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    played_At = Column("Played_At", DateTime, nullable=False)

    def __init__(self, musicId, played_At):
        self.musicId = musicId
        self.played_At = played_At

Base.metadata.create_all(bind=database)

