<script lang="ts">
    import { getBlockInfo } from '../lib/api';
    import type { BlockInfo } from '../lib/types';
    import { Database, ArrowUpRight } from 'lucide-svelte';
     
    let blockNumber: number;
    let blockInfo: BlockInfo | null = null;
    let error: string | null = null;
   
    async function fetchBlockInfo() {
      try {
        error = null;
        blockInfo = await getBlockInfo(blockNumber);
      } catch (e: unknown) {
        error = e instanceof Error ? e.message : 'Erro desconhecido';
        blockInfo = null;
      }
    }
  </script>
  
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-semibold">Informações do Bloco</h2>
      {#if blockInfo}
        <span class="px-3 py-1 bg-orange-500/10 text-orange-400 rounded-full text-sm">
          Bloco #{blockInfo.height}
        </span>
      {/if}
    </div>
  
    <!-- Search -->
    <div class="flex gap-3">
      <input
        type="number"
        bind:value={blockNumber}
        placeholder="Número do bloco"
        class="flex-1 bg-slate-900/50 border border-slate-700 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-orange-500/50 focus:border-orange-500 transition-all"
      />
      <button
        on:click={fetchBlockInfo}
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
  
    {#if blockInfo}
      <!-- Block Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
          <div class="flex items-center gap-3">
            <Database size={20} class="text-orange-500 shrink-0" />
            <div class="min-w-0 w-full">
              <div class="text-sm text-slate-400">Hash</div>
              <div class="font-mono text-sm truncate" title={blockInfo.hash}>
                {blockInfo.hash}</div>
            </div>
          </div>
        </div>
        <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
          <div class="flex items-center gap-3">
            <Database size={20} class="text-orange-500" />
            <div>
              <div class="text-sm text-slate-400">Tamanho</div>
              <div class="font-semibold">{blockInfo.size} bytes</div>
            </div>
          </div>
        </div>
        <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
          <div class="flex items-center gap-3">
            <Database size={20} class="text-orange-500" />
            <div>
              <div class="text-sm text-slate-400">Transações</div>
              <div class="font-semibold">{blockInfo.transactions.length}</div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Transactions -->
      <div class="space-y-4">
        <h3 class="text-lg font-medium">Transações</h3>
        <div class="space-y-3">
          {#each blockInfo.transactions as tx}
            <div class="group p-4 bg-slate-900/30 rounded-lg border border-slate-700 hover:border-orange-500/50 transition-all duration-300">
              <div class="flex justify-between items-center">
                <div class="font-mono text-sm text-slate-400 truncate">
                  {tx.txid}
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-sm text-slate-400">{tx.total_output} BTC</span>
                  <ArrowUpRight 
                    size={16}
                    class="text-slate-500 group-hover:text-orange-500 transition-colors"
                  />
                </div>
              </div>
              <div class="mt-2 text-sm text-slate-500">
                Tamanho: {tx.size} bytes
              </div>
            </div>
          {/each}
        </div>
      </div>
    {/if}
  </div>

  <style>
    .truncate {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  </style>