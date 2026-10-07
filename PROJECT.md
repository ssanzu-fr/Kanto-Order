# KANTO ORDERS: PROJECT

> Vision and school requirements. Read after `AI_CONTEXT.md`. Rules and architecture live in `AI_CONTEXT.md`, progress lives in `TASKS.md`.

---

# 1. SCHOOL REQUIREMENTS (Machine Problem)

**Project title:** Simple Business Process Management System

**Project problem:** Online Food Ordering Process

The system must follow this process:

```
Customer Places Order
 ↓
Enter Food Order
 ↓
Calculate Total Amount
 ↓
Check Payment Status
 ↓
Paid?
  NO  → Pending Payment
  YES → Order Confirmed
 ↓
Prepare Order
 ↓
Order Ready
 ↓
Order Completed
```

The program must display something similar to:

```
Customer: Maria Santos
Order No.: 001
Food: Chicken Meal
Price: ₱120
Payment: PAID
Order Status: COMPLETED
```

The final documentation must contain:

1. Project title
2. Business problem
3. Description of the process
4. How the program solves the problem
5. Programming language used and why
6. Short conclusion

---

# 2. MAIN GOAL

> Show the online food ordering process as a working program where every step is visible, enforced and saved.

A kanto food stall is a natural fit: customers order, pay, wait, and get their food. The program turns that real routine into a controlled process so no order is lost, skipped or prepared without payment.

---

# 3. DOCUMENTATION DRAFT (reused in Phase 9)

## Business problem

A small food business that takes orders manually (by shouting, notebooks or chat messages) loses track of orders. Orders get forgotten, food is prepared before it is paid, totals are miscalculated, and nobody knows an order's current status.

## Description of the process

1. The customer places an order and gives their name.
2. The food order is entered (items and quantities).
3. The total amount is calculated.
4. The payment status is checked.
5. If unpaid, the order stays in **Pending Payment**. If paid, it becomes **Confirmed**.
6. The order is prepared (**Preparing**), then marked **Ready**.
7. When the customer receives it, the order is **Completed**.

## How the program solves the problem

- Every order gets a unique order number and a visible status.
- Totals are calculated by the program, never by hand.
- The workflow only allows forward steps, and an unpaid order can never be prepared.
- Orders are saved to a JSON file, so records survive closing the app.
- The receipt shows customer, order number, food, price, payment and status in one place.

## Programming language and why

Python with customtkinter: readable syntax, strong support for object-oriented design, a built-in way to build desktop interfaces, no web server needed, and it runs on any school computer. JSON gives simple, human-readable storage that is easy to inspect during checking.

## Conclusion (to be finalized after testing)

The system shows how a simple business process can be modeled, enforced and tracked with an object-oriented program, using a familiar Filipino food stall as the setting.

---

# 4. THE PROCESS AS CODE

Status flow:

```
PENDING_PAYMENT → CONFIRMED → PREPARING → READY → COMPLETED
```

| Process step          | Where it happens in the program                   |
| --------------------- | ------------------------------------------------- |
| Customer places order | Order form: customer name                         |
| Enter food order      | Order form: menu and cart                         |
| Calculate total       | `OrderService`                                    |
| Check payment status  | `PaymentService`                                  |
| Paid? NO              | Status `PENDING_PAYMENT`, button **Mark as Paid** |
| Paid? YES             | Status `CONFIRMED`                                |
| Prepare order         | Button **Start Preparing** → `PREPARING`          |
| Order ready           | Button **Mark Ready** → `READY`                   |
| Order completed       | Button **Complete Order** → `COMPLETED`           |

Payment choice on the order form: **Pay now** (order starts `CONFIRMED`) or **Pay later** (order starts `PENDING_PAYMENT`).

---

# 5. MENU (prices are adjustable, ask before changing)

