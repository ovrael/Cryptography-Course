##############################
#                            #
#  Jacek Jendrzejewski 2022  #
#                            #
##############################

### API IMPORTS
import base64
import hashlib
import json
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from block import Block
from blockchain import Blockchain

# RUN -> python -m uvicorn main:[BELOW VARIABLE NAME] --reload
app = FastAPI()
blockchain = Blockchain()

@app.get('/chain')
async def get_chain():
    """Gets blockchain as json

    Parameters:
        None

    Returns:
        json with blockchain data
    """
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return  {
            "length": len(chain_data),
            "chain": chain_data
            }
        
@app.get('/mine')
async def mine_block():
    """Mines current blockchain

    Parameters:
        None

    Returns:
        json with blockchain data
    """
    status = blockchain.mine()
    return  {
            "status": status
            }
    
@app.post('/addTransaction')
async def add_transaction(transaction: str):
    """Adds new transaction
    
    Parameters:
        None

    Returns:
        None
    """
    blockchain.add_new_transaction(transaction)
    return True