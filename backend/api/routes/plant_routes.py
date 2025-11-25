# backend/api/routes/plant_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/plants", tags=["plants"])

# Pydantic models
class PlantCreate(BaseModel):
    name: str
    species: str
    status: Optional[str] = "offline"
    health: Optional[str] = "Unknown"
    water: Optional[str] = "Not watered yet"
    image: Optional[str] = "https://images.unsplash.com/photo-1466781783364-36c955e42a7f?w=400&h=400&fit=crop"
    age_months: Optional[int] = 0

class PlantUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    status: Optional[str] = None
    health: Optional[str] = None
    water: Optional[str] = None
    image: Optional[str] = None
    age_months: Optional[int] = None

class Plant(BaseModel):
    id: str
    name: str
    species: str
    status: str
    health: str
    water: str
    image: str
    age_months: int
    created_at: datetime
    updated_at: datetime

# Get MongoDB instance
from backend.mongo.main import MongoDB

@router.post("/", response_model=Plant)
async def create_plant(plant: PlantCreate):
    """Create a new plant"""
    try:
        database = await MongoDB.get_database()
        plants_collection = database["plants"]
        
        plant_dict = plant.dict()
        plant_dict["created_at"] = datetime.utcnow()
        plant_dict["updated_at"] = datetime.utcnow()
        
        result = await plants_collection.insert_one(plant_dict)
        
        # Get the inserted plant
        created_plant = await plants_collection.find_one({"_id": result.inserted_id})
        created_plant["id"] = str(created_plant.pop("_id"))
        
        return created_plant
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating plant: {str(e)}")

@router.get("/", response_model=List[Plant])
async def get_all_plants():
    """Get all plants"""
    try:
        database = await MongoDB.get_database()
        plants_collection = database["plants"]
        
        plants = []
        async for plant in plants_collection.find():
            plant["id"] = str(plant.pop("_id"))
            plants.append(plant)
        
        return plants
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting plants: {str(e)}")

@router.get("/{plant_id}", response_model=Plant)
async def get_plant(plant_id: str):
    """Get a specific plant by ID"""
    try:
        database = await MongoDB.get_database()
        plants_collection = database["plants"]
        
        plant = await plants_collection.find_one({"_id": ObjectId(plant_id)})
        
        if not plant:
            raise HTTPException(status_code=404, detail="Plant not found")
        
        plant["id"] = str(plant.pop("_id"))
        return plant
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting plant: {str(e)}")

@router.put("/{plant_id}", response_model=Plant)
async def update_plant(plant_id: str, plant_update: PlantUpdate):
    """Update a plant"""
    try:
        database = await MongoDB.get_database()
        plants_collection = database["plants"]
        
        # Only update fields that are provided
        update_data = {k: v for k, v in plant_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await plants_collection.update_one(
            {"_id": ObjectId(plant_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Plant not found")
        
        # Get updated plant
        updated_plant = await plants_collection.find_one({"_id": ObjectId(plant_id)})
        updated_plant["id"] = str(updated_plant.pop("_id"))
        
        return updated_plant
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating plant: {str(e)}")

@router.delete("/{plant_id}")
async def delete_plant(plant_id: str):
    """Delete a plant"""
    try:
        database = await MongoDB.get_database()
        plants_collection = database["plants"]
        
        result = await plants_collection.delete_one({"_id": ObjectId(plant_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Plant not found")
        
        return {"message": "Plant deleted successfully", "id": plant_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting plant: {str(e)}")