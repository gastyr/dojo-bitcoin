import { api } from 'src/boot/axios';
import { Block } from 'src/models/Block';

export const blockService = {
  async getBlock(hash: number): Promise<Block> {
    const { data } = await api.get(`/blocks/${hash}`);
    console.log('Dados da API:', data);
    return new Block(data);
  },
};