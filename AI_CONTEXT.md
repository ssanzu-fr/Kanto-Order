# KANTO ORDERS — AI HANDOFF CONTEXT

## READ THIS FIRST

This file is the priority document for any AI agent working on this project.

Reading order:

1. `AI_CONTEXT.md` (this file): rules, stack, structure, phases
2. `PROJECT.md`: the vision, the school requirements, the process, the theme
3. `TASKS.md`: what is done and what is next

Do not restart the planning process. The plan is already decided.
The user wants to BUILD the project and learn through implementation.
The user prefers concise, direct answers. Give complete practical steps when needed, but do not repeat things already established.
Do not make major project decisions without asking.

---

# PROJECT

**School title:** Simple Business Process Management System
**Business problem:** Online Food Ordering Process
**Working app name:** Kanto Orders (a placeholder, ask the user before changing it)

A small desktop application for a school Machine Problem. It models a Filipino "kanto" food stall (lugaw, pares, mami, street food) and walks every order through a fixed business process.

Project philosophy:

> A polished, realistic small business application. Not an unnecessarily large system.

---

# STACK

- Python 3.10+
- customtkinter (UI)
- Pillow (images, the bat logo)
- JSON file for saving orders (`data/orders.json`)
- `unittest` for service tests (Phase 8)

DO NOT switch to PyQt, Flask, web frameworks, or a database.
DO NOT add dependencies beyond the list above without asking.

---

# ARCHITECTURE RULE (MOST IMPORTANT)

The user explicitly does NOT want one giant file.

- **UI never calculates or decides anything.** It only calls services and displays results.
- **Services hold the business logic** and work on models.
- **Models are plain data classes** (dataclasses and enums). No UI code, no file I/O.
- **Storage is isolated** in one service. Nothing else touches the JSON file.
- One responsibility per file. If a file grows past roughly 200 lines, ask whether to split it.

---

# PROJECT STRUCTURE

```
kanto-orders/
├── AI_CONTEXT.md
├── PROJECT.md
├── TASKS.md
├── PROMPTS.md
├── requirements.txt
├── main.py                  # entry point only, launches the app
├── models/
│   ├── __init__.py
│   ├── enums.py             # OrderStatus, PaymentStatus
│   ├── menu_item.py         # MenuItem: id, name, price, category
│   ├── order_item.py        # OrderItem: menu item + quantity, subtotal
│   ├── order.py             # Order: order no., customer, items, status, payment
│   └── payment.py           # Payment: amount, status
├── services/
│   ├── __init__.py
│   ├── order_service.py     # create order, add items, calculate total
│   ├── payment_service.py   # check / mark payment status
│   ├── workflow_service.py  # moves an order through the allowed statuses
│   └── storage_service.py   # load/save data/orders.json
├── data/
│   ├── menu.py              # the menu list
│   └── orders.json          # saved orders (created at runtime)
├── ui/
│   ├── __init__.py
│   ├── theme.py             # colors, fonts, sizes
│   ├── fonts.py             # loads bundled font files
│   ├── app.py               # main window and layout
│   ├── header.py            # title bar with bat logo
│   ├── order_form.py        # customer name, menu, cart
│   ├── order_list.py        # list of orders and status buttons
│   └── receipt_view.py      # receipt in the required format
├── assets/
│   ├── fonts/               # Bungee, Nunito (.ttf)
│   └── images/              # bat logo and accents
└── tests/
    └── test_services.py
```

If the real structure differs, trust the real files, inspect first, and tell the user about the difference.

---

# THE PROCESS (DO NOT ALTER)

This is the exact required business process. It is graded.

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

Status flow in code:

```
PENDING_PAYMENT → CONFIRMED → PREPARING → READY → COMPLETED
```

Rules:

- A new order starts as `PENDING_PAYMENT` with payment `UNPAID`, unless paid at creation.
- Paying moves `PENDING_PAYMENT` → `CONFIRMED`.
- An unpaid order can NEVER be prepared, made ready, or completed.
- Statuses only move forward one step at a time. No skipping, no going back.
- The total is always calculated by `OrderService`, never typed in by hand or computed in the UI.

Required display format (the receipt must match this):

```
Customer: Maria Santos
Order No.: 001
Food: Chicken Meal
Price: ₱120
Payment: PAID
Order Status: COMPLETED
```

With several items, the `Food` and `Price` lines list each item (name, quantity, subtotal) followed by a total. The six labelled fields must always be present and in this order.

Order numbers are zero-padded to 3 digits (001, 002, ...) and continue from the highest saved number after a restart.

---

# SCOPE

## MVP

- Enter a customer name
- Pick items from the menu with quantities (cart)
- Calculate total
- Pay / mark as paid
- Advance status step by step
- Orders list with live statuses
- Receipt in the required format
- Save and load orders from JSON

## Do NOT add unless explicitly requested

- Login or authentication
- Real payment integration
- Database
- Networking or web server
- Inventory management
- Multiple users or roles
- Printing or exporting to PDF

## Menu

Lugaw, goto, mami, pares, kwek-kwek, fishball, isaw, pagpag, plus drinks: sago't gulaman, buko juice, iced tea. Prices in ₱ live only in `data/menu.py`.

---

# VISUAL DIRECTION

> Night market, with bats.

Feels: dark, warm, lantern-lit, a little rustic, readable, uncluttered.

- Dark background, lantern-yellow and chili-red accents, cream text
- Heading font: **Bungee** (neon-sign feel). Body font: **Nunito**. Both bundled in `assets/fonts/`
- One drawn bat silhouette as the logo, plus small bat accents in the header and empty states
- Bat images are bundled locally. No online images, the app must work offline

Avoid:

