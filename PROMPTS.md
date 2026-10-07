# KANTO ORDERS: PHASE PROMPTS

> Copy-paste one prompt per phase into Claude Code, launched from the project root.
> Every prompt makes the agent read the docs first, ask only the questions that block the phase, build, then update `TASKS.md`.

## How to use

1. Open a terminal in the project root (the folder with `AI_CONTEXT.md`).
2. Launch Claude Code.
3. Paste the prompt for the current phase.
4. Answer its questions (reply "your call" to let it decide small things).
5. When it says the phase is done, check the "Done when" list below the prompt.
6. Only then paste the next prompt.

## Standard opening (already included in every prompt below)

> Read `AI_CONTEXT.md` first (rules, architecture, phases), then `PROJECT.md` (vision, school requirements, process, theme), then `TASKS.md` (what is done). Do not restart planning.

---

## Resume prompt (use any time you reopen a session)

```
Read AI_CONTEXT.md, then PROJECT.md, then TASKS.md. Tell me in 3 lines: the current phase, what is already done, and the next unchecked task. Inspect the actual files and tell me if they differ from the docs. Do not build anything yet.
```

---

## Phase 1: Setup

```
Read AI_CONTEXT.md first for rules and phasing, then PROJECT.md for the main goal and the school requirements, then TASKS.md. We are starting Phase 1 (Setup).

Before building, ask me only what you need, in one message, maximum 4 questions. Things you should check with me: Python version installed on my machine, the exact folder where the project lives, whether I will use Git, and whether I already downloaded the Bungee and Nunito font files.

Then do Phase 1: create the venv, requirements.txt, the folder skeleton with __init__.py files, .gitignore, and a main.py that opens an empty customtkinter window. Give me the exact PowerShell commands. Do not start Phase 2.

When finished: tick Phase 1 in TASKS.md, tell me how to run the app, and tell me what you verified.
```

**Done when:** `python main.py` opens an empty window, and the folder skeleton matches `AI_CONTEXT.md`.

---

## Phase 2: Models and menu data

```
Read AI_CONTEXT.md, PROJECT.md and TASKS.md. Phase 1 is finished. We are on Phase 2 (Models and menu data). Inspect the existing project first.

Ask me, in one message, only what blocks this phase: do I want to keep the menu prices in PROJECT.md section 5 or change any, and do I want item names with portion info like "Kwek-kwek (5 pcs)" or plain names.

Then build the models (enums, MenuItem, OrderItem, Payment, Order) as dataclasses and enums with type hints, plus data/menu.py with all 12 items. Models must contain no UI code and no file I/O. Show me a small terminal check that creates an Order and prints it. Do not start Phase 3.

When finished: tick Phase 2 in TASKS.md, explain in a few lines how the models relate to each other, and say what you verified.
```

**Done when:** you can create an `Order` with items in a Python shell and the subtotal and status fields make sense.

---

## Phase 3: Services

```
Read AI_CONTEXT.md, PROJECT.md and TASKS.md. Phase 2 is finished. We are on Phase 3 (Services). Inspect the existing models first.

Ask me, in one message, only what blocks this phase: should "Pay now" at order creation mean the order starts as CONFIRMED immediately (my assumption: yes), and should the order number continue from the highest saved number after restart (my assumption: yes). Confirm both assumptions rather than asking open questions.

Then build OrderService (create order, add items, calculate total, generate 3-digit order numbers), PaymentService, WorkflowService (forward-only, one step at a time, unpaid can never be prepared), and StorageService (save and load data/orders.json, handle a missing or corrupted file without crashing). Services must work with no UI. Prove it with a terminal script that runs the full process from Place Order to Completed and shows the blocked cases. Do not start Phase 4.

When finished: tick Phase 3 in TASKS.md, show me the terminal output, and list which rules you enforced in WorkflowService.
```

**Done when:** a terminal script runs the whole process, blocked transitions raise clear errors, and `orders.json` is written and reloaded.

---

## Phase 4: UI shell and theme

```
Read AI_CONTEXT.md, PROJECT.md and TASKS.md. Phase 3 is finished. We are on Phase 4 (UI shell and night market theme). Inspect the existing project, and do not touch the services.

Before building, ask me, in one message, maximum 4 questions, and offer concrete options for each: (1) the color palette (give me 2 or 3 hex palettes in the night market direction, lantern yellow and chili red accents), (2) whether I approve the screen layout in PROJECT.md section 7 or want it changed, (3) the final app name, (4) window size and whether it should be resizable.

Then build ui/theme.py, ui/fonts.py (Bungee for headings, Nunito for body, safe fallback if loading fails), ui/app.py with the layout frames, and ui/header.py with a text-only header for now (bat comes in Phase 7). No emoji. No business logic in the UI. Do not build the order form yet. Do not start Phase 5.

When finished: tick Phase 4 in TASKS.md and tell me how to run it.
```

**Done when:** the window shows the dark themed layout with empty panels, correct fonts, and no console errors.

---

## Phase 5: Order form and cart

