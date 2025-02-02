import { Transaction } from './Transaction';

export class Block {
  readonly height: number;
  readonly hash: string;
  readonly time: Date;
  readonly nonce: number;
  readonly difficulty: number;
  readonly numTransactions: number;
  readonly size: number;
  readonly weight: number;
  readonly merkleRoot: string;
  readonly transactions: Array<Transaction>;

  constructor(data: {
    height: number;
    hash: string;
    time: number;
    nonce: number;
    difficulty: number;
    num_transactions: number;
    size: number;
    weight: number;
    merkle_root: string;
    transactions: Array<{
      txid: string;
      size: number;
      vsize: number;
      weight: number;
      fee: string;
      total_input: string;
      total_output: string;
      input_count: number;
      output_count: number;
      inputs?: Array<{
        txid: string;
        vout: number;
        sequence: number;
        addresses: string[];
        value: string;
        type: string;
        scriptSig: {
          asm: string;
          hex: string;
        };
      }>;
      outputs?: Array<{
        value: string;
        n: number;
        type: string;
        addresses: string[];
        scriptPubKey: string;
      }>;
    }>;
  }) {
    // Validações básicas
    if (data.height < 0) throw new Error('Height cannot be negative');
    if (data.size <= 0) throw new Error('Size must be positive');

    this.height = data.height;
    this.hash = data.hash;
    this.time = new Date(data.time * 1000);
    this.nonce = data.nonce;
    this.difficulty = data.difficulty;
    this.numTransactions = data.num_transactions;
    this.size = data.size;
    this.weight = data.weight;
    this.merkleRoot = data.merkle_root;

    this.transactions = data.transactions.map(
      (tx) =>
        new Transaction({
          txid: tx.txid,
          size: tx.size,
          vsize: tx.vsize,
          weight: tx.weight,
          fee: tx.fee,
          total_input: tx.total_input,
          total_output: tx.total_output,
          confirmations: 1,
          time: data.time,
          in_mempool: false,
          input_count: tx.input_count,
          output_count: tx.output_count,
          inputs: tx.inputs || [],
          outputs: tx.outputs || [],
          transfers: [],
          input_addresses: [],
          output_addresses: [],
          block: {
            hash: this.hash,
            height: this.height,
            time: data.time,
          },
        })
    );
  }

  get formattedTime(): string {
    return new Intl.DateTimeFormat('pt-BR', {
      dateStyle: 'short',
      timeStyle: 'medium',
    }).format(this.time);
  }

  get formattedSize(): string {
    return `${(this.size / 1024).toFixed(2)} KB`;
  }

  get formattedWeight(): string {
    return `${(this.weight / 1000).toFixed(2)} kWU`;
  }

  get formattedDifficulty(): string {
    return new Intl.NumberFormat('pt-BR').format(this.difficulty);
  }

  get formattedHeight(): string {
    return new Intl.NumberFormat('pt-BR').format(this.height);
  }

  get shortHash(): string {
    return `${this.hash.substring(0, 8)}...${this.hash.substring(56)}`;
  }

  get totalFees(): number {
    return this.transactions.reduce((sum, tx) => sum + tx.fee, 0);
  }

  get formattedTotalFees(): string {
    return `${this.totalFees.toFixed(8)} BTC`;
  }

  get averageTransactionSize(): number {
    return this.size / this.numTransactions;
  }

  get formattedAverageTransactionSize(): string {
    return `${this.averageTransactionSize.toFixed(2)} bytes`;
  }
}
