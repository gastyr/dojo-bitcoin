export class UnspentOutput {
  readonly txid: string;
  readonly vout: number;
  readonly amount: number;
  readonly confirmations: number;
  readonly height: number | undefined;

  constructor(data: {
    txid: string;
    vout: number;
    amount: number;
    confirmations: number;
    height?: number;
  }) {
    if (data.amount < 0) throw new Error('Amount cannot be negative');
    if (data.confirmations < 0) throw new Error('Confirmations cannot be negative');

    this.txid = data.txid;
    this.vout = data.vout;
    this.amount = data.amount;
    this.confirmations = data.confirmations;
    this.height = data.height;
  }

  get isConfirmed(): boolean {
    return this.confirmations > 0;
  }

  get formattedAmount(): string {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BTC',
      minimumFractionDigits: 8,
    }).format(this.amount);
  }

}

export class Address {
  readonly address: string;
  readonly network: string;
  readonly balance: number;
  readonly unspentCount: number;
  readonly unspentOutputs: UnspentOutput[];

  constructor(data: {
    address: string;
    network: string;
    balance: number;
    unspent_count: number;
    unspent_outputs: Array<{
      txid: string;
      vout: number;
      amount: number;
      confirmations: number;
      height?: number;
    }>;
  }) {
    if (data.balance < 0) throw new Error('Balance cannot be negative');
    if (data.unspent_count < 0) throw new Error('Unspent count cannot be negative');

    this.address = data.address;
    this.network = data.network;
    this.balance = data.balance;
    this.unspentCount = data.unspent_count;
    this.unspentOutputs = data.unspent_outputs.map((utxo) => new UnspentOutput(utxo));
  }

  get formattedBalance(): string {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BTC',
      minimumFractionDigits: 8,
    }).format(this.balance);
  }

  get totalConfirmedBalance(): number {
    return this.unspentOutputs
      .filter((utxo) => utxo.isConfirmed)
      .reduce((sum, utxo) => sum + utxo.amount, 0);
  }

  get formattedTotalConfirmedBalance(): string {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BTC',
      minimumFractionDigits: 8,
    }).format(this.totalConfirmedBalance);
  }

  get isTestnet(): boolean {
    return this.network === 'testnet';
  }
}