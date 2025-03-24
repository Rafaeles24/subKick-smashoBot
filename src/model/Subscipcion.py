from sqlalchemy import Column, Integer, String, DateTime, Boolean
from config.db import Base, engine

class Subscripcion(Base):
    __tablename__ = "subscipciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_guild_id = Column(Integer, nullable=True)
    discord_id = Column(Integer, unique=True)
    discord_nickname = Column(String, nullable=False)
    vigente = Column(Boolean, default=True) # true de vigente y false de expirado.
    sub_role_active = Column(Boolean, default=True)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=False)
    estado_registro = Column(Boolean, default=True)

Base.metadata.create_all(engine)