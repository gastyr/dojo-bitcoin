export const mockData = {
  block: {
    height: 800000,
    hash: "000000000000000000024bead8df69990852c202db0e0097c1a12ea637d7e96d",
    time: 1690987654,
    nonce: 123456789,
    difficulty: 53911173001054.59,
    num_transactions: 2876,
    size: 1567832,
    weight: 3993405,
    merkle_root: "d9f12c2644d4d6c123c69b86d3c948a452070b8ffa01f5510f0927c8bb273206",
    transactions: [
      {
        txid: "7a5b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7",
        size: 225,
        vsize: 225,
        fee: 0.00015,
        input_count: 1,
        output_count: 2,
        total_output: 6.25
      }
    ]
  },

  transaction: {
    txid: "7a5b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7",
    size: 225,
    vsize: 225,
    fee: 0.00015,
    input_count: 1,
    output_count: 2,
    total_output: 6.25,
    inputs: [
      {
        txid: "8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b",
        vout: 0,
        address: "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
        value: 6.25015
      }
    ],
    outputs: [
      {
        address: "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
        value: 6.25,
        script_type: "witness_v0_keyhash"
      },
      {
        address: "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4",
        value: 0.00015,
        script_type: "witness_v0_keyhash"
      }
    ]
  },

  address: {
    address: "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
    network: "mainnet",
    balance: 12.34567890,
    unspent_count: 3,
    unspent_outputs: [
      {
        txid: "7a5b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7",
        vout: 0,
        amount: 5.0,
        confirmations: 123,
        height: 800000
      }
    ]
  },

  mempool: {
    size: 15234,
    bytes: 23456789,
    usage: 67890123,
    transactions: [
      {
        txid: "7a5b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7",
        size: 225,
        fee: 0.00015,
        time: 1690987654
      },
      {
        txid: "8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b",
        size: 332,
        fee: 0.00022,
        time: 1690987653
      }
    ]
  }
};