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


async def createOrUpdateSub(discord_id, discord_nickname, fecha_inicio, fecha_fin):
    db = next(get_db())

    try:
        if isinstance(fecha_inicio, str):
            fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d").date()

        if isinstance(fecha_fin, str):
            fecha_fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d").date()

        sub = db.query(Subscripcion).filter(Subscripcion.discord_id == discord_id).first()

        if sub:
            sub.fecha_inicio = fecha_inicio
            sub.fecha_fin = fecha_fin
            sub.estado_registro = True
        else: 
            nuevaSub = Subscripcion(
                discord_id = discord_id,
                discord_nickname = discord_nickname,
                fecha_inicio = fecha_inicio,
                fecha_fin = fecha_fin,
            )

            db.add(nuevaSub)
        
        db.commit()

        return { "Status": "Success" }
    
    except IntegrityError:   
        db.rollback()
        return { "Error": "❌ El usuario ya tiene una suscripción."}
    except Exception as e:
        db.rollback()
        return { "Error": f"❌ Error inesperado: {str(e)}"}
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