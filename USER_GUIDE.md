# KANTO ORDERS - USER GUIDE

## How to Use the System

### Creating an Order (Left Panel - "NEW ORDER")

1. **Enter Customer Name**
   - Type the customer's name in the "Customer:" field at the top

2. **Select Food Category**
   - Click one of the category buttons:
     - "Rice and Soup" (Lugaw, Goto, Mami, Pares, Chicken Meal)
     - "Street Food" (Kwek-kwek, Fishball, Isaw, Pagpag)
     - "Drinks" (Sago't Gulaman, Buko Juice, Iced Tea)

3. **Add Items to Cart**
   - Each menu item has a **[- 0 +]** control
   - Click **+** to add one item
   - Click **-** to remove one item
   - The number shows current quantity

4. **Check Your Cart**
   - Cart section shows all items added
   - Running total appears below cart: "Total: ₱XX"

5. **Choose Payment**
   - Select **"Pay now"** → Order starts as CONFIRMED
   - Select **"Pay later"** → Order starts as PENDING PAYMENT

6. **Place Order**
   - Click **"PLACE ORDER"** button at the bottom
   - Success popup appears
   - Form clears automatically
   - New order appears in the right panel

### Managing Orders (Right Panel - "ORDERS")

1. **View Orders**
   - All orders appear as cards
   - Filter by status using dropdown (top right)
   - Most recent orders at the top

2. **Order Card Shows:**
   - Order number and customer name
   - Items ordered
   - Total amount
   - Payment badge (PAID / UNPAID)
   - Status badge (color-coded)
   - Action button (if available)

3. **Status Flow & Action Buttons:**
   - **PENDING PAYMENT** → Click "Mark as Paid" → CONFIRMED
   - **CONFIRMED** → Click "Start Preparing" → PREPARING
   - **PREPARING** → Click "Mark Ready" → READY
   - **READY** → Click "Complete Order" → COMPLETED
   - **COMPLETED** → No button (order finished)

4. **View Receipt**
   - Click anywhere on an order card
   - Receipt appears in bottom panel

### Receipt (Bottom Panel)

Shows selected order details in required format:
- Customer name
- Order number
- Food items
- Price
- Payment status
- Order status

## Important Rules

- **Cannot prepare unpaid orders** - Must mark as paid first
- **Cannot skip statuses** - Must follow the flow step by step
- **Cannot go backwards** - Forward only (no undoing)
- **Orders persist** - Saved automatically, reload on restart

## Troubleshooting

**"No orders yet" message?**
- No orders have been created yet, or filter is hiding them

**Can't click "PLACE ORDER"?**
- Check: Did you enter a customer name?
- Check: Did you add items to cart (quantity > 0)?

**Action button not appearing?**
- Completed orders have no action button
- Check the order's current status

**Error popup appears?**
- Read the message - it tells you what's missing
- Common: Empty name or empty cart
