from fastapi import FastAPI, HTTPException
from bitcoin.rpc import RawProxy
from typing import Dict, Any
import os
import uvicorn

app = FastAPI(title="Bitcoin Block Explorer API")

def get_bitcoin_rpc() -> RawProxy:
    """
    Cria uma conexão RPC com o Bitcoin usando variáveis de ambiente
    """
    host = os.getenv("BITCOIN_RPC_HOST", "localhost")
    port = os.getenv("BITCOIN_RPC_PORT", "18443")
    user = os.getenv("BITCOIN_RPC_USER", "user")
    password = os.getenv("BITCOIN_RPC_PASSWORD", "pass")
    
    service_url = f"http://{user}:{password}@{host}:{port}"
    return RawProxy(service_url=service_url)

# Criamos uma única instância do RPC client
bitcoin_rpc = get_bitcoin_rpc()

@app.get("/")
async def read_root():
    """
    Endpoint de healthcheck
    """
    try:
        # Testa a conexão com o node Bitcoin
        bitcoin_rpc.getblockchaininfo()
        return {"status": "ok", "message": "Connected to Bitcoin node"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Bitcoin node connection error: {str(e)}")

@app.get("/blocks/{block_number}")
async def get_block_by_number(block_number: int) -> Dict[str, Any]:
    """
    Obtém informações de um bloco específico pelo seu número/altura
    """
    try:
        # Primeiro obtemos o hash do bloco pela altura
        block_hash = bitcoin_rpc.getblockhash(block_number)
        # Depois obtemos as informações detalhadas do bloco
        block_info = bitcoin_rpc.getblock(block_hash, 2)  # 2 para obter informações detalhadas das transações
        
        return {
            "height": block_info["height"],
            "hash": block_info["hash"],
            "time": block_info["time"],
            "nonce": block_info["nonce"],
            "difficulty": block_info["difficulty"],
            "num_transactions": len(block_info["tx"]),
            "size": block_info["size"],
            "weight": block_info["weight"],
            "merkle_root": block_info["merkleroot"],
            "transactions": block_info["tx"]
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Bloco não encontrado: {str(e)}")

@app.get("/transactions/{tx_hash}")
async def get_transaction_by_hash(tx_hash: str) -> Dict[str, Any]:
    """
    Obtém informações de uma transação específica pelo seu hash
    """
    try:
        tx_info = bitcoin_rpc.getrawtransaction(tx_hash, True)
        
        return {
            "txid": tx_info["txid"],
            "size": tx_info["size"],
            "vsize": tx_info["vsize"],
            "weight": tx_info["weight"],
            "time": tx_info.get("time"),
            "inputs": [{
                "txid": vin.get("txid"),
                "vout": vin.get("vout"),
                "sequence": vin.get("sequence"),
                "scriptSig": vin.get("scriptSig")
            } for vin in tx_info["vin"]],
            "outputs": [{
                "value": vout["value"],
                "n": vout["n"],
                "scriptPubKey": vout["scriptPubKey"]
            } for vout in tx_info["vout"]]
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Transação não encontrada: {str(e)}")

@app.get("/balance/{address}")
async def get_address_balance(address: str) -> Dict[str, float | str]:
    """
    Obtém o saldo de um endereço específico
    """
    try:
        # Obtém informações da carteira
        balance = bitcoin_rpc.getreceivedbyaddress(address)
        
        return {
            "address": address,
            "balance": balance
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Endereço não encontrado ou erro: {str(e)}")

@app.get("/mempool")
async def get_mempool_info() -> Dict[str, Any]:
    """
    Funcionalidade adicional: Obtém informações sobre a mempool
    """
    try:
        mempool_info = bitcoin_rpc.getmempoolinfo()
        return mempool_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter informações da mempool: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)