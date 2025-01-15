import time
import random
import logging
import os
import traceback
from typing import Dict
from bitcoin.rpc import RawProxy

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class BitcoinSimulator:
    def __init__(self):
        # Configurações de ambiente
        host = os.getenv("BITCOIN_RPC_HOST", "bitcoin")
        port = os.getenv("BITCOIN_RPC_PORT", "18443")
        user = os.getenv("BITCOIN_RPC_USER", "user")
        password = os.getenv("BITCOIN_RPC_PASSWORD", "pass")
        
        self.service_url = f"http://{user}:{password}@{host}:{port}"
        self.addresses: Dict[str, float] = {}
        self.mining_address = None

        # Esperar o node Bitcoin estar pronto
        self.wait_for_bitcoin_node()
        self.rpc = RawProxy(service_url=self.service_url)

    def wait_for_bitcoin_node(self, max_retries: int = 30):
        """Espera o node Bitcoin estar pronto para aceitar conexões"""
        retry = 0
        while retry < max_retries:
            try:
                rpc = RawProxy(service_url=self.service_url)
                rpc.getblockchaininfo()
                logger.info("Conexão com Bitcoin node estabelecida!")
                return
            except Exception as ex:
                retry += 1
                logger.warning(f"Erro ao conectar ao Bitcoin node: {ex}")
                logger.info(f"Tentativa {retry}/{max_retries}...")
                time.sleep(2)
        raise Exception("Não foi possível conectar ao Bitcoin node após várias tentativas.")

    def setup_wallets(self, num_wallets: int = 10):
        """Cria carteiras e armazena seus endereços"""
        logger.info(f"Criando {num_wallets} carteiras...")

        # Criar endereço para mineração
        self.mining_address = self.rpc.getnewaddress("mining")
        logger.info(f"Endereço de mineração: {self.mining_address}")

        # Criar demais endereços
        for i in range(num_wallets):
            address = self.rpc.getnewaddress(f"wallet{i}")
            self.addresses[address] = 0
            logger.info(f"Criada carteira {i}: {address}")

    def generate_initial_blocks(self, num_blocks: int = 101):
        """Gera blocos iniciais para ter fundos para transações"""
        logger.info(f"Gerando {num_blocks} blocos iniciais...")

        for i in range(0, num_blocks, 10):
            blocks_to_generate = min(10, num_blocks - i)
            self.rpc.generatetoaddress(blocks_to_generate, self.mining_address)
            logger.info(f"Gerados {blocks_to_generate} blocos ({i+1}-{i+blocks_to_generate})")

        balance = self.rpc.getbalance()
        logger.info(f"Saldo após mineração inicial: {balance} BTC")

    def create_simple_transaction(self, addresses):
        """Cria uma transação simples"""
        sender = random.choice(addresses)
        receiver = random.choice([addr for addr in addresses if addr != sender])
        amount = random.uniform(0.0001, 0.1)
        txid = self.rpc.sendtoaddress(receiver, amount)
        logger.info(f"Transação simples criada: {amount:.8f} BTC para {receiver}, TXID: {txid}")

    def create_multi_output_transaction(self, addresses):
        """Cria uma transação com múltiplos outputs"""
        receivers = random.sample(addresses, 3)
        outputs = {recv: random.uniform(0.0001, 0.05) for recv in receivers}

        raw_tx = self.rpc.createrawtransaction([], outputs)
        funded_tx = self.rpc.fundrawtransaction(raw_tx)
        signed_tx = self.rpc.signrawtransactionwithwallet(funded_tx['hex'])
        txid = self.rpc.sendrawtransaction(signed_tx['hex'])
        logger.info(f"Transação com múltiplos outputs criada, TXID: {txid}")

    def create_chain_transaction(self, addresses):
        """Cria uma cadeia de transações"""
        addr1, addr2, addr3 = random.sample(addresses, 3)
        amount = random.uniform(0.001, 0.01)
        txid1 = self.rpc.sendtoaddress(addr1, amount)
        txid2 = self.rpc.sendtoaddress(addr2, amount / 2)
        txid3 = self.rpc.sendtoaddress(addr3, amount / 4)
        logger.info(f"Transações em cadeia criadas, TXIDs: {txid1}, {txid2}, {txid3}")

    def create_complex_transactions(self, num_transactions: int = 100):
        """Cria transações variadas entre as carteiras"""
        logger.info(f"Criando {num_transactions} transações...")
        addresses = list(self.addresses.keys())

        for i in range(num_transactions):
            try:
                if i % 3 == 0:
                    self.create_simple_transaction(addresses)
                elif i % 3 == 1:
                    self.create_multi_output_transaction(addresses)
                else:
                    self.create_chain_transaction(addresses)

                if (i + 1) % 5 == 0:
                    self.rpc.generatetoaddress(1, self.mining_address)
                    logger.info(f"Novo bloco gerado após {i+1} transações")
            except Exception as e:
                logger.error(f"Erro na transação {i+1}: {e}\n{traceback.format_exc()}")

    def run_simulation(self, num_wallets: int = 10, num_transactions: int = 100, final_blocks: int = 10):
        """Executa a simulação completa"""
        try:
            logger.info("Iniciando simulação do blockchain...")

            self.setup_wallets(num_wallets)
            self.generate_initial_blocks(101)

            for batch in range((num_transactions + 19) // 20):
                logger.info(f"Iniciando lote {batch+1} de transações...")
                self.create_complex_transactions(min(20, num_transactions - batch * 20))
                self.rpc.generatetoaddress(3, self.mining_address)

            logger.info(f"Gerando {final_blocks} blocos finais...")
            self.rpc.generatetoaddress(final_blocks, self.mining_address)

            logger.info("Simulação concluída!")
            for address in self.addresses:
                balance = self.rpc.getreceivedbyaddress(address)
                logger.info(f"Endereço: {address}, Saldo final: {balance:.8f} BTC")

        except Exception as e:
            logger.error(f"Erro durante a simulação: {e}\n{traceback.format_exc()}")
            raise

if __name__ == "__main__":
    num_wallets = 10
    num_transactions = 100
    simulator = BitcoinSimulator()
    simulator.run_simulation(num_wallets=num_wallets, num_transactions=num_transactions)