- Emoji used as decoration. Tkinter renders emoji unreliably on Windows, and heavy emoji looks AI-generated
- Neon overload, excessive gradients, clutter
- Generic AI-looking layouts
- Everything-centered, equal-weight card grids

Details are in `PROJECT.md`.

---

# DEVELOPMENT PHASES

Work one phase at a time. Never start the next phase until the user says so. Each phase ends with its "Done when" check and a ticked `TASKS.md`.

## PHASE 1: SETUP

Build:

- Project folder, venv, `requirements.txt` (customtkinter, Pillow)
- Folder skeleton with `__init__.py` files, `.gitignore`
- Bungee and Nunito `.ttf` files in `assets/fonts/`
- `main.py` opening an empty customtkinter window

Do NOT: write models, services or real UI yet.
Done when: `python main.py` opens an empty window and the skeleton matches the structure above.

## PHASE 2: MODELS AND MENU DATA

Build:

- `enums.py` (OrderStatus, PaymentStatus)
- `MenuItem`, `OrderItem`, `Payment`, `Order` as dataclasses with type hints
- `data/menu.py` with all 12 menu items

Do NOT: put UI code or file I/O in models.
Done when: an `Order` with items can be created and printed from a Python shell.

## PHASE 3: SERVICES

Build:

- `OrderService`: create order, add items, calculate total, 3-digit order numbers
- `PaymentService`: check and mark payment status
- `WorkflowService`: forward-only, one step at a time, unpaid can never be prepared
- `StorageService`: save and load `orders.json`, survive a missing or corrupted file

Do NOT: touch the UI. Services must run and be testable without it.
Done when: a terminal script runs the full process from Place Order to Completed, blocked transitions raise clear errors, and orders reload from JSON.

## PHASE 4: UI SHELL AND THEME

Build:

- `theme.py` (palette, fonts, sizes), `fonts.py` (safe fallback)
- `app.py` (window and layout frames), `header.py` (text only for now)

Ask first: palette options, layout approval, final app name, window size.
Do NOT: build the order form, add bats or emoji yet.
Done when: the dark themed layout shows with correct fonts and empty panels, no console errors.

## PHASE 5: ORDER FORM AND CART

Build:

- Customer name, menu by category, quantity controls
- Cart with running total taken from `OrderService` (UI never calculates)
- Pay now / Pay later, Place Order saving through services
- Validation for empty name and empty cart

Do NOT: build the order list or receipt yet.
Done when: placing an order writes the correct total and status to `orders.json` and bad input is rejected politely.

## PHASE 6: ORDER LIST, STATUS BUTTONS, RECEIPT

Build:

- One order card per order with status badge
- Action buttons: Mark as Paid, Start Preparing, Mark Ready, Complete Order
- Status filter, optional "Clear all orders" for demos (confirm dialog)
- `receipt_view.py` in the exact required format

Do NOT: change service rules to make the UI easier.
Done when: one order can be clicked from Pending Payment to Completed, the receipt matches the required format, and data survives a restart.

## PHASE 7: BAT AND THEME POLISH

Build:

- Bat silhouette logo (PNG, local), header placement
- Bat accent in the empty state, a few meaningful places only
- Consistent status badge colors, spacing, hover and focus states

Do NOT: change service logic, add emoji decoration, or add decorative elements that do nothing.
Done when: the app looks intentional and themed, and passes the "avoid" list in VISUAL DIRECTION.

## PHASE 8: TESTING

Build:

- `tests/test_services.py` (total, payment, workflow, storage, corrupted JSON)
- Manual run of the full process and edge cases (empty name, empty cart, restart, long names, many orders)

Do NOT: fix bugs silently. Report them first.
Done when: all tests pass, the manual checklist passes, and the receipt matches the required format.

## PHASE 9: SCHOOL DOCUMENTATION AND SUBMISSION

Build:

- Final documentation with the 6 required sections (title, business problem, process description, how the program solves it, language and why, short conclusion)
- Process diagram, screenshot list (one per status), demo script with sample orders
- Clean project folder for submission

Do NOT: copy the plan blindly. Document what was actually built.
Done when: the documentation matches the finished program and the folder is clean.

## PHASE FLOW

```
SETUP -> MODELS -> SERVICES -> UI SHELL -> ORDER FORM -> ORDER LIST + RECEIPT
      -> POLISH -> TESTING -> DOCUMENTATION
```

Track progress in `TASKS.md`. When a phase is finished, tick its boxes and update the "Current status" line.

---

# DEVELOPMENT RULES

1. Build instead of endlessly planning.
2. Keep the MVP focused.
3. Do not introduce major features without approval.
4. Follow the architecture rule: UI → services → models.
5. Use type hints everywhere.
6. Use `dataclass` and `Enum` for models.
7. Keep code understandable. Short functions, clear names.
8. Do not rewrite working code unnecessarily.
9. Before modifying the project, inspect the existing implementation.
10. After changes, run the app or tests and report what you verified.
11. Handle bad input: empty name, empty cart, corrupted JSON.
12. Preserve the night market theme.

---

# HOW TO WORK WITH THE USER

The user wants to build quickly and learn by implementation.

Give:

- Exact commands (the user is on Windows, use PowerShell syntax)
- Exact files
- Complete code when requested
- Short explanations
- Clear checklists

Do not:

- Restart planning
- Ask one tiny question at every step
- Repeat established information
- Over-explain simple code
- Make silent architectural decisions
- Add unnecessary technologies

Development approach:

> Build → encounter problem → understand it → fix it → continue.

---

# CURRENT STATUS

Phase 0: documentation written. Project not yet created.

**Immediate priority: start Phase 1 (Setup).**
