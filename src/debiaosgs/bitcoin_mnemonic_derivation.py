#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.symbols import BTC as SYMBOL
import json


# Initialize Bitcoin mainnet HDWallet
hdwallet: HDWallet = HDWallet(symbol=SYMBOL, use_default_path=False)

# Get Bitcoin HDWallet from mnemonic
words = 'put your bitcoin mnemonic 12 words here'
hdwallet.from_mnemonic(words)

# Derivation from path
hdwallet.from_path("m/86'/0'/0'/1/3")

# Print all Bitcoin HDWallet information's
print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))