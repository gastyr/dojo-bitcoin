// Interface que define a estrutura dos dados recebidos da API
export interface NetworkDTO {
  isTestnet: boolean;
  networkName: string;
  lastBlock: number;
  mempoolSize: number;
}

// Interface que define a estrutura opcional para construção do objeto
interface NetworkConstructor {
  isTestnet?: boolean;
  networkName?: string;
  lastBlock?: number;
  mempoolSize?: number;
}

export class Network implements NetworkDTO {
  readonly isTestnet: boolean;
  readonly networkName: string;
  readonly lastBlock: number;
  readonly mempoolSize: number;

  constructor(data: NetworkConstructor) {
    this.isTestnet = data.isTestnet ?? false;
    this.networkName = data.networkName ?? '';
    this.lastBlock = data.lastBlock ?? 0;
    this.mempoolSize = data.mempoolSize ?? 0;
  }

  // Método estático para criar uma instância a partir dos dados da API
  static fromDTO(dto: NetworkDTO): Network {
    return new Network(dto);
  }
}