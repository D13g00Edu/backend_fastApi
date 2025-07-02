Para ejecutar esta aplicación:
1. Asegúrate de tener Python instalado.
2. Instala FastAPI y Uvicorn:
   pip install "fastapi[all]" uvicorn
3. Guarda el código anterior en un archivo llamado, por ejemplo, main.py
4. Ejecuta desde tu terminal:
   uvicorn main:app --reload
Una vez en ejecución, podrás acceder a:
- La API en: http://127.0.0.1:8000/
- La documentación interactiva de Swagger UI en: http://127.0.0.1:8000/docs
- La documentación de ReDoc en: http://127.0.0.1:8000/redo