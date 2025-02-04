from fastapi import FastAPI, HTTPException
from bitcoin.rpc import RawProxy, JSONRPCError
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from dataclasses import dataclass
from contextlib import contextmanager
import os
import uvicorn

@dataclass
class BitcoinConfig:
    host: str
    port: str
    user: str
    password: str
    
    @classmethod
    def from_env(cls):
        return cls(
            host=os.getenv("BITCOIN_RPC_HOST", "localhost"),
            port=os.getenv("BITCOIN_RPC_PORT", "18443"),
            user=os.getenv("BITCOIN_RPC_USER", "user"),
            password=os.getenv("BITCOIN_RPC_PASSWORD", "pass")
        )
    
    @property
    def service_url(self) -> str:
        return f"http://{self.user}:{self.password}@{self.host}:{self.port}"

class BitcoinRPC:
    def __init__(self, config: BitcoinConfig):
        self.config = config
        self._rpc = None
    
    def _create_connection(self) -> RawProxy:
        """
        Cria uma nova conexão RPC
        """
        return RawProxy(service_url=self.config.service_url)

    @contextmanager
    def get_rpc(self):
        """
        Context manager que garante uma conexão fresca para cada operação
        """
        try:
            self._rpc = self._create_connection()
            yield self._rpc
        finally:
            self._rpc = None

external_ip = os.getenv("EXTERNAL_IP", "localhost")
print(f"Allowed origins: [http://localhost:9000, http://localhost:8080, http://{external_ip}:8001, http://{external_ip}, https://{external_ip}]")
app = FastAPI(title="Bitcoin Block Explorer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:9000",
        "http://localhost:8080",
        f"http://{external_ip}:8001",
        f"http://{external_ip}",
        f"https://{external_ip}",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc)
    allow_headers=["*"],  # Permite todos os headers
)

config = BitcoinConfig.from_env()
bitcoin = BitcoinRPC(config)

@app.get("/")
async def read_root():
    """
    Endpoint de healthcheck
    """
    try:
        with bitcoin.get_rpc() as rpc:
            info = rpc.getblockchaininfo()
            return {
                "status": "ok", 
                "message": "Connected to Bitcoin node",
                "chain": info["chain"],
                "blocks": info["blocks"]
            }
    except Exception as ex:
        raise HTTPException(status_code=503, detail=f"Bitcoin node connection error: {str(ex)}")

@app.get("/blocks/{block_number}")
async def get_block_by_number(block_number: int) -> Dict[str, Any]:
    """
    Obtém informações de um bloco específico pelo seu número/altura
    """
    try:
        with bitcoin.get_rpc() as rpc:
            # Obtém o hash do bloco pela altura
            block_hash = rpc.getblockhash(block_number)
            # Obtém informações detalhadas do bloco
            block_info = rpc.getblock(block_hash, 2)
            
            # Processa as transações para incluir informações relevantes
            transactions = []
            for tx in block_info["tx"]:
                tx_processed = {
                    "txid": tx["txid"],
                    "size": tx["size"],
                    "vsize": tx["vsize"],
                    "fee": tx.get("fee", "0"),
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
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"Bloco não encontrado: {str(ex)}")

@app.get("/transactions/{tx_hash}")
async def get_transaction_by_hash(tx_hash: str) -> Dict[str, Any]:
    """
    Obtém informações de uma transação específica pelo seu hash,
    incluindo endereços de origem e destino com seus respectivos valores
    """
    try:
        with bitcoin.get_rpc() as rpc:
            # Verifica se a transação está na mempool primeiro
            try:
                _ = rpc.getmempoolentry(tx_hash)
                in_mempool = True
            except Exception:
                in_mempool = False

            # Obtém a transação
            tx_info = rpc.getrawtransaction(tx_hash, True)
            
            # Processa os inputs e outputs para melhor legibilidade
            inputs = []
            input_addresses = []  # Para rastrear todos endereços de origem
            total_input = 0
            
            # Processa inputs
            for vin in tx_info["vin"]:
                input_info = {
                    "txid": vin.get("txid"),
                    "vout": vin.get("vout"),
                    "sequence": vin.get("sequence")
                }
                
                # Se não for coinbase, busca a transação anterior para obter o endereço e valor
                if "txid" in vin:
                    try:
                        prev_tx = rpc.getrawtransaction(vin["txid"], True)
                        prev_vout = prev_tx["vout"][vin["vout"]]
                        
                        input_info.update({
                            "addresses": prev_vout["scriptPubKey"].get("addresses", []),
                            "value": prev_vout["value"],
                            "type": prev_vout["scriptPubKey"].get("type")
                        })
                        
                        total_input += prev_vout["value"]
                        input_addresses.extend(prev_vout["scriptPubKey"].get("addresses", []))
                    except Exception as e:
                        input_info["error"] = f"Não foi possível obter detalhes do input: {str(e)}"
                else:
                    # Caso seja coinbase
                    input_info.update({
                        "coinbase": vin.get("coinbase"),
                        "type": "coinbase"
                    })
                
                if "scriptSig" in vin:
                    input_info["scriptSig"] = {
                        "asm": vin["scriptSig"].get("asm"),
                        "hex": vin["scriptSig"].get("hex")
                    }
                
                inputs.append(input_info)
            
            # Processa outputs
            outputs = []
            output_addresses = []  # Para rastrear todos endereços de destino
            total_output = 0
            
            for vout in tx_info["vout"]:
                output_info = {
                    "value": vout["value"],
                    "n": vout["n"],
                    "type": vout["scriptPubKey"].get("type"),
                    "addresses": vout["scriptPubKey"].get("addresses", []),
                    "scriptPubKey": vout["scriptPubKey"].get("hex")
                }
                
                total_output += vout["value"]
                output_addresses.extend(vout["scriptPubKey"].get("addresses", []))
                outputs.append(output_info)
            
            # Calcula a taxa se não for coinbase
            fee = round(total_input - total_output, 8) if inputs and "coinbase" not in inputs[0] else 0
            
            # Prepara um resumo das transferências
            transfers = []
            for input_addr in set(input_addresses):
                input_total = sum(
                    inp.get("value", 0) 
                    for inp in inputs 
                    if inp.get("addresses") and input_addr in inp["addresses"]
                )
                
                for output_addr in set(output_addresses):
                    output_total = sum(
                        out["value"] 
                        for out in outputs 
                        if out["addresses"] and output_addr in out["addresses"]
                    )
                    
                    if input_addr != output_addr:  # Ignora transferências para o mesmo endereço
                        transfers.append({
                            "from": input_addr,
                            "to": output_addr,
                            "value": min(input_total, output_total)  # Usa o menor valor para evitar dupla contagem
                        })
            
            result = {
                "txid": tx_info["txid"],
                "size": tx_info["size"],
                "vsize": tx_info["vsize"],
                "weight": tx_info["weight"],
                "fee": fee,
                "total_input": total_input,
                "total_output": total_output,
                "confirmations": tx_info.get("confirmations", 0),
                "time": tx_info.get("time"),
                "in_mempool": in_mempool,
                "inputs": inputs,
                "outputs": outputs,
                "transfers": transfers,  # Nova seção com resumo das transferências
                "input_addresses": list(set(input_addresses)),
                "output_addresses": list(set(output_addresses))
            }

            # Adiciona informações do bloco se a transação estiver confirmada
            if "blockhash" in tx_info:
                block_info = rpc.getblock(tx_info["blockhash"])
                result["block"] = {
                    "hash": block_info["hash"],
                    "height": block_info["height"],
                    "time": block_info["time"]
                }
            
            return result
            
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"Transação não encontrada: {str(ex)}")

