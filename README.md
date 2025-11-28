# Buy Me a Coffee (Vyper)

A **Vyper-based Ethereum funding contract** that allows users to “buy a coffee” (donate ETH) to the contract owner. The project includes full testing and deployment scripts, as well as a mock Chainlink price feed for local development. 

---

## 📝 Project Overview

This project implements a simple funding system where users can send ETH donations to the owner. Key features:

* **No maximum donation limit**
* **Minimum donation is $5 USD** (evaluated dynamically using a Chainlink price feed)
* Compatible with **Ethereum testnets or local blockchain**
* Fully testable with a **unit test** and **staging test**

---

## 📂 Contracts

### **1. Buy_me_a_coffee.vy**

Main funding contract:

* Users call the `fund` function to donate ETH
* Donation amount is validated against a **USD minimum ($5)** using a Chainlink price feed
* Owner can withdraw funds at any time

### **2. Get_price_module.vy**

Utility contract:

* Provides conversion of ETH to USD
* Interfaces with Chainlink price feed for accurate rate calculation
* Uses Moccasin's "manifest named" feature to deploy the contract with a price feed specified in the moccasin.toml

### **3. mock_v3_aggregator.vy (Mock)**

Used for testing and local deployment:

* Simulates a Chainlink price feed
* Implements the `AggregatorV3Interface` so that tests can run without requiring a live oracle

---

## 🛠 Scripts

All scripts are written in **Python**, using the Vyper ecosystem:

* `deploy_contract.py` — Deploys `Buy_me_a_coffee.vy` to a blockchain
* `deploy_mock.py` — Deploys the `Aggregator.vy` mock for local testing
* `withdraw.py` — Withdraws ETH from the deployed contract
* Testing scripts (`tests/`) — Include **unit tests** and **staging tests**

---

## ✅ Testing

* **Unit Tests:** Quick local tests using mocks for price feeds
* **Staging Tests:** Run against testnets to verify real oracle integration
* Run tests with your preferred Python testing framework (e.g., `pytest`)

Example:

```bash
pytest tests/
```

---

## 💻 Usage

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/buy_me_a_coffee.git
cd buy_me_a_coffee
```

2. Install any dependencies (if needed) — currently, this project does not require external packages.

3. Deploy a mock aggregator locally:

```bash
python deploy_mock.py
```

4. Deploy the main contract:

```bash
python deploy_contract.py
```

5. Fund the contract:

```python
# Example Python script
fund_contract(amount_in_eth)
```

6. Withdraw funds (owner only):

```bash
python withdraw.py
```

---

## 📐 Project Structure

```
buy_me_a_coffee/
├── contracts/
│   ├── Buy_me_a_coffee.vy
│   ├── Get_price_module.vy
│   └── Aggregator.vy
├── interfaces/
│   └── AggregatorV3Interface.vyi
├── scripts/
│   ├── deploy_contract.py
│   ├── deploy_mock.py
│   └── withdraw.py
├── tests/
│   ├── unit/
│   └── staging/
└── README.md
```

---

## 📄 License

This project is MIT licensed — feel free to use and modify it.

---

## ⚡ Notes

* The project is a **Moccasin template**, ideal for experimenting with Vyper contracts and Chainlink integration.
* Always verify contract addresses and price feeds before using real ETH on mainnet.


## Quickstart

1. Deploy to a fake local network that titanoboa automatically spins up!

```bash
mox run deploy
```

2. Run tests

```
mox test
```

_For documentation, please run `mox --help` or visit [the Moccasin documentation](https://cyfrin.github.io/moccasin)_