| Category      | Item              | Price |
| ------------- | ----------------- | ----- |
| Rice and Soup | Lugaw             | ₱35   |
| Rice and Soup | Goto              | ₱50   |
| Rice and Soup | Mami              | ₱65   |
| Rice and Soup | Pares             | ₱80   |
| Rice and Soup | Chicken Meal      | ₱120  |
| Street Food   | Kwek-kwek (5 pcs) | ₱30   |
| Street Food   | Fishball (10 pcs) | ₱20   |
| Street Food   | Isaw (2 sticks)   | ₱25   |
| Street Food   | Pagpag            | ₱45   |
| Drinks        | Sago't Gulaman    | ₱25   |
| Drinks        | Buko Juice        | ₱35   |
| Drinks        | Iced Tea          | ₱25   |

Chicken Meal at ₱120 matches the sample in the instructions.

---

# 6. THEME: NIGHT MARKET, WITH BATS

Feels: a street stall lit by lanterns after dark. Warm, readable, a little rustic. Not cluttered.

## Palette direction (final hex chosen in Phase 4, stored only in `ui/theme.py`)

| Role             | Direction                                                  |
| ---------------- | ---------------------------------------------------------- |
| Background       | deep night blue-black                                      |
| Panels           | slightly lighter dark with a warm tint                     |
| Primary accent   | lantern yellow                                             |
| Secondary accent | chili red                                                  |
| Text             | warm cream                                                 |
| Status colors    | one distinct, muted color per status (used on badges only) |

## Fonts

- Headings: **Bungee**
- Body: **Nunito**
- Bundled in `assets/fonts/`, loaded in `ui/fonts.py`, with a safe fallback if loading fails.

## Bats

- One bat silhouette logo (PNG, transparent), drawn locally with Pillow or supplied as an asset.
- Small bat accents only where they add meaning: header, empty order list, maybe the Completed badge.
- No online images. Works offline.

## Avoid

- Emoji as decoration or as bat icons
- Neon glow everywhere, heavy gradients
- Equal-weight card grids and everything centered
- Decorative elements that do nothing

---

# 7. SCREEN PLAN (single window)

```
┌────────────────────────────────────────────────────────────┐
│ [bat]  KANTO ORDERS                      Orders today: 4   │
├───────────────────────────┬────────────────────────────────┤
│ NEW ORDER                 │ ORDERS      [All|Pending|...]  │
│ Customer: [___________]   │ ┌────────────────────────────┐ │
│ [Rice&Soup][Street][Drink]│ │ 001 Maria Santos  [PAID]   │ │
│  Lugaw      ₱35  [- 1 +]  │ │ Chicken Meal x1    ₱120    │ │
│  Goto       ₱50  [- 0 +]  │ │ Status: READY  [Complete]  │ │
│  ...                      │ └────────────────────────────┘ │
│ Cart                      │ ┌────────────────────────────┐ │
│  Lugaw x2          ₱70    │ │ 002 Juan  [UNPAID]         │ │
│ Total:            ₱70     │ │ Status: PENDING [Mark Paid]│ │
│ Payment: (o) Now ( ) Later│ └────────────────────────────┘ │
│ [ PLACE ORDER ]           │                                │
├───────────────────────────┴────────────────────────────────┤
│ RECEIPT (selected order)                                   │
└────────────────────────────────────────────────────────────┘
```

Left is for creating orders, right is for managing them, bottom shows the receipt of the selected order. Final layout may be adjusted in Phase 4 after asking.

---

# 8. DECISIONS ALREADY MADE

- Python + customtkinter + Pillow + JSON
- Object-oriented, one file per responsibility
- Night market theme with a drawn bat logo, no emoji bats
- Fonts: Bungee (headings), Nunito (body)
- Cart with quantities, as long as the required process and receipt stay intact
- Menu includes rice and soup, street food and drinks
- Orders saved in `data/orders.json`, reloaded on startup

# 9. OPEN DECISIONS (ask the user when the phase needs them)

- Final app name (currently "Kanto Orders")
- Final hex palette and exact layout (Phase 4)
- How the bat logo is made: drawn by code with Pillow, or a supplied PNG (Phase 7)
- Whether to include a "Clear all orders" reset button for demos (Phase 6)
- Menu prices (Phase 2)
