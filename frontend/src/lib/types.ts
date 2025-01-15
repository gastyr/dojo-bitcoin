export interface BlockInfo {
  height: number;
  hash: string;
  time: number;
  nonce: number;
  difficulty: number;
  num_transactions: number;
  size: number;
  weight: number;
  merkle_root: string;
  transactions: TransactionInfo[];
}

export interface TransactionInfo {
  txid: string;
  size: number;
  vsize: number;
  fee: number;
  input_count: number;
  output_count: number;
  total_output: number;
}

export interface AddressBalance {
  address: string;
  network: string;
  balance: number;
  unspent_count: number;
  unspent_outputs: UnspentOutput[];
}

export interface UnspentOutput {
  txid: string;
  vout: number;
  amount: number;
  confirmations: number;
  height?: number;
}

export interface MempoolInfo {
  size: number;
  bytes: number;
  usage: number;
  transactions: MempoolTransaction[];
}

export interface MempoolTransaction {
  txid: string;
  size: number;
  fee: number;
  time: number;
}