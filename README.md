# Vending Machine Simulator

## 🧾 Overview

The Vending Machine OOP System is a comprehensive object-oriented simulation developed to demonstrate professional software engineering practices. This project implements a complete vending machine ecosystem without graphical interfaces, focusing exclusively on clean architecture, SOLID principles, and comprehensive testing.

## ⚙️ Key Features

### 🏗️ Object-Oriented Design

- **SOLID Principles Implementation** – All five SOLID principles applied throughout the architecture
- **Clean Architecture** – Four-layer separation (UI, Services, Core, Models)
- **Design Patterns** – Abstract Factory (Drinks), Facade (VendingMachine), Strategy (PaymentService)

### 🍹 Drink Management System

- **Extensible Drink Hierarchy** – Abstract Drink base class with Soda, Juice, Water subclasses
- **Polymorphic Behavior** – Each drink type provides unique descriptions and properties
- **Stock Management** – Real-time quantity tracking with restocking capabilities

### 💳 Payment Processing

- **Payment Service Abstraction** – Interface-based design supporting multiple payment methods
- **Cash Payment Implementation** – Complete cash handling with change calculation
- **Extensible for Future Methods** – Credit card, mobile payments can be added easily

### 📊 Transaction Management

- **Complete Transaction History** – Records all purchases, failures, and cancellations
- **Real-time Statistics** – Sales totals, success rates, and operational metrics
- **Audit Trail** – Detailed logging for debugging and analysis

### 🧪 Comprehensive Testing

- **50+ Unit & Integration Tests** – Full test coverage across all components
- **Exception Testing** – Edge cases and error scenarios thoroughly validated
- **Integration Testing** – End-to-end workflows verified

### 🛡️ Robust Error Handling

- **Custom Exception Hierarchy** – Domain-specific exceptions for clear error reporting
- **Graceful Failure Recovery** – Failed transactions don't corrupt system state
- **Input Validation** – All user inputs validated with meaningful feedback

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher

### Running the Simulator

```bash
python run.py
```

### How to Use

Once the simulator starts, you will see a menu with the following options:

| Option | Action |
|--------|--------|
| 1 | View available drinks and prices |
| 2 | Insert money (enter amount in dollars) |
| 3 | Select and purchase a drink by code |
| 4 | View transaction statistics |
| 5 | Refund your money and exit |
| 6 | Enter Admin Mode |
| 7 | Quit |

**Example workflow:**
1. Press `1` to view the menu
2. Press `2` and enter `2.00` to insert $2.00
3. Press `3` and enter `A1` to buy a Coca-Cola
4. Collect your drink and change!

### Admin Mode

Access the admin panel to manage inventory and view reports.

**Password:** `admin123`

**Admin Features:**
- View detailed inventory with categories
- Restock existing items
- Add new drinks (Soda, Juice, Water)
- View full transaction history
- View sales statistics

### Running the Tests

```bash
python run_tests.py
```

## 📁 Project Structure

```
assignment/
├── run.py              # Main entry point
├── run_tests.py        # Test runner
├── README.md           # This file
├── src/
│   └── vending_machine/
│       ├── core/       # VendingMachine controller
│       ├── models/     # Drink hierarchy, Inventory
│       ├── services/   # Payment, Transactions
│       ├── ui/         # Display, Menu
│       └── utils/      # Custom exceptions
└── tests/
    ├── test_drinks.py
    ├── test_inventory.py
    ├── test_payment.py
    ├── test_transactions.py
    ├── test_machine.py
    └── test_integration.py
```


**Author**:Ayanda Phaketsi 
**Date**: 2026
