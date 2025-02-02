import { api } from 'src/boot/axios';
import { Network, type NetworkDTO } from 'src/models/Network';

export const networkService = {
  async getNetworkInfo(): Promise<Network> {
    const { data } = await api.get<NetworkDTO>('/network/info');
    return Network.fromDTO(data);
  },
};