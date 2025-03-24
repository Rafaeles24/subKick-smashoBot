import easyocr
import cv2
import numpy as np
import re
import os
from datetime import datetime
from .verificarImagen import verificarImagen

async def subImageRead(imagePath):
    try:
        verificarImg = verificarImagen(imagePath)

        if not verificarImg:
            return { "error": "La imagen no coincide con lo establecido."}

        reader = easyocr.Reader(['es'], gpu=True)
        results = reader.readtext(imagePath, detail=True)

        # Extraer el texto detectado
        fullText = " ".join([res[1] for res in results])  

        # Detectar el canal
        canal = "smashdota" if "smashdota" in fullText.lower() else None

        # Extraer fechas en formato de ejemplo: 21 mar 2025
        fechaPattern = re.findall(r'\b\d{2} (?:ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic) \d{4}\b', fullText)
        fechaInicio, fechaFin = (fechaPattern + [None, None])[:2]  # Si no hay dos fechas, rellena con None

        # Detectar el nickname (rango de palabra válida igual a 3)
        palabras = fullText.split()
        palabrasInvalidas = {"Buscar", "Transacciones", "Canal", "Suscripciones", "Historial", "Métodos", "Panel", "Ajustes", "de", "pagos", "pago"}
        nicknamePatterns = re.compile(r'^[a-zA-Z0-9_.-]+$')
        nickname = next((p for p in palabras if p not in palabrasInvalidas and nicknamePatterns.match(p)), None)

        # Cargar imagen y convertir a HSV
        img = cv2.imread(imagePath)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Definir rango de verde en HSV
        lower_green = np.array([35, 80, 80]) 
        upper_green = np.array([85, 255, 255])

        # Crear máscara de detección de color verde
        mask = cv2.inRange(hsv, lower_green, upper_green)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Verificar qué texto está dentro de las áreas verdes
        textoResaltado = None
        for (bbox, text, prob) in results:
            x_min, y_min = int(bbox[0][0]), int(bbox[0][1])
            x_max, y_max = int(bbox[2][0]), int(bbox[2][1])

            for contour in contours:
                if cv2.pointPolygonTest(contour, ((x_min + x_max) // 2, (y_min + y_max) // 2), False) >= 0:
                    textoResaltado = text
                    break

        # Determinar si es regalado o no
        esRegalado = textoResaltado.lower() == "regalado" if textoResaltado else None

        if os.path.exists(imagePath):
            os.remove(imagePath)
        
        # Transforma la fecha de cadena a una valida sql
        meses = {
        	"ene": "Jan", "feb": "Feb", "mar": "Mar", "abr": "Apr",
        	"may": "May", "jun": "Jun", "jul": "Jul", "ago": "Aug",
        	"sep": "Sep", "oct": "Oct", "nov": "Nov", "dic": "Dec"
        }

        dayIni, monthIni, yearIni = fechaInicio.split()
        mesIngIni = meses[monthIni.lower()]
        fechaInicio = datetime.strptime(f"{dayIni} {mesIngIni} {yearIni}", "%d %b %Y")
        fechaInicio = fechaInicio.strftime("%Y-%m-%d") 

        dayFin, monthFin, yearFin = fechaFin.split()
        mesIngFin = meses[monthFin.lower()]
        fechaFin = datetime.strptime(f"{dayFin} {mesIngFin} {yearFin}", "%d %b %Y")
        fechaFin = fechaFin.strftime("%Y-%m-%d") 

        if not esRegalado:
            fechaFin = fechaInicio
            fechaInicio = None

        data = {
            "nickname": nickname,
            "canal_kick": canal,
            "fecha_inicio": fechaInicio,
            "fecha_fin": fechaFin
        }

        return data
    
    except Exception as e:
        print(f"❌ Error en subImageRead: {e}")
        return None
