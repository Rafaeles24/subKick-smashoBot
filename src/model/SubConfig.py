from sqlalchemy import Column, Integer
from config.db import Base, engine

class SubConfig(Base):
    __tablename__ = "subconfig"

    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_guild_id = Column(Integer, unique=True)
    discord_sub_role_id = Column(Integer, unique=True, nullable=True)
    discord_sub_channel_id = Column(Integer, unique=True, nullable=True)

Base.metadata.create_all(engine)