```
Read AI_CONTEXT.md, PROJECT.md and TASKS.md. Phase 4 is finished. We are on Phase 5 (Order form and cart). Inspect the theme and app layout first and reuse them.

Ask me, in one message, only what blocks this phase: should the menu use category tabs (Rice and Soup, Street Food, Drinks) or one scrolling list, and should the quantity control be - / + buttons or a number box. Suggest your pick for each and I will confirm.

Then build ui/order_form.py: customer name, menu by category with quantity controls, a cart with a running total that comes from OrderService (the UI must not calculate it), Pay now / Pay later, and a Place Order button that creates and saves the order through the services. Validate empty name and empty cart with a clear, themed message. Do not start Phase 6.

When finished: tick Phase 5 in TASKS.md, and tell me exactly how to test it.
```

**Done when:** placing an order writes it to `data/orders.json` with the correct total and status, and bad input is rejected politely.

---

## Phase 6: Order list, status buttons, receipt

```
Read AI_CONTEXT.md, PROJECT.md and TASKS.md. Phase 5 is finished. We are on Phase 6 (Order list, actions, receipt). Inspect the existing UI and services first.

Ask me, in one message, only what blocks this phase: should I have a "Clear all orders" button for demos (default: yes, with a confirm dialog), and should completed orders stay in the list or move to a separate filter (default: stay, with a status filter). Confirm the defaults rather than asking open questions.

Then build ui/order_list.py with one order card per order and a status badge, one action button per status (Mark as Paid, Start Preparing, Mark Ready, Complete Order) that calls WorkflowService and PaymentService, a status filter, and ui/receipt_view.py that shows the selected order in exactly the required format from AI_CONTEXT.md (Customer, Order No., Food, Price, Payment, Order Status, with multiple food lines and a total). Orders must reload after closing and reopening the app. Do not start Phase 7.

When finished: tick Phase 6 in TASKS.md, and give me a 2-minute demo script to check the full process.
```

**Done when:** you can run one order from Pending Payment to Completed by clicking, the receipt matches the required format, and the data survives a restart.

---

## Phase 7: Bat and theme polish

```
Read AI_CONTEXT.md, PROJECT.md and TASKS.md. Phase 6 is finished. We are on Phase 7 (Bat and theme polish). Inspect the whole UI first. Do not change service logic.

Ask me, in one message, only what blocks this phase: should the bat logo be drawn by code with Pillow (my suggestion, no external files) or do I provide a PNG, what bat style do I want (simple flat silhouette, wings spread, or hanging), and where besides the header do I want bat accents (empty order list, completed badge, receipt). Keep bat accents to a few meaningful places.

Then create the bat logo, place it in the header, add the empty-state accent, make status badge colors consistent, and fix spacing, hover and focus states. Check the result against the "avoid" list in AI_CONTEXT.md (no emoji spam, no neon overload, no clutter, no generic card grid) and tell me honestly what still looks generic. Do not start Phase 8.

When finished: tick Phase 7 in TASKS.md.
```

**Done when:** the app looks intentional and themed, bats appear in a few meaningful places, and nothing looks like a default template.

---

## Phase 8: Testing

```
Read AI_CONTEXT.md, PROJECT.md and TASKS.md. Phase 7 is finished. We are on Phase 8 (Testing). Inspect the existing project first.

Ask me, in one message, only what blocks this phase: do I want unittest tests only, or tests plus a written manual test checklist I can screenshot for my documentation (default: both).

Then write tests/test_services.py with unittest covering total calculation, payment check, forward-only workflow, unpaid order blocked from preparing, storage save and load, and corrupted JSON. Run them and show the results. Then walk the app manually through the full process and edge cases (empty name, empty cart, restart, corrupted orders.json, long names, many orders) and report every bug you find. Fix bugs only after telling me what they are. Do not start Phase 9.

When finished: tick Phase 8 in TASKS.md and give me the test results as a short table.
```

**Done when:** all tests pass, the manual checklist passes, and you found and fixed anything that broke.

---

## Phase 9: School documentation

```
Read AI_CONTEXT.md, PROJECT.md and TASKS.md. Phase 8 is finished. We are on Phase 9 (School documentation). Use the real, finished program, not only the plan.

Ask me, in one message, only what blocks this phase: what file format my professor wants (Word, PDF or other), my name, section and subject for the cover page, and whether the documentation should be English only or mixed English and Filipino.

Then prepare the final documentation with these six sections exactly: project title, business problem, description of the process, how the program solves the problem, programming language used and why, short conclusion. Use the draft in PROJECT.md section 3 as the base but update it to match what was actually built. Add the process diagram, a list of screenshots I need to take (one per status), and a short demo script with sample orders. Also clean up the project folder for submission and tell me what to include.

When finished: tick Phase 9 in TASKS.md.
```

**Done when:** the documentation matches the program, the screenshots list is complete, and the project folder is clean.

---

## Quick prompts for problems

**Something broke:**

```
Read AI_CONTEXT.md. Something broke: [paste the error or describe it]. Inspect the relevant files, explain the cause in a few lines, fix it without rewriting working code, then tell me what you verified.
```

**I want to change something:**

```
Read AI_CONTEXT.md and PROJECT.md. I want to change: [describe]. Tell me which files it touches and whether it conflicts with the required process or architecture rule. Ask before making anything bigger than a small change.
```

**Check my architecture:**

```
Read AI_CONTEXT.md. Review the project against the architecture rule: UI calls services, services work on models, no logic in the UI, no file over about 200 lines. List violations only. Do not change code yet.
```

**Phase done check:**

```
Read TASKS.md and inspect the project. Tell me honestly whether the current phase is really finished, which boxes are not actually done, and what is the next phase. Do not start it.
```
