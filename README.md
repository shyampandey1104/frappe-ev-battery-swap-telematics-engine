# Frappe EV Fleet Battery Swapping & BMS Telematics Engine

[![Frappe Framework](https://img.shields.io/badge/Frappe-v15.x-blue.svg)](https://frappeframework.com/)
[![Clean Energy](https://img.shields.io/badge/EV-Battery%20as%20a%20Service-green.svg)]()
[![IoT Telematics](https://img.shields.io/badge/IoT-BMS%20Telemetry-orange.svg)]()
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📌 Executive Overview & Real-World Client Problem

The rapid transition of delivery fleets (quick commerce 2-wheelers and 3-wheelers) to electric vehicles relies on the **Battery-as-a-Service (BaaS)** swapping model.

Swapping station operators and fleet managers face severe operational challenges:
1. **Thermal Runaway Hazards:** Lithium-ion battery packs charging at high C-rates risk thermal runaway; failure to flag cells over 55°C causes catastrophic station fires.
2. **State of Charge (SoC) Dispute:** Drivers are frequently billed incorrectly if energy consumption is not metered dynamically based on battery capacity and returned vs dispensed charge.
3. **Battery Asset Shrinkage:** Operators lose track of battery serial numbers as packs circulate continuously between vehicles, stations, and charging bays.

This Frappe application delivers an intelligent Battery Swapping Station Management System integrating IoT BMS telemetry with driver wallet billing.

---

## 🏛️ System Architecture Flow

```mermaid
flowchart TD
    A["EV Driver Arrives at Swap Station"] -->|Plug In Drained Battery| B["Station Smart Dock (BMS Ingestion)"]
    B -->|Check Pack Temp & State of Health (SoH)| C{"Safety Audit (Temp <= 55°C?)"}
    C -->|Temp > 55°C (Overheating)| D["Station Interlock: Pack Placed in Quarantine"]
    C -->|Temp Safe| E["Read Return State of Charge (e.g. 15%)"]
    E -->|Select Fully Charged Pack (SoC >= 90%)| F["Dispense Ready Battery"]
    F -->|Calculate Consumed Energy (kWh)| G["Driver Wallet Billing Engine"]
    G -->|Debit Wallet Balance| H["ERPNext POS Invoice & Transaction Receipt"]
    H -->|Driver Dispatched (<90s)| I["Station Inventory State Updated"]
```

---

## 🚀 Key Engineering Capabilities

- **Real-Time BMS Telemetry Ingestion:** Monitors voltage, current, cell temperatures, SoC, and SoH per battery pack.
- **Thermal Safety Interlocks:** Automatically locks out defective or overheating packs from being dispensed.
- **Dynamic Energy Metering:** Calculates exact kWh consumed per swap and applies dynamic tariff rules.
- **Prepaid Driver Wallet Engine:** Seamlessly deducts swap charges from driver accounts with automated low-balance SMS warnings.

---

## 📂 Frappe DocType Schema & Data Structure

```text
ev_battery_swap/
├── ev_battery_swap_core/
│   ├── doctype/
│   │   ├── smart_battery_pack/
│   │   │   ├── smart_battery_pack.json
│   │   │   ├── smart_battery_pack.py
│   │   │   └── smart_battery_pack.js
│   │   └── battery_swap_log/
│   │       └── battery_swap_log.json
│   └── workspace/
│       └── ev_battery_swap_workspace/
│           └── ev_battery_swap_workspace.json
```

---

## ⚡ Frappe Hooks & Whitelisted APIs

- **REST Endpoint:** `POST /api/method/ev_battery_swap.api.register_battery_telemetry`
- **Whitelisted Method:** `@frappe.whitelist() def execute_battery_swap(vehicle_id, returned_pack_id, driver_wallet_balance_inr)`
- **Hooks Event:** `scheduler_events.hourly` audits battery fleet degradation and SoH trends.

---

## 🛠️ Installation & Bench Setup

```bash
bench get-app https://github.com/shyampandey1104/frappe-ev-battery-swap-telematics-engine
bench --site erp.yourdomain.com install-app ev_battery_swap
bench --site erp.yourdomain.com migrate
python3 -m unittest discover tests
```

---

## 📄 License
MIT License. Built for EV OEM manufacturers, logistics fleet operators, and energy infrastructure providers.
