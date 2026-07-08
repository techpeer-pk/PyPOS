# PyPOS-Lite: Stationary Shop POS
## 35K PKR One-Time | Fixed Scope | No Extras

**Client:** Stationary Shopkeeper  
**Budget:** 35,000 PKR (ONE-TIME, FINAL)  
**Timeline:** 10 days build + delivery  
**Support:** 30 days bug fixes only  

---

## What Client Gets (EXACTLY THIS)

### 1. Single .EXE File
- `PyPOS-Lite.exe` (standalone, ~100 MB)
- No Python needed
- Double-click to run
- Works offline completely
- Professional POS look

### 2. Five Professional Screens

**Screen 1: Dashboard (Home)**
- Today's sales total
- Invoice count
- Low stock alerts
- Quick action buttons

**Screen 2: New Sale (Main POS)**
```
Barcode Scan → Add to cart → Set Qty → Complete & Print Receipt
```
- Auto-add items
- Edit quantities
- Show running total
- Print thermal receipt
- Save invoice

**Screen 3: Inventory Management**
```
View all products → Search → Edit stock → Add new product
```
- List all products with SKU/price/stock
- Search by name
- Edit quantities
- Low stock warning flags
- Add new product form

**Screen 4: Daily Sales Report**
```
See all invoices for today → View totals
```
- List of all sales
- Invoice numbers with amounts
- Daily summary (total, average, count)
- Print report button

**Screen 5: Settings**
```
Configure printer/scanner → Backup database
```
- Shop info
- Printer port selection
- Scanner test
- Backup/Restore buttons

That's it. Looks professional, works simple.

### 3. Hardware Support
- ✅ USB Barcode Scanner (reads into app)
- ✅ Thermal Receipt Printer (ESC/POS)
- ✅ USB Ports (standard Windows)

### 4. Delivery Package
```
USB Stick contains:
├── PyPOS-Lite.exe
├── Quick Start (1 page PDF)
└── Data folder (for backups)
```

### 5. Training
- 2 hours on-site
- Shopkeeper learns: scan → sale → print
- That's all

### 6. Support (30 days)
- WhatsApp only
- Bug fixes only (not feature requests)
- After 30 days: paid support if needed

---

## What Client DOES NOT Get

### ❌ ABSOLUTELY NOT INCLUDED

- No dashboard
- No detailed reports
- No customer credit tracking (too complex for 35K)
- No analytics
- No accounting module
- No multi-user / passwords
- No cloud sync
- No PDF/Excel export
- No barcode stickers generation
- No professional installer
- No long-term support
- No updates/upgrades
- No mobile app
- No customer database search
- No invoicing history search

---

## Database (MINIMAL)

