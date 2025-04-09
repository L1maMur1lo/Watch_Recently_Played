import sys
sys.path.append(".")

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import func

from .Schemas import Music, Executions
from datetime import datetime, timedelta

import os

class DatabaseModels:

    def __init__(self):

        self.stringConnection = os.environ["StringConnection"]
        
        self.database = create_engine(self.stringConnection)
        self.Session = sessionmaker(bind=self.database)
        self.session = self.Session()

    def addMusic(self, id:str, title:str, artists:str, duration:int, albumImgUrl:str):
        response = self.session.query(Music).filter_by(id=id).first()

        if response is None:    
            music = Music(id, title, artists, duration, albumImgUrl)
            self.session.add(music)
            self.session.commit()

            return True

    def addExecution(self, musicId:str, played_At:str):
        try:
            dateTime = datetime.strptime(played_At, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            dateTime = datetime.strptime(played_At, '%Y-%m-%dT%H:%M:%SZ')
        
        dateTime = (dateTime - timedelta(hours=3))
        response = self.session.query(Executions).where(Executions.musicId==musicId, Executions.played_At==dateTime).first()

        if response is None:
            executions = Executions(musicId=musicId, played_At=dateTime)
            self.session.add(executions)
            self.session.commit()
        
            return True
    
    def readRows(self, table_name:str):
        if table_name == "Music": response = self.session.query(Music).count()
        elif table_name == "Executions": response = self.session.query(Executions).count()
        else: response = None
        
        return response

    def readAllRows(self, table_name:str, limit:int=100, offset=0):
        if table_name == "Music": response = self.session.query(Music).limit(limit).offset(offset).all()
        elif table_name == "Executions": response = self.session.query(Executions).limit(limit).offset(offset).all()
        else: response = None
        
        return response

    def readTopMusics(self, limit:int=10, offset:int=0) -> list:
        streams = func.count(Executions.musicId).label("streams")
        stream_time = (Music.duration * streams).label("stream_Time")

        response = (self.session.query(
                Music.id,
                Music.title,
                Music.artists,
                Music.duration,
                Music.albumImgUrl,
                streams,
                stream_time
            )
            .select_from(Music)
            .join(Executions)
            .group_by(Music.id)
            .order_by(streams.desc(), Music.title)
            .limit(limit)
            .offset(offset)
        ).all()

        return response

    def readMusic(self, id:str) -> list:
        streams = func.count(Executions.musicId).label("streams")
        stream_time = (Music.duration * streams).label("stream_Time")

        response = (self.session.query(
                Music.id,
                Music.title,
                Music.artists,
                Music.duration,
                Music.albumImgUrl,
                streams,
                stream_time
            )
            .select_from(Music)
            .join(Executions)
            .group_by(Music.id)
            .where(Music.id == id)
        ).first()

        return response
    
    def close(self):
        self.session.close_all()
