import { api } from 'src/boot/axios';
import { Address } from 'src/models/Address';

export const addressService = {
  async getAddress(address: string): Promise<Address> {
    console.log("Request enviada");
    const { data } = await api.get(`/balance/${address}`);
    return new Address(data);
  },
};