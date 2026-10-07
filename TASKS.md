# KANTO ORDERS: TASKS

> Progress tracker. Update when work is finished. Tick boxes, never delete them.

**Current status:** Phase 8 done (Testing complete).
**Next:** Phase 9 (School documentation).

---

## Phase 0: Documentation

- [x] AI_CONTEXT.md
- [x] PROJECT.md
- [x] TASKS.md
- [x] PROMPTS.md

## Phase 1: Setup

- [x] Create project folder and open it in the terminal
- [x] Create and activate virtual environment
- [x] `requirements.txt` (customtkinter, Pillow)
- [x] Install dependencies
- [x] Folder skeleton with `__init__.py` files
- [x] Place Bungee and Nunito `.ttf` files in `assets/fonts/`
- [x] `main.py` opens an empty customtkinter window
- [x] `.gitignore` (venv, `__pycache__`, `data/orders.json`)
- [x] Copy the four MD files into the project root

## Phase 2: Models and menu data

- [x] `models/enums.py` (OrderStatus, PaymentStatus)
- [x] `models/menu_item.py`
- [x] `models/order_item.py`
- [x] `models/payment.py`
- [x] `models/order.py`
- [x] `data/menu.py` with all 12 items
- [x] Quick check in the terminal: create an Order object and print it

## Phase 3: Services

- [x] `services/order_service.py` (create order, add items, calculate total, order numbers)
- [x] `services/payment_service.py`
- [x] `services/workflow_service.py` (forward-only, unpaid cannot be prepared)
- [x] `services/storage_service.py` (save, load, handle missing or corrupted JSON)
- [x] Run the whole process in the terminal without any UI

## Phase 4: UI shell and theme

- [x] `ui/theme.py` (palette, fonts, sizes)
- [x] `ui/fonts.py` (load Bungee and Nunito with fallback)
- [x] `ui/app.py` (window and layout frames)
- [x] `ui/header.py`
- [x] Layout approved by the user

## Phase 5: Order form and cart

- [x] `ui/order_form.py`: customer name
- [x] Menu by category with quantity controls
- [x] Cart with running total (from `OrderService`)
- [x] Pay now / Pay later
- [x] Place order creates and saves an order
- [x] Validation: empty name, empty cart

## Phase 6: Order list, actions, receipt

- [x] `ui/order_list.py` loads saved orders
- [x] One order card per order with status badge
- [x] Action button per status (Mark as Paid, Start Preparing, Mark Ready, Complete Order)
- [x] Status filter
- [x] `ui/receipt_view.py` in the required format
- [x] Orders persist after closing and reopening the app

## Phase 7: Bat and theme polish

- [x] Bat logo created and placed in header
- [x] Bat accent in empty state
- [x] Status badge colors consistent
- [x] Spacing, hover and focus states
- [x] Checked against the "avoid" list (no emoji spam, no clutter)

## Phase 8: Testing

- [x] `tests/test_services.py` (total, payment, workflow, storage)
- [x] Full flow: place, pay, prepare, ready, complete
- [x] Unpaid order cannot be prepared
- [x] No skipping or going back in statuses
- [x] Restart keeps orders and continues order numbers
- [x] Corrupted `orders.json` does not crash the app
- [x] Receipt matches the required format

## Phase 9: School documentation

- [ ] Final documentation (6 required sections)
- [ ] Process diagram
- [ ] Screenshots of each status
- [ ] Source code folder cleaned
- [ ] Demo walkthrough ready (sample orders)

---

## Decisions log

(Add one line per decision: date, decision.)

- 2026-10-07: Synced this tracker with the actual `frontend` implementation; Phase 8 tests are complete.