```sql
-- Products Table
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    sku TEXT UNIQUE,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    reorder_level INTEGER DEFAULT 5
);

-- Invoices Table (Track sales only)
CREATE TABLE invoices (
    id TEXT PRIMARY KEY,
    date TEXT,
    total REAL,
    items_count INTEGER,
    payment_method TEXT
);

-- Invoice Items (What was sold)
CREATE TABLE invoice_items (
    invoice_id TEXT,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL
);

-- Settings (Simple config)
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

That's it. 4 tables. Done.

---

## UI (4-5 Professional Screens)

### Screen 1: DASHBOARD (Home)

```
┌──────────────────────────────────────────────┐
│           PyPOS-LITE DASHBOARD               │
├──────────────────────────────────────────────┤
│                                              │
│  [NEW SALE]  [PRODUCTS]  [REPORTS]  [EXIT]  │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │  TODAY'S SALES SUMMARY               │   │
│  │  Total Sales:    5,450 PKR           │   │
│  │  Invoices:       12                  │   │
│  │  Last Sale:      14:32               │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │  LOW STOCK ALERTS                    │   │
│  │  ⚠ Pen Set - Only 2 left            │   │
│  │  ⚠ Eraser - Only 5 left             │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │  QUICK ACTIONS                       │   │
│  │  [View Inventory] [Print Report]     │   │
│  └──────────────────────────────────────┘   │
│                                              │
└──────────────────────────────────────────────┘
```

**Shows:**
- Today's total sales + invoice count
- Low stock warnings
- Quick action buttons
- Last sale time

---

### Screen 2: NEW SALE (Main POS Screen)

```
┌──────────────────────────────────────────────┐
│            NEW SALE - INVOICE                │
├──────────────────────────────────────────────┤
│                                              │
│  Barcode/SKU: [__________________]  Scan    │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ Item         Qty  Price Per  Total   │   │
│  ├──────────────────────────────────────┤   │
│  │ Notebook     2    200        400     │   │
│  │ Pen Set      3    150        450     │   │
│  │ Copy Paper   1    500        500     │   │
│  │ Eraser       5    50         250     │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  ┌──── TOTALS ────────────────────────┐    │
│  │ Subtotal:           1,600 PKR      │    │
│  │ Tax (if any):         0 PKR        │    │
│  │ TOTAL:             1,600 PKR       │    │
│  └────────────────────────────────────┘    │
│                                              │
│  Payment: [Cash ▼]                          │
│                                              │
│  [- Remove]  [Clear]  [COMPLETE & PRINT]   │
│                                              │
│  Invoice #: INV-20240115-005                │
│                                              │
└──────────────────────────────────────────────┘
```

**Actions:**
- Barcode scan → item auto-added
- Edit qty by clicking item
- Remove item button
- Payment method dropdown
- Complete → print → new sale

---

### Screen 3: INVENTORY MANAGEMENT

```
┌──────────────────────────────────────────────┐
│         INVENTORY MANAGEMENT                 │
├──────────────────────────────────────────────┤
│                                              │
│  [+ Add New]  [Import CSV]  [Back]          │
│                                              │
│  Search: [__________] Category: [All ▼]     │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ Product   SKU    Price Stock  Action │   │
│  ├──────────────────────────────────────┤   │
│  │ Notebook  NB-01  200   45   [Edit]   │   │
│  │ Pen Set   PS-01  150   2⚠  [Edit]   │   │
│  │ Eraser    ER-01  50    120  [Edit]   │   │
│  │ Copy      CP-01  500   200  [Edit]   │   │
│  │ Pencil    PC-01  30    80   [Edit]   │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  Total Products: 25                         │
│  Low Stock Items: 3                         │
│                                              │
└──────────────────────────────────────────────┘
```

**Actions:**
- Search products
- Add new product (opens form)
- Edit stock (click edit → popup)
- See low stock flags
- Import from CSV (if needed)

---

### Screen 4: REPORTS (Daily Sales)

```
┌──────────────────────────────────────────────┐
│           DAILY SALES REPORT                 │
├──────────────────────────────────────────────┤
│                                              │
│  Date: [Today ▼]  [View]  [Print]           │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ Invoice#  Time   Items  Amount Status │   │
│  ├──────────────────────────────────────┤   │
│  │ INV-001   10:30  2      400   PAID   │   │
│  │ INV-002   11:15  5      1,200 PAID   │   │
│  │ INV-003   12:45  3      850   PAID   │   │
│  │ INV-004   14:00  1      500   PAID   │   │
│  │ INV-005   14:32  4      1,100 PAID   │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ SUMMARY:                             │   │
│  │ Total Sales:        5,450 PKR        │   │
│  │ Invoices:           5                │   │
│  │ Avg Sale:           1,090 PKR        │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  [Back]  [Print Report]                     │
│                                              │
└──────────────────────────────────────────────┘
```

**Shows:**
- All invoices for selected day
- Invoice time, items count, amount
- Daily totals (simple)
- Print button

---

### Screen 5: SETTINGS (Simple Config)

```
┌──────────────────────────────────────────────┐
│           SETTINGS & CONFIG                  │
├──────────────────────────────────────────────┤
│                                              │
│  Shop Name: [Stationary Store]              │
│  Owner: [__________________]                │
│  Phone: [__________________]                │
│                                              │
│  ┌─ PRINTER ──────────────────────────────┐  │
│  │ Printer Port: [COM4 ▼]                 │  │
│  │ [Test Print]                           │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌─ SCANNER ──────────────────────────────┐  │
│  │ Auto-detect: [Enabled ▼]               │  │
│  │ [Test Scan]                            │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌─ BACKUP ───────────────────────────────┐  │
│  │ Last Backup: 2024-01-15 20:30          │  │
│  │ [Backup Now]  [Restore]                │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  [Save]  [Back]                             │
│                                              │
└──────────────────────────────────────────────┘
```

**Actions:**
- Edit shop name/info
- Configure printer port
- Test scanner
- Backup/restore database

---

## Code Structure (Lean & Professional)

```
PyPOS-Lite/
├── main.py                 (80 lines - app entry + menu)
├── database.py             (120 lines - SQLite connection)
├── models.py               (200 lines - Product, Invoice CRUD)
├── ui/
│   ├── dashboard.py        (150 lines - home screen + totals)
│   ├── sales.py            (250 lines - main POS screen)
│   ├── inventory.py        (200 lines - product management)
│   ├── reports.py          (150 lines - daily sales report)
│   └── settings.py         (100 lines - config screen)
├── services/
│   ├── printer.py          (120 lines - ESC/POS receipt)
│   ├── scanner.py          (80 lines - barcode listener)
│   └── backup.py           (60 lines - backup/restore)
├── config.py               (30 lines - constants)
├── data.db                 (auto-created)
└── README.txt              (15 lines - setup guide)

