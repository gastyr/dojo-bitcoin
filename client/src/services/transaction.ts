import { api } from 'src/boot/axios';
import { Transaction } from 'src/models/Transaction';

export const transactionService = {
  async getTransaction(txid: string): Promise<Transaction> {
    const { data } = await api.get(`/transactions/${txid}`);
    return new Transaction(data);
  },
};