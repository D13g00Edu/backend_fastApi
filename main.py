# Importa las clases necesarias de FastAPI y Pydantic
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List, Optional
import uuid # Para generar IDs únicos

# 1. Define el Modelo de Datos usando Pydantic
# Pydantic nos ayuda a definir la estructura de los datos
# y realiza validaciones automáticas.

# Modelo base para crear o actualizar un elemento
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# Modelo que incluye el ID para los elementos que se leen o se devuelven
class Item(BaseModel):
    id: str # El ID será una cadena (UUID)
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# 2. Inicializa la aplicación FastAPI
app = FastAPI(
    title="API CRUD de Elementos",
    description="Una API RESTful simple para gestionar elementos (CRUD) con FastAPI y almacenamiento en memoria.",
    version="1.0.0",
    docs_url="/docs",       # URL para la documentación de Swagger UI
    redoc_url="/redoc"      # URL para la documentación de ReDoc
)

# 3. Simulación de una base de datos en memoria
# En una aplicación real, esto se conectaría a una base de datos persistente
# (ej. PostgreSQL, MongoDB, SQLite).
# Usamos un diccionario donde la clave es el ID del elemento y el valor es el objeto Item.
fake_db: Dict[str, Item] = {}

# 4. Implementa los Endpoints CRUD

@app.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo elemento",
    description="Añade un nuevo elemento a la base de datos con un ID único generado automáticamente."
)
async def create_item(item: ItemCreate):
    """
    Crea un nuevo elemento en la base de datos.

    - **item**: Objeto ItemCreate que contiene el nombre, descripción, precio e impuesto del elemento.
    - **Retorna**: El elemento creado con su ID único.
    """
    item_id = str(uuid.uuid4()) # Genera un ID único para el elemento
    new_item = Item(id=item_id, **item.dict()) # Combina el ID con los datos del elemento
    fake_db[item_id] = new_item # Almacena el elemento en nuestra "base de datos"
    return new_item

@app.get(
    "/items/",
    response_model=List[Item],
    summary="Obtener todos los elementos",
    description="Recupera una lista de todos los elementos almacenados en la base de datos."
)
async def read_items():
    """
    Recupera todos los elementos.

    - **Retorna**: Una lista de todos los elementos.
    """
    return list(fake_db.values())

@app.get(
    "/items/{item_id}",
    response_model=Item,
    summary="Obtener un elemento por ID",
    description="Recupera un elemento específico utilizando su ID único."
)
async def read_item(item_id: str):
    """
    Recupera un elemento por su ID.

    - **item_id**: El ID único del elemento a recuperar.
    - **Retorna**: El elemento correspondiente si se encuentra.
    - **Lanza**: HTTPException 404 si el elemento no se encuentra.
    """
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Elemento no encontrado"
        )
    return fake_db[item_id]

@app.put(
    "/items/{item_id}",
    response_model=Item,
    summary="Actualizar un elemento existente",
    description="Actualiza los detalles de un elemento existente utilizando su ID. Los campos no proporcionados no se modifican."
)
async def update_item(item_id: str, item: ItemCreate):
    """
    Actualiza un elemento existente por su ID.

    - **item_id**: El ID único del elemento a actualizar.
    - **item**: Objeto ItemCreate con los campos a actualizar.
    - **Retorna**: El elemento actualizado.
    - **Lanza**: HTTPException 404 si el elemento no se encuentra.
    """
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Elemento no encontrado"
        )
    # Actualiza los campos del elemento existente
    updated_item = Item(id=item_id, **item.dict())
    fake_db[item_id] = updated_item
    return updated_item

@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un elemento",
    description="Elimina un elemento de la base de datos utilizando su ID único."
)
async def delete_item(item_id: str):
    """
    Elimina un elemento por su ID.

    - **item_id**: El ID único del elemento a eliminar.
    - **Retorna**: Nada (código de estado 204 No Content) si la eliminación fue exitosa.
    - **Lanza**: HTTPException 404 si el elemento no se encuentra.
    """
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Elemento no encontrado"
        )
    del fake_db[item_id] # Elimina el elemento de la "base de datos"
    return {"message": "Elemento eliminado exitosamente"}