TOTAL: ~1,500 lines of code (Professional but simple)
```

**What makes it professional:**
- 5 screens (not 2)
- Dashboard shows daily totals
- Inventory searchable
- Reports visible
- Settings configurable
- But code is still clean & lean

---

## What Claude Code Builds

### Phase 1 (Day 1-2): Database + Models
```python
# models.py — CRUD operations only

class Product:
    @staticmethod
    def add(name, sku, price, stock):
        # INSERT into products
        
    @staticmethod
    def get_by_sku(sku):
        # SELECT from products
        
    @staticmethod
    def update_stock(sku, new_qty):
        # UPDATE stock

class Invoice:
    @staticmethod
    def create(items, payment_method):
        # INSERT into invoices + items
        # AUTO-GENERATE RECEIPT

    @staticmethod
    def get_today_total():
        # SUM(total) WHERE DATE = TODAY
```

**Test:** Add 5 products, create 1 invoice, verify stock updated.

### Phase 2 (Day 3-4): UI Forms
```python
# ui_sales.py — Sales screen
# ui_inventory.py — Inventory screen

Both forms:
- Accept input
- Call models
- Refresh display
```

**Test:** Scan barcode → add item → complete sale.

### Phase 3 (Day 5-6): Printer + Scanner
```python
# printer.py — ESC/POS commands
# scanner.py — USB barcode listener

Printer:
- Receive invoice → format → send to printer
- Print receipt

Scanner:
- Read USB data → trigger item_add function
```

**Test:** Scan real barcode → item appears.

### Phase 4 (Day 7-9): Build .EXE + Test
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# Output: dist/PyPOS-Lite.exe
```

**Test on clean Windows machine (no Python).**

### Phase 5 (Day 10): Delivery Prep
```
- Copy .exe to USB
- Create README.txt
- Backup database example
- Print Quick Start sheet
```

---

## Daily Workflow (Shopkeeper's Perspective)