@app.get("/balance/{address}")
async def get_address_balance(address: str) -> Dict[str, Any]:
    """
    Obtém o saldo e histórico de transações de um endereço específico
    """
    try:
        with bitcoin.get_rpc() as rpc:
            # Verifica se a carteira está disponível
            try:
                validation = rpc.validateaddress(address)
                if not validation.get("isvalid", False):
                    raise HTTPException(status_code=404, detail="Endereço inválido")
            except JSONRPCError as e:
                raise HTTPException(status_code=400, detail=f"Erro na validação do endereço: {str(e)}")

            # Primeiro tenta obter o saldo via getreceivedbyaddress
            try:
                received = rpc.getreceivedbyaddress(address)
            except JSONRPCError:
                # Se falhar (endereço não na carteira), usa scantxoutset
                descriptor = f"addr({address})"
                scan_result = rpc.scantxoutset("start", [descriptor])
                received = scan_result["total_amount"] if scan_result["success"] else 0
            
            # Obtém UTXOs para informações detalhadas
            try:
                utxos = rpc.listunspent(0, 9999999, [address])
            except JSONRPCError:
                descriptor = f"addr({address})"
                scan_result = rpc.scantxoutset("start", [descriptor])
                utxos = scan_result.get("unspents", []) if scan_result["success"] else []
            
            # Formata os UTXOs
            unspent_outputs = []
            for utxo in utxos:
                output = {
                    "txid": utxo.get("txid"),
                    "vout": utxo.get("vout"),
                    "amount": utxo.get("amount"),
                    "confirmations": utxo.get("confirmations", 0)
                }
                if "height" in utxo:
                    output["height"] = utxo["height"]
                unspent_outputs.append(output)
            
            chain_info = rpc.getblockchaininfo()
            
            return {
                "address": address,
                "network": chain_info["chain"],
                "balance": received,
                "unspent_count": len(unspent_outputs),
                "unspent_outputs": unspent_outputs,
            }
            
    except Exception as ex:
        raise HTTPException(status_code=400, detail=f"Erro ao obter saldo: {str(ex)}")

@app.get("/mempool")
async def get_mempool_info() -> Dict[str, Any]:
    """
    Obtém informações detalhadas sobre a mempool
    """
    try:
        with bitcoin.get_rpc() as rpc:
            mempool_info = rpc.getmempoolinfo()
            # Obtém todas as transações na mempool
            mempool_txs = rpc.getrawmempool(True)
            
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

@app.get("/network/info")
async def get_network_info() -> Dict[str, Any]:
    """
    Obtém informações gerais sobre a rede Bitcoin
    """
    try:
        with bitcoin.get_rpc() as rpc:
            # Obtém informações da blockchain
            chain_info = rpc.getblockchaininfo()
            
            # Obtém informações da mempool
            mempool_info = rpc.getmempoolinfo()
            
            return {
                "isTestnet": chain_info["chain"] != "main",
                "networkName": chain_info["chain"],
                "lastBlock": chain_info["blocks"],
                "mempoolSize": mempool_info["size"]
            }
            
    except Exception as ex:
        raise HTTPException(
            status_code=503, 
            detail=f"Erro ao obter informações da rede: {str(ex)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)