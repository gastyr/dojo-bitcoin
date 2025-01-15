<script lang="ts">
    import { getAddressBalance } from '../lib/api';
    import type { AddressBalance } from '../lib/types';
    import { Wallet, CreditCard, Database } from 'lucide-svelte';
     
    let address: string = '';
    let balance: AddressBalance | null = null;
    let error: string | null = null;
   
    async function fetchBalance() {
      try {
        error = null;
        balance = await getAddressBalance(address);
      } catch (e: unknown) {
        error = e instanceof Error ? e.message : 'Erro desconhecido';
        balance = null;
      }
    }
  </script>
  
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-semibold">Saldo do Endereço</h2>
      {#if balance}
        <span class="px-3 py-1 bg-orange-500/10 text-orange-400 rounded-full text-sm">
          {balance.balance} BTC
        </span>
      {/if}
    </div>
  
    <!-- Search -->
    <div class="flex gap-3">
      <input
        type="text"
        bind:value={address}
        placeholder="Endereço Bitcoin"
        class="flex-1 bg-slate-900/50 border border-slate-700 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-orange-500/50 focus:border-orange-500 transition-all"
      />
      <button
        on:click={fetchBalance}
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
  
    {#if balance}
      <!-- Address Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
          <div class="flex items-center gap-3">
            <Wallet size={20} class="text-orange-500" />
            <div>
              <div class="text-sm text-slate-400">Endereço</div>
              <div class="font-mono text-sm truncate">{balance.address}</div>
            </div>
          </div>
        </div>
        
        <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
          <div class="flex items-center gap-3">
            <CreditCard size={20} class="text-orange-500" />
            <div>
              <div class="text-sm text-slate-400">Saldo</div>
              <div class="font-semibold">{balance.balance} BTC</div>
            </div>
          </div>
        </div>
        
        <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
          <div class="flex items-center gap-3">
            <Database size={20} class="text-orange-500" />
            <div>
              <div class="text-sm text-slate-400">UTXOs</div>
              <div class="font-semibold">{balance.unspent_count}</div>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>