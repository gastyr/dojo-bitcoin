export class Transfer {
  readonly type: 'input' | 'output';
  readonly address: string;
  readonly value: number;
  readonly txid: string;
  readonly vout: number | undefined;

  constructor(data: {
    type: 'input' | 'output';
    address: string;
    value: string;
    txid: string;
    vout?: number;
  }) {
    this.type = data.type;
    this.address = data.address;
    this.value = parseFloat(data.value);
    this.txid = data.txid;
    this.vout = data.vout;
  }

  get formattedValue(): string {
    return `${this.value.toFixed(8)} BTC`;
  }
}

export class TransactionInput {
  readonly txid: string;
  readonly vout: number;
  readonly sequence: number;
  readonly addresses: string[];
  readonly value: number;
  readonly type: string;
  readonly scriptSig: {
    asm: string;
    hex: string;
  };

  constructor(data: {
    txid: string;
    vout: number;
    sequence: number;
    addresses: string[];
    value: string;
    type: string;
    scriptSig: { asm: string; hex: string };
  }) {
    this.txid = data.txid;
    this.vout = data.vout;
    this.sequence = data.sequence;
    this.addresses = data.addresses;
    this.value = parseFloat(data.value);
    this.type = data.type;
    this.scriptSig = data.scriptSig;
  }

  get formattedValue(): string {
    if (isNaN(this.value)) {
      return "--";
    }
    return `${this.value.toFixed(8)} BTC`;
  }
}

export class TransactionOutput {
  readonly value: number;
  readonly n: number;
  readonly type: string;
  readonly addresses: string[];
  readonly scriptPubKey: string;

  constructor(data: {
    value: string;
    n: number;
    type: string;
    addresses: string[];
    scriptPubKey: string;
  }) {
    this.value = parseFloat(data.value);
    this.n = data.n;
    this.type = data.type;
    this.addresses = data.addresses;
    this.scriptPubKey = data.scriptPubKey;
  }

  get formattedValue(): string {
    if (isNaN(this.value)) {
      return "--";
    }
    return `${this.value.toFixed(8)} BTC`;
  }
}

export class Transaction {
  readonly txid: string;
  readonly size: number;
  readonly vsize: number;
  readonly weight: number;
  readonly fee: number;
  readonly totalInput: number;
  readonly totalOutput: number;
  readonly confirmations: number;
  readonly time: Date;
  readonly inMempool: boolean;
  readonly inputCount: number;
  readonly outputCount: number;
  readonly inputs: TransactionInput[];
  readonly outputs: TransactionOutput[];
  readonly transfers: Transfer[];
  readonly inputAddresses: string[];
  readonly outputAddresses: string[];
  readonly block: {
    hash: string;
    height: number;
    time: number;
  } | null;

  constructor(data: {
    txid: string;
    size: number;
    vsize: number;
    weight: number;
    fee: string;
    total_input: string;
    total_output: string;
    confirmations: number;
    time: number;
    in_mempool: boolean;
    input_count: number;
    output_count: number;
    inputs?: {
      txid: string;
      vout: number;
      sequence: number;
      addresses: string[];
      value: string;
      type: string;
      scriptSig: { asm: string; hex: string };
    }[];
    outputs?: {
      value: string;
      n: number;
      type: string;
      addresses: string[];
      scriptPubKey: string;
    }[];
    transfers: {
      type: 'input' | 'output';
      address: string;
      value: string;
      txid: string;
      vout?: number;
    }[];
    input_addresses: string[];
    output_addresses: string[];
    block: {
      hash: string;
      height: number;
      time: number;
    } | null;
  }) {
    this.txid = data.txid;
    this.size = data.size;
    this.vsize = data.vsize;
    this.weight = data.weight;
    this.fee = parseFloat(data.fee);
    this.totalInput = parseFloat(data.total_input);
    this.totalOutput = parseFloat(data.total_output);
    this.confirmations = data.confirmations;
    this.time = new Date(data.time * 1000);
    this.inMempool = data.in_mempool;
    this.inputCount = data.input_count;
    this.outputCount = data.output_count;
    this.inputs = (data.inputs || []).map((input) => new TransactionInput(input));
    this.outputs = (data.outputs || []).map((output) => new TransactionOutput(output));
    this.transfers = data.transfers.map((transfer) => new Transfer(transfer));
    this.inputAddresses = data.input_addresses;
    this.outputAddresses = data.output_addresses;
    this.block = data.block;
  }

  get formattedSize(): string {
    return `${this.size} bytes`;
  }

  get formattedWeight(): string {
    return `${this.weight} WU`;
  }

  get formattedFee(): string {
    return `${this.fee.toFixed(8)} BTC`;
  }

  get formattedTotalInput(): string {
    return `${this.totalInput.toFixed(8)} BTC`;
  }

  get formattedTotalOutput(): string {
    return `${this.totalOutput.toFixed(8)} BTC`;
  }

  get feeRate(): number {
    return this.fee / this.vsize;
  }

  get formattedFeeRate(): string {
    return `${(this.feeRate * 100000000).toFixed(2)} sat/vB`;
  }

  get formattedTime(): string {
    return new Intl.DateTimeFormat('pt-BR', {
      dateStyle: 'short',
      timeStyle: 'medium',
    }).format(this.time);
  }

  get isConfirmed(): boolean {
    return this.confirmations > 0;
  }

  get blockHeight(): number | null {
    return this.block?.height ?? null;
  }

  get blockHash(): string | null {
    return this.block?.hash ?? null;
  }

  get blockTime(): Date | null {
    return this.block?.time ? new Date(this.block.time * 1000) : null;
  }
}
