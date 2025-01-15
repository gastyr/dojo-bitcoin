<script lang="ts">
  import { getMempoolInfo } from '../lib/api';
  import type { MempoolInfo } from '../lib/types';
  import { Clock, HardDrive, Database, Coins } from 'lucide-svelte';
 
  let mempoolInfo: MempoolInfo | null = null;
  let error: string | null = null;

  async function fetchMempoolInfo() {
    try {
      error = null;
      mempoolInfo = await getMempoolInfo();
    } catch (e: unknown) {
      error = e instanceof Error ? e.message : 'Erro desconhecido';
      mempoolInfo = null;
    }
  }

  // Atualiza a cada 30 segundos
  setInterval(fetchMempoolInfo, 30000);
 
  // Carrega dados iniciais
  fetchMempoolInfo();
</script>

<div class="space-y-6">
<div class="flex items-center justify-between">
  <h2 class="text-xl font-semibold">Informações da Mempool</h2>
  {#if mempoolInfo}
    <span class="px-3 py-1 bg-orange-500/10 text-orange-400 rounded-full text-sm flex items-center gap-2">
      <Clock size={14} />
      Atualizado agora
    </span>
  {/if}
</div>

{#if error}
  <div class="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-lg">
    {error}
  </div>
{/if}

{#if mempoolInfo}
  <!-- Mempool Stats -->
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
      <div class="flex items-center gap-3">
        <Database size={20} class="text-orange-500" />
        <div>
          <div class="text-sm text-slate-400">Transações Pendentes</div>
          <div class="font-semibold">{mempoolInfo.size.toLocaleString()}</div>
        </div>
      </div>
    </div>
    
    <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
      <div class="flex items-center gap-3">
        <HardDrive size={20} class="text-orange-500" />
        <div>
          <div class="text-sm text-slate-400">Tamanho Total</div>
          <div class="font-semibold">{(mempoolInfo.bytes / 1024 / 1024).toFixed(2)} MB</div>
        </div>
      </div>
    </div>
    
    <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
      <div class="flex items-center gap-3">
        <HardDrive size={20} class="text-orange-500" />
        <div>
          <div class="text-sm text-slate-400">Uso de Memória</div>
          <div class="font-semibold">{Math.round(mempoolInfo.usage / 1024 / 1024)} MB</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Recent Transactions -->
  <div class="space-y-4">
    <h3 class="text-lg font-medium">Transações Recentes</h3>
    <div class="space-y-3">
      {#each mempoolInfo.transactions as tx}
        <div class="group p-4 bg-slate-900/30 rounded-lg border border-slate-700 hover:border-orange-500/50 transition-all duration-300">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-2">
            <div class="font-mono text-sm text-slate-400 truncate">
              {tx.txid}
            </div>
            <div class="flex items-center gap-4">
              <div class="flex items-center gap-2">
                <HardDrive size={16} class="text-slate-500" />
                <span class="text-sm text-slate-400">{tx.size} bytes</span>
              </div>
              <div class="flex items-center gap-2">
                <Coins size={16} class="text-orange-500" />
                <span class="text-sm text-orange-400">{tx.fee} BTC</span>
              </div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>
{/if}
</div>