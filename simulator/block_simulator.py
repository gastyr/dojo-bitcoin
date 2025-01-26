import time
import random
import logging
import os
import traceback
from typing import Dict
from bitcoin.rpc import RawProxy, JSONRPCError

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
        self.fallback_fee = 0.00001

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
    
    def create_wallet(self):
        """Cria uma nova wallet se não existir"""
        try:
            # Tenta criar uma nova wallet
            logger.info("Criando wallet...")
            try:
                self.rpc.createwallet("simulator_wallet")
                logger.info("Nova wallet 'simulator_wallet' criada com sucesso")
            except JSONRPCError as ex:
                if "Database already exists" in str(ex):
                    logger.info("Wallet 'simulator_wallet' já existe, carregando...")
                    self.rpc.loadwallet("simulator_wallet")
                else:
                    raise
            
        except Exception as e:
            logger.error(f"Erro ao criar/carregar wallet: {e}")
            raise

    def verify_blockchain_state(self):
        """Verifica o estado atual do blockchain"""
        try:
            info = self.rpc.getblockchaininfo()
            logger.info("Estado atual do blockchain:")
            logger.info(f"Blocos: {info['blocks']}")
            logger.info(f"Headers: {info['headers']}")
            logger.info(f"Chain: {info['chain']}")
            return info
        except Exception as ex:
            logger.error(f"Erro ao verificar estado do blockchain: {ex}")
            raise

    def setup_wallets(self, num_wallets: int = 10):
        """Cria carteiras e armazena seus endereços"""
        try:
            logger.info(f"Criando {num_wallets} carteiras...")

            # Criar endereço para mineração
            self.mining_address = self.rpc.getnewaddress("mining")
            logger.info(f"Endereço de mineração: {self.mining_address}")

            # Criar demais endereços
            for i in range(num_wallets):
                address = self.rpc.getnewaddress(f"wallet{i}")
                self.addresses[address] = 0
                logger.info(f"Criado endereço para wallet{i}: {address}")
        except JSONRPCError as ex:
            logger.error(f"Erro ao criar endereços: {ex}")
            raise

    def generate_initial_blocks(self, num_blocks: int = 101):
        """Gera blocos iniciais para ter fundos para transações"""
        try:
            logger.info(f"Gerando {num_blocks} blocos iniciais...")

            for i in range(0, num_blocks, 10):
                blocks_to_generate = min(10, num_blocks - i)
                self.rpc.generatetoaddress(blocks_to_generate, self.mining_address)
                logger.info(f"Gerados {blocks_to_generate} blocos ({i+1}-{i+blocks_to_generate})")

            balance = self.rpc.getbalance()
            logger.info(f"Saldo após mineração inicial: {balance} BTC")
        except Exception as ex:
            logger.error(f"Erro ao gerar blocos iniciais: {ex}")
            raise

    def create_simple_transaction(self, addresses):
        """Cria uma transação simples"""
        try:
            sender = random.choice(addresses)
            receiver = random.choice([addr for addr in addresses if addr != sender])
            amount = round(random.uniform(0.0001, 0.01), 8)
            
            txid = self.rpc.sendtoaddress(
                receiver, 
                amount,
                "",     # Comment
                "",     # Comment from
                False,  # Subtract fee from amount
                True    # Replaceable
            )
            logger.info(f"Transação simples criada: {amount:.8f} BTC para {receiver}, TXID: {txid}")
            return txid
        except Exception as e:
            logger.error(f"Erro ao criar transação simples: {e}")
            raise

    def create_multi_output_transaction(self, addresses):
        """Cria uma transação com múltiplos outputs"""
        try:
            receivers = random.sample(addresses, min(3, len(addresses)))
            outputs = {}
            for recv in receivers:
                # Reduzindo o valor das transações
                amount = round(random.uniform(0.0001, 0.01), 8)
                outputs[recv] = amount

            raw_tx = self.rpc.createrawtransaction([], outputs)
            
            # Configurando opções básicas para fundrawtransaction
            options = {
                "changePosition": 1,
                "replaceable": True
            }
            
            funded_tx = self.rpc.fundrawtransaction(raw_tx, options)
            signed_tx = self.rpc.signrawtransactionwithwallet(funded_tx['hex'])
            txid = self.rpc.sendrawtransaction(signed_tx['hex'])
            logger.info(f"Transação com múltiplos outputs criada, TXID: {txid}")
            return txid
        except Exception as e:
            logger.error(f"Erro ao criar transação múltipla: {e}")
            raise

    def create_chain_transaction(self, addresses):
        """Cria uma cadeia de transações"""
        try:
            if len(addresses) < 3:
                raise ValueError("Necessário pelo menos 3 endereços para criar cadeia de transações")
                
            addr1, addr2, addr3 = random.sample(addresses, 3)
            amount = round(random.uniform(0.001, 0.005), 8)
            txid1 = self.rpc.sendtoaddress(addr1, amount)
            time.sleep(0.3)
            txid2 = self.rpc.sendtoaddress(addr2, round(amount / 2, 8))
            time.sleep(0.3)
            txid3 = self.rpc.sendtoaddress(addr3, round(amount / 4, 8))
            
            logger.info(f"Transações em cadeia criadas, TXIDs: {txid1}, {txid2}, {txid3}")
        except Exception as e:
            logger.error(f"Erro ao criar cadeia de transações: {e}")
            raise

    def create_complex_transactions(self, num_transactions: int = 100):
        """Cria transações variadas entre as carteiras"""
        logger.info(f"Criando {num_transactions} transações...")
        addresses = list(self.addresses.keys())

        for i in range(num_transactions):
            try:
                # Gera um bloco a cada 2 transações para garantir fundos suficientes
                if i % 2 == 0:
                    self.rpc.generatetoaddress(1, self.mining_address)
                    time.sleep(0.3)
                
                if i % 3 == 0:
                    self.create_simple_transaction(addresses)
                elif i % 3 == 1:
                    self.create_multi_output_transaction(addresses)
                else:
                    self.create_chain_transaction(addresses)

                time.sleep(0.3)
            except Exception as e:
                logger.error(f"Erro na transação {i+1}: {e}\n{traceback.format_exc()}")
                try:
                    self.rpc.generatetoaddress(1, self.mining_address)
                    time.sleep(2)
                except Exception as ex:
                    logger.error(f"Erro ao criar transações: {str(ex)}")

    def distribute_initial_funds(self, amount: float = 10):
        """Distribui fundos iniciais para cada endereço a partir da carteira mineradora."""
        try:
            if not self.mining_address:
                raise ValueError("Endereço minerador não está configurado.")

            for address in self.addresses:
                # Cria uma transação do endereço minerador para o endereço alvo
                outputs = {address: amount}
                raw_tx = self.rpc.createrawtransaction([], outputs)

                # Vincula os fundos ao endereço minerador
                options = {
                    "changeAddress": self.mining_address,
                    "replaceable": True
                }
                funded_tx = self.rpc.fundrawtransaction(raw_tx, options)

                # Assina e envia a transação
                signed_tx = self.rpc.signrawtransactionwithwallet(funded_tx['hex'])
                txid = self.rpc.sendrawtransaction(signed_tx['hex'])
                logger.info(f"Enviados {amount:.8f} BTC de {self.mining_address} para {address}, TXID: {txid}")
        except Exception as e:
            logger.error(f"Erro ao distribuir fundos iniciais: {e}")
            raise

    def run_simulation(self, num_wallets: int = 5, num_transactions: int = 50, final_blocks: int = 10):
        """Executa a simulação completa"""
        try:
            logger.info("Iniciando simulação do blockchain...")

            # Verifica o estado atual da blockchain
            blockchain_info = self.verify_blockchain_state()
            current_blocks = blockchain_info['blocks']

            if current_blocks > 100:
                logger.info(f"A blockchain já possui {current_blocks} blocos. Nenhuma ação será realizada.")
                return

            self.create_wallet()
            self.setup_wallets(num_wallets)
            self.generate_initial_blocks(201)
            
            logger.info("Distribuindo fundos iniciais...")
            self.distribute_initial_funds(10)

            for batch in range((num_transactions + 9) // 10):
                logger.info(f"Iniciando lote {batch+1} de transações...")
                self.create_complex_transactions(min(10, num_transactions - batch * 10))
                self.rpc.generatetoaddress(5, self.mining_address)  # Gerando blocos entre lotes

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
