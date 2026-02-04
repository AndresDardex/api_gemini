import os
import time
from google import genai
from dotenv import load_dotenv
# 1. Cargar configuración de variables de entorno
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, ".ven"))
load_dotenv()
clave_api = os.getenv("GEMINI_API_KEY")
# 2. Inicializar el Cliente
# Este cliente gestiona la conexión
def ejecutar_consulta():
    print("🚀 Conectando con el motor de Gemini ...")

    if not clave_api:
        print("❌ Falta la variable GEMINI_API_KEY en el entorno.")
        return

    client = genai.Client(api_key=clave_api)

    prompt = "Preséntate brevemente como un asistente de IA configurado para apoyar el curso de 'Desarrollo de aplicaciones con IA"
    max_reintentos = 3
    espera_segundos = 5

    for intento in range(1, max_reintentos + 1):
        try:
            # 3. Llamada directa al servicio de modelos
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    max_output_tokens=128
                ),
            )

            print("\n--- Respuesta Recibida ---")
            print(response.text)
            print("--------------------------")
            return
        except Exception as e:
            mensaje = str(e)
            if "RESOURCE_EXHAUSTED" in mensaje or "429" in mensaje:
                if intento < max_reintentos:
                    print(f"⚠️ Cuota agotada. Reintentando en {espera_segundos}s (intento {intento}/{max_reintentos})...")
                    time.sleep(espera_segundos)
                    espera_segundos *= 2
                    continue
            print(f"❌ Ocurrió un error en la conexión: {e}")
            return


if __name__ == "__main__":
    ejecutar_consulta()