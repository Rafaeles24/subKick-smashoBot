import cv2
import os
from skimage.metrics import structural_similarity as ssim

def verificarImagen(imagenPath):
    try:
        umbral=0.7
        plantillasPath = "./src/templates"
        # Cargar imágenes en escala de grises
        imagen = cv2.imread(imagenPath, cv2.IMREAD_GRAYSCALE)

        if imagen is None:
            raise ValueError(f"❌ No se pudo cargar la imagen: {imagenPath}")

        totalScore = 0
        numPlantillas = 0

        # Comparar con la cantidad total de plantillas.
        for plantillaNombre in os.listdir(plantillasPath):
            plantillaPath = os.path.join(plantillasPath, plantillaNombre)
            plantilla = cv2.imread(plantillaPath, cv2.IMREAD_GRAYSCALE)

            if plantilla is None:
                print(f"⚠️ No se pudo cargar la plantilla: {plantillaPath}")
                continue

            if imagen.shape != plantilla.shape:
                imagenResized = cv2.resize(imagen, (plantilla.shape[1], plantilla.shape[0]))
            else:
                imagenResized = imagen
            
            score, _ = ssim(imagenResized, plantilla, full=True)
            totalScore += score
            numPlantillas += 1
        
        if numPlantillas == 0:
            return False
        
        promedioScore = totalScore / numPlantillas
        return promedioScore >= umbral  # Retorna True si la similitud supera el umbral
    
    except Exception as e:
        print(e)
        return None