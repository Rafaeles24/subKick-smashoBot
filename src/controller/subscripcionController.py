from sqlalchemy.exc import IntegrityError
from config.db import get_db
from model.Subscipcion import Subscripcion
import datetime

async def getSubscripcion(discord_id):
    db = next(get_db())

    try:
        sub = db.query(Subscripcion).filter(Subscripcion.discord_id == discord_id).first()

        if not sub: 
            return { "status": "Error" }
        
        return sub
    
    except Exception as e:
        db.rollback()
        return f"❌ Error inesperado: {str(e)}"
    finally:
        db.close()

async def getAllActiveSubscripciones(discord_guild_id):
    db = next(get_db())

    try:
        subs = db.query(Subscripcion).filter(
            Subscripcion.discord_guild_id == discord_guild_id, 
            Subscripcion.vigente == True, 
            Subscripcion.estado_registro == True, 
            Subscripcion.sub_role_active == True
            ).all()
        return subs
    
    except Exception as e:
        db.rollback()
        return f"❌ Error inesperado: {str(e)}"
    finally:
        db.close()



async def createOrUpdateSub(discord_guild_id, discord_id, discord_nickname, fecha_inicio, fecha_fin):
    db = next(get_db())
    try:
        if isinstance(fecha_inicio, str):
            fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d").date()

        if isinstance(fecha_fin, str):
            fecha_fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d").date()

        sub = db.query(Subscripcion).filter(Subscripcion.discord_guild_id == discord_guild_id, Subscripcion.discord_id == discord_id).first()
        print(f"Subscripcion encontrada: {sub}")

        if sub:
            sub.vigente = True
            sub.sub_role_active = True
            sub.fecha_inicio = fecha_inicio
            sub.fecha_fin = fecha_fin
            sub.estado_registro = True
            print(f"Subscripcion actualizada: {sub}")
        else: 
            nuevaSub = Subscripcion(
                discord_guild_id = discord_guild_id,
                discord_id = discord_id,
                discord_nickname = discord_nickname,
                fecha_inicio = fecha_inicio,
                fecha_fin = fecha_fin,
            )
            print(f"Subscripcion nueva: {nuevaSub}")
            db.add(nuevaSub)

        db.commit()

        return "Success"
    
    except IntegrityError:   
        db.rollback()
        return "❌ El usuario ya tiene una suscripción."
    except Exception as e:
        db.rollback()
        print(f"❌ Error inesperado: {str(e)}")
        return f"❌ Hubo un error inesperado."
    finally:
        db.close()

async def desactivarSubscripcion(discord_id):
    db = next(get_db())

    try:
        sub = db.query(Subscripcion).filter(Subscripcion.discord_id == discord_id).first()
        
        if not sub:
            return "Este usuario no posee una subscipcion."

        sub.estado_registro = False

        db.commit()
        return "Success"
    
    except Exception as e:
        db.rollback()
        return f"❌ Error inesperado: {str(e)}"
    finally:
        db.close()

async def setExpiredSubscripciones(discord_guild_id):
    db = next(get_db())

    try:
        subs = await getAllActiveSubscripciones(discord_guild_id)

        for sub in subs:
            tiempoActual = datetime.date.today()
            if sub.fecha_fin.date() < tiempoActual:
                sub.vigente = False
                db.add(sub)
                db.commit()

        return await getExpiredSubscripciones(discord_guild_id)
    
    except Exception as e:
        db.rollback()
        return f"❌ Error inesperado: {str(e)}"
    finally:
        db.close()

async def getExpiredSubscripciones(discord_guild_id):
    db = next(get_db())
    try:
        subs = db.query(Subscripcion).filter(
            Subscripcion.discord_guild_id == discord_guild_id, 
            Subscripcion.estado_registro == True, 
            Subscripcion.vigente == False,
            Subscripcion.sub_role_active == True
            ).all()
        
        return subs

    except Exception as e:
        db.rollback()
        return f"❌ Error inesperado: {str(e)}"
    finally:
        db.close()

async def setRoleExpired(discord_id):
    db = next(get_db())
    try:
        expired = db.query(Subscripcion).filter(Subscripcion.discord_id == discord_id).first()
        expired.sub_role_active = False
        db.add(expired)
        db.commit()

        return expired
    except Exception as e:
        db.rollback()
        return f"❌ Error inesperado: {str(e)}"
    finally:
        db.close()