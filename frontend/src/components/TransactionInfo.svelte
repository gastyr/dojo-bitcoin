<script lang="ts">
    import { getTransaction } from '../lib/api';
    import type { TransactionInfo } from '../lib/types';
    import { ArrowUpRight, Binary, Coins, Hash } from 'lucide-svelte';
   
    let txHash: string = '';
    let transaction: TransactionInfo | null = null;
    let error: string | null = null;
 
    async function fetchTransaction() {
      try {
        error = null;
        transaction = await getTransaction(txHash);
      } catch (e: unknown) {
        error = e instanceof Error ? e.message : 'Erro desconhecido';
        transaction = null;
      }
    }
</script>

<div class="space-y-6">
  <div class="flex items-center justify-between">
    <h2 class="text-xl font-semibold">Informações da Transação</h2>
    {#if transaction}
      <span class="px-3 py-1 bg-orange-500/10 text-orange-400 rounded-full text-sm flex items-center gap-2">
        <Coins size={14} />
        {transaction.fee} BTC
      </span>
    {/if}
  </div>

  <!-- Search -->
  <div class="flex gap-3">
    <div class="relative flex-1">
      <input
        type="text"
        bind:value={txHash}
        placeholder="Hash da transação"
        class="w-full bg-slate-900/50 border border-slate-700 rounded-lg py-2 pl-10 pr-4 focus:outline-none focus:ring-2 focus:ring-orange-500/50 focus:border-orange-500 transition-all font-mono"
      />
      <Hash size={18} class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
    </div>
    <button
      on:click={fetchTransaction}
      class="px-6 py-2 bg-gradient-to-r from-orange-500 to-amber-600 rounded-lg font-medium hover:opacity-90 transition-opacity"
    >
      Buscar
    </button>
  </div>

  {#if error}
    <div class="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-lg">
      {error}
    </div>
  {/if}

  {#if transaction}
    <!-- Transaction Details -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
        <div class="flex items-center gap-3">
          <Hash size={20} class="text-orange-500" />
          <div class="overflow-hidden">
            <div class="text-sm text-slate-400">TxID</div>
            <div class="font-mono text-sm truncate" title={transaction.txid}>
              {transaction.txid}
            </div>
          </div>
        </div>
      </div>
      
      <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
        <div class="flex items-center gap-3">
          <Binary size={20} class="text-orange-500" />
          <div>
            <div class="text-sm text-slate-400">Tamanho</div>
            <div class="font-semibold">{transaction.size.toLocaleString()} bytes</div>
          </div>
        </div>
      </div>
      
      <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
        <div class="flex items-center gap-3">
          <Coins size={20} class="text-orange-500" />
          <div>
            <div class="text-sm text-slate-400">Taxa</div>
            <div class="font-semibold">{transaction.fee} BTC</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Additional Transaction Details (if available in your API) -->
    {#if transaction.inputs && transaction.outputs}
      <div class="space-y-4 mt-6">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium">Detalhes da Transação</h3>
          <div class="flex items-center gap-2 text-sm text-slate-400">
            <ArrowUpRight size={16} class="text-orange-500" />
            Ver no Blockchain
          </div>
        </div>
        
        <!-- You can add more transaction details here like inputs/outputs -->
      </div>
    {/if}
  {/if}
</div>