const API_BASE = '/api';

export async function getBlockInfo(blockNumber: number) {
  const response = await fetch(`${API_BASE}/blocks/${blockNumber}`);
  if (!response.ok) throw new Error('Bloco não encontrado');
  return response.json();
}

export async function getTransaction(txHash: string) {
  const response = await fetch(`${API_BASE}/transactions/${txHash}`);
  if (!response.ok) throw new Error('Transação não encontrada');
  return response.json();
}

export async function getAddressBalance(address: string) {
  const response = await fetch(`${API_BASE}/balance/${address}`);
  if (!response.ok) throw new Error('Endereço inválido');
  return response.json();
}

export async function getMempoolInfo() {
  const response = await fetch(`${API_BASE}/mempool`);
  if (!response.ok) throw new Error('Erro ao obter informações da mempool');
  return response.json();
}

// import { mockData } from './mockData';

// const delay = (ms: number) => new Promise<void>(resolve => setTimeout(resolve, ms));

// export async function getBlockInfo(blockNumber: number) {
//   await delay(500);
//   return mockData.block;
// }

// export async function getTransaction(txHash: string) {
//   await delay(500);
//   return mockData.transaction;
// }

// export async function getAddressBalance(address: string) {
//   await delay(500);
//   return mockData.address;
// }

// export async function getMempoolInfo() {
//   await delay(500);
//   return mockData.mempool;
// }