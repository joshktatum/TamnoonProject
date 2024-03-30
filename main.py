from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.crud import create_asset, get_assets, get_asset, create_group, delete_asset, get_assets_by_group

app = FastAPI()
class Tag(BaseModel):
    key: str
    value: str
class Cloud_account(BaseModel):
    id: str
    name: str
class Asset(BaseModel):
    id: str
    name: str
    type: str
    tags: List[Tag]
    cloud_account: Cloud_account
    owner_id: str
    region: str
    group_name: str = ""
    
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI DynamoDB Todo App!"}

@app.get("/asset/", response_model=List[Asset])
def read_api_assets():
    return get_assets()

@app.post("/asset", response_model=Asset)
def create_api_asset(asset: Asset):
    created_asset = create_asset(asset.model_dump())
    return created_asset # Ensure that create_asset returns the asset itself

@app.get("/asset/{id}", response_model=Asset)
def read_api_asset(id: str):
    asset = get_asset(id)
    if not asset:
        raise HTTPException(status_code=404, detail="asset not found")
    return asset

@app.delete("/asset/{id}", response_model=dict)
def delete_api_asset(id: str):
    response = delete_asset(id)
    if 'ResponseMetadata' not in response:
        raise HTTPException(status_code=404, detail="asset not found")
    return {"message": "asset deleted successfully"}

@app.put("/group/{group_name}", response_model = List[Asset])
def create_api_group(group_name:str, type: str | None=None, tags: List[Tag] | None=None, cloud_account:Cloud_account | None=None, owner_id:str | None=None, region:str | None=None):
    return create_group(group_name, type, tags, cloud_account, owner_id, region)

@app.get("/asset/group/{group_name}", response_model=List[Asset])
def read_api_group(group_name):
    return get_assets_by_group(group_name)