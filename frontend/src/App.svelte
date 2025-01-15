<script lang="ts">
  import BlockInfo from './components/BlockInfo.svelte';
  import TransactionInfo from './components/TransactionInfo.svelte';
  import AddressBalance from './components/AddressBalance.svelte';
  import MempoolInfo from './components/MempoolInfo.svelte';
  import { Search, Box, ArrowUpRight, Clock, Database, Wallet } from 'lucide-svelte';
  import './app.css';

  let activeTab = 'block';
  let isSearchFocused = false;
  
  const tabs = [
    { id: 'block', icon: Box, label: 'Blocos' },
    { id: 'transaction', icon: ArrowUpRight, label: 'Transações' },
    { id: 'address', icon: Wallet, label: 'Endereços' },
    { id: 'mempool', icon: Clock, label: 'Mempool' }
  ];
</script>

<div class="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 text-slate-100 p-6">
  <div class="max-w-6xl mx-auto">
    <!-- Header -->
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold mb-2 bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 bg-clip-text text-transparent">
        Bitcoin Block Explorer
      </h1>
      <p class="text-slate-400">Explore a rede Bitcoin em tempo real</p>
    </div>

    <!-- Search Bar -->
    <div class="mb-8">
      <div class="relative transition-all duration-300" class:scale-105={isSearchFocused}>
        <input
          type="text"
          placeholder="Buscar por bloco, transação ou endereço..."
          class="w-full bg-slate-800/50 border border-slate-700 rounded-lg py-3 px-12 focus:outline-none focus:ring-2 focus:ring-orange-500/50 focus:border-orange-500 transition-all"
          on:focus={() => isSearchFocused = true}
          on:blur={() => isSearchFocused = false}
        />
        <div class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
          <Search size={20} />
        </div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      {#each tabs as { id, icon: Icon, label }}
        <button
          on:click={() => activeTab = id}
          class="p-4 rounded-lg border transition-all duration-300 {
            activeTab === id 
              ? 'bg-gradient-to-br from-orange-500 to-amber-600 border-transparent text-white shadow-lg shadow-orange-500/20'
              : 'bg-slate-800/50 border-slate-700 hover:bg-slate-700/50'
          }"
        >
          <div class="flex flex-col items-center gap-2">
            <svelte:component this={Icon} size={24} />
            <span class="font-medium">{label}</span>
          </div>
        </button>
      {/each}
    </div>

    <!-- Content Area -->
    <div class="bg-slate-800/50 rounded-xl p-6 border border-slate-700 backdrop-blur-sm">
      {#if activeTab === 'block'}
        <BlockInfo />
      {:else if activeTab === 'transaction'}
        <TransactionInfo />
      {:else if activeTab === 'address'}
        <AddressBalance />
      {:else if activeTab === 'mempool'}
        <MempoolInfo />
      {/if}
    </div>
  </div>
</div>

<style>
  :global(.scale-105) {
    transform: scale(1.05);
  }
</style>