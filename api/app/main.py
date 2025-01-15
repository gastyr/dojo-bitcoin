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

# Cria uma única instância do RPC client
bitcoin_rpc = get_bitcoin_rpc()

@app.get("/")
async def read_root():
    """
    Endpoint de healthcheck
    """
    try:
        info = bitcoin_rpc.getblockchaininfo()
        return {
            "status": "ok", 
            "message": "Connected to Bitcoin node",
            "chain": info["chain"],
            "blocks": info["blocks"]
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Bitcoin node connection error: {str(e)}")

@app.get("/blocks/{block_number}")
async def get_block_by_number(block_number: int) -> Dict[str, Any]:
    """
    Obtém informações de um bloco específico pelo seu número/altura
    """
    try:
        # Obtém o hash do bloco pela altura
        block_hash = bitcoin_rpc.getblockhash(block_number)
        # Obtém informações detalhadas do bloco
        block_info = bitcoin_rpc.getblock(block_hash, 2)
        
        # Processa as transações para incluir informações relevantes
        transactions = []
        for tx in block_info["tx"]:
            tx_processed = {
                "txid": tx["txid"],
                "size": tx["size"],
                "vsize": tx["vsize"],
                "fee": tx.get("fee", 0),
                "input_count": len(tx["vin"]),
                "output_count": len(tx["vout"]),
                "total_output": sum(vout["value"] for vout in tx["vout"])
            }
            transactions.append(tx_processed)
        
        return {
            "height": block_info["height"],
            "hash": block_info["hash"],
            "time": block_info["time"],
            "nonce": block_info["nonce"],
            "difficulty": block_info["difficulty"],
            "num_transactions": len(transactions),
            "size": block_info["size"],
            "weight": block_info["weight"],
            "merkle_root": block_info["merkleroot"],
            "transactions": transactions
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
        
        # Calcula o valor total de saída
        total_output = sum(vout["value"] for vout in tx_info["vout"])
        
        # Processa os inputs e outputs para melhor legibilidade
        inputs = []
        for vin in tx_info["vin"]:
            input_info = {
                "txid": vin.get("txid"),
                "vout": vin.get("vout"),
                "sequence": vin.get("sequence")
            }
            # Adiciona informações do scriptsig se disponível
            if "scriptSig" in vin:
                input_info["scriptSig"] = {
                    "asm": vin["scriptSig"].get("asm"),
                    "hex": vin["scriptSig"].get("hex")
                }
            inputs.append(input_info)
        
        return {
            "txid": tx_info["txid"],
            "size": tx_info["size"],
            "vsize": tx_info["vsize"],
            "weight": tx_info["weight"],
            "total_output": total_output,
            "confirmations": tx_info.get("confirmations", 0),
            "time": tx_info.get("time"),
            "inputs": inputs,
            "outputs": [{
                "value": vout["value"],
                "n": vout["n"],
                "type": vout["scriptPubKey"].get("type"),
                "addresses": vout["scriptPubKey"].get("addresses", []),
                "scriptPubKey": vout["scriptPubKey"].get("hex")
            } for vout in tx_info["vout"]]
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Transação não encontrada: {str(e)}")

@app.get("/balance/{address}")
async def get_address_balance(address: str) -> Dict[str, Any]:
    """
    Obtém o saldo e histórico de transações de um endereço específico
    """
    try:
        # Importa o endereço para a carteira temporariamente
        try:
            bitcoin_rpc.importaddress(address, "", False)
        except Exception:
            pass  # Ignora se o endereço já estiver importado
        
        # Obtém as transações do endereço
        received = bitcoin_rpc.getreceivedbyaddress(address, 0)
        
        # Obtém informações de transações não confirmadas (se houver)
        unconfirmed = 0
        try:
            unconfirmed = bitcoin_rpc.getunconfirmedbalance()
        except Exception:
            pass
        
        return {
            "address": address,
            "balance": received,
            "unconfirmed_balance": unconfirmed,
            "network": "regtest"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao obter saldo: {str(e)}")

@app.get("/mempool")
async def get_mempool_info() -> Dict[str, Any]:
    """
    Obtém informações detalhadas sobre a mempool
    """
    try:
        mempool_info = bitcoin_rpc.getmempoolinfo()
        # Obtém todas as transações na mempool
        mempool_txs = bitcoin_rpc.getrawmempool(True)
        
        return {
            "size": mempool_info["size"],
            "bytes": mempool_info["bytes"],
            "usage": mempool_info["usage"],
            "transactions": [
                {
                    "txid": txid,
                    "size": info["size"],
                    "fee": info["fee"],
                    "time": info["time"]
                }
                for txid, info in mempool_txs.items()
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter informações da mempool: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)