**Morning:**
1. Turn on computer
2. Double-click `PyPOS-Lite.exe`
3. Dashboard opens (shows yesterday's sales)
4. Click "NEW SALE" button

**During Day:**
1. Customer comes with items
2. Click "NEW SALE" → goes to Sales screen
3. Scan each barcode (beep, auto-added to cart)
4. Items appear with price
5. Adjust quantity if needed
6. Click "COMPLETE & PRINT"
7. Thermal printer prints receipt
8. Saves invoice to database
9. Screen clears automatically, ready for next sale

**Mid-Day:**
1. Click "INVENTORY" to check stock
2. See low stock warnings
3. Update quantities if needed
4. Back to selling

**Evening:**
1. Click "REPORTS" to see daily summary
2. Verify total sales
3. Close app
4. Auto-backup happens

**Weekly:**
1. Click SETTINGS → "Backup Now" button
2. Copy data.db file to USB stick
3. Keep USB safe off-site

**If printer/scanner issue:**
1. Click SETTINGS
2. Click "Test Print" or "Test Scan"
3. Fix issue (or call support)

---

## Error Handling (Minimal but Effective)

```python
# If barcode not found:
MessageBox("Product not found. Add first.")

# If stock goes negative:
MessageBox("Not enough stock!")

# If printer fails:
MessageBox("Printer not responding. Check cable.")
(Saves receipt to file instead)

# If database error:
MessageBox("Data error. Restart app.")
```

No fancy error logs. Just simple messages.

---

## Receipt Format (Thermal Printer)

```
========================================
        STATIONARY SHOP
        Receipt
========================================
Date: 2024-01-15 14:32
Invoice: INV-20240115-001

Notebook           2x  400 = 800
Pen Set            3x  450 = 1,350
Copy Paper         1x  500 = 500

----------------------------------------
TOTAL:                      2,650 PKR
Payment: CASH
Status: PAID

Thank you! Come again.
========================================

```

Simple, readable, fits on receipt paper.

---

## Technical Specs

| Spec | Requirement |
|------|------------|
| **Language** | Python 3.10 |
| **Database** | SQLite (file-based) |
| **UI Framework** | PyQt6 (minimal) |
| **File Size** | ~80 MB .exe |
| **RAM Usage** | ~200 MB |
| **Disk Usage** | ~500 MB (app + data) |
| **Barcode** | USB scanner, standard keyboard input |
| **Printer** | USB thermal printer, ESC/POS |
| **OS** | Windows 7+ |
| **No Internet** | ✅ Works 100% offline |

---

## Installation (Client Does This)

**Step 1:** Double-click `PyPOS-Lite.exe`  
**Step 2:** Wait 10 seconds  
**Step 3:** App opens  
**Step 4:** Ready to use  

No installation wizard. No folders. No "Next Next Finish". Just double-click.

---

## Data Backup (Simple)

**What to backup:**
```
PyPOS-Lite folder:
├── PyPOS-Lite.exe
└── data.db  ← THIS FILE (copy weekly)
```

**How:**
```
1. Right-click data.db
2. Copy
3. Paste to USB stick
4. Keep USB safe
```

**That's it.** No complicated backup software.

---

## Support Scope (30 Days Only)

### I WILL FIX:
- ✅ App won't start
- ✅ Barcode scanner not working
- ✅ Printer not printing
- ✅ Database corrupted (restore from backup)
- ✅ Typos in product names (edit in inventory)

### I WILL NOT DO:
- ❌ Add new features
- ❌ Change design/layout
- ❌ Export reports
- ❌ Integrate with other software
- ❌ Add customer tracking
- ❌ Create invoicing history search

**After 30 days:** 
- Support ends
- Can ask for paid support (if needed, future)

---

## Contract Template (Use This)

```
PyPOS-Lite POS System - Service Agreement

CLIENT: [Stationary Shop Name]
AMOUNT: PKR 35,000 (One-time, Final)
DATE: [Date]

DELIVERABLES:
1. PyPOS-Lite.exe application
2. SQLite database (data.db)
3. Quick Start guide
4. 2-hour on-site training
5. 30-day email/WhatsApp support

SCOPE:
- Invoicing with barcode scanning
- Thermal receipt printing
- Basic stock management
- Daily sales tracking
- Offline-first operation

NOT INCLUDED:
- Cloud backup
- Customer database
- Advanced reporting
- Accounting module
- Long-term support (after 30 days)
- Feature additions
- Multi-location support

SUPPORT:
- 30 days: WhatsApp support (business hours)
- Bug fixes only (no feature requests)
- After 30 days: No support (optional paid support available)

PAYMENT:
- Full 35,000 PKR upon delivery
- No refunds (software delivered as agreed)
- No additional costs (hidden or otherwise)

SIGNATURE: _____________ DATE: _______
```

---

## Delivery Checklist

Before handing over:

- [ ] App starts without errors
- [ ] Can add 5 test products
- [ ] Barcode scanner works (if available)
- [ ] Can complete a sale
- [ ] Receipt prints (or saves to file)
- [ ] Stock updates after sale
- [ ] App closes cleanly
- [ ] Database file is safely backed up
- [ ] README is clear and simple
- [ ] Shopkeeper trained for 2 hours
- [ ] Shopkeeper can do simple sale independently

---

## What Happens After Delivery

**Day 1:** Shopkeeper uses app  
**Days 2-30:** You monitor WhatsApp, fix bugs if any  
**Day 31:** Support ends, you're done  

That's it. Clean. Clear. Final.

---

## Pricing Breakdown (Transparency)

```
Development:              18,000 PKR
- Database + CRUD         5,000
- Sales form              5,000
- Inventory form          3,000
- Printer integration     3,000
- Scanner integration     2,000

.EXE Packaging:            3,000 PKR
- PyInstaller config      1,000
- Build + test            1,000
- USB prep + docs         1,000

Training + Delivery:       8,000 PKR
- 2 hours on-site         5,000
- Travel                  2,000
- USB stick + docs        1,000

Contingency (bugs/fixes):  6,000 PKR
- 30-day support buffer   6,000

─────────────────────────────────
TOTAL:                    35,000 PKR
─────────────────────────────────
```

---

## Timeline (Realistic)

```
Day 1-2:  Database + models (quick, simple)
Day 3-4:  UI forms (no fancy design, just functional)
Day 5-6:  Printer + scanner (ESC/POS basic)
Day 7:    .EXE packaging + test
Day 8:    Final testing on clean machine
Day 9:    Prep delivery (USB, docs, etc.)
Day 10:   On-site training + delivery
Days 11-40: 30-day support (WhatsApp)
```

---

## Why This Works for 35K

✅ **Looks professional** — 5 screens, proper UI  
✅ **Scope is controlled** — 5 tables, ~1,500 lines (still lean)  
✅ **No extra features** — No accounting, no advanced reports, no cloud  
✅ **Fast to build** — 10 days realistic (well-defined screens)  
✅ **Easy to support** — No complex logic, straightforward code  
✅ **Clear boundaries** — Exact 5 screens, no "one more feature"  
✅ **One-time cost** — No recurring, no hidden charges  

---

## If Client Asks for More (After Day 1)

**Response:**
```
"That's Phase 2 (35K budget is Phase 1).
For more features, new quote needed:
- Detailed reports: +15K
- Customer database: +10K
- Each addition: +5-15K

Want to add? New contract + new price."
```

---

## Hand Off to Claude Code

**Instruction:**

> Build PyPOS-Lite exactly as per this plan:
> 
> Phase 1 (Days 1-2): Database schema (5 tables) + models.py (Product, Invoice CRUD)
> Phase 2 (Days 3-5): All 5 UI screens (dashboard, sales, inventory, reports, settings) using PyQt6
> Phase 3 (Days 6): Thermal printer (ESC/POS) + barcode scanner (USB) integration
> Phase 4 (Days 7-8): PyInstaller config, build .exe, test on clean Windows
> Phase 5 (Days 9-10): Final testing + delivery prep
> 
> 5 Screens (EXACT):
> 1. Dashboard (today's sales + alerts)
> 2. New Sale (main POS screen with barcode)
> 3. Inventory (product list + management)
> 4. Reports (daily sales list)
> 5. Settings (printer/scanner config + backup)
> 
> Constraints:
> - NO extra features beyond these 5 screens
> - NO fancy animations or design
> - NO scope creep
> - Total: ~1,500 lines of code
> - .EXE size: <100 MB
> 
> Start Phase 1, I'll review and approve each phase.

---

## Final Word

**35K is TIGHT. But 100% doable for this scope.**

If shopkeeper is happy with:
- ✅ Barcode → Sale → Receipt
- ✅ Stock tracking
- ✅ Works offline

Then this is EXACTLY what he needs. Nothing less, nothing more.

**Khatam. Finished. Done. 🎯**
