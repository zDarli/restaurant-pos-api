# Order module (POS)

## Scope
This module is responsible for:
- Order lifecycle (create / draft / submit / cancel / close)
- Order items (add / update / remove)
- Monetary snapshot (subtotal/discount/tax/total)

Out of scope (separate modules):
- Payments / refunds
- Fiscalization
- Cash shifts

## Domain entities

### Order (Aggregate Root)
**Identity:** order_id
**Purpose:** Represents a single customer order and controls its consistency.

Fields:
- id
- type: DINE_IN | TAKEAWAY | DELIVERY
- status: DRAFT | SUBMITTED | CANCELED | CLOSED
- table_id (nullable)
- customer_name (nullable)
- customer_phone (nullable)

Monetary snapshot:
- currency: ISO 4217 (e.g., "RUB")
- subtotal_amount
- discount_amount
- tax_amount
- total_amount

Timestamps:
- created_at
- updated_at

### OrderItem
**Identity:** order_item_id
**Belongs to:** Order

Snapshot fields (must not change after submit):
- product_id (or menu_item_id)
- name_snapshot
- unit_price_amount_snapshot

Other fields:
- quantity
- line_total_amount
- notes (nullable)

## Invariants (business rules)
1. Items can be modified only when Order.status == DRAFT
   - add/update/remove is forbidden in SUBMITTED/CANCELED/CLOSED
2. Order cannot be submitted if it has 0 items
3. totals are recalculated from items on every items change
4. Status transitions must follow the state machine below

## Status machine
Allowed transitions:
- DRAFT -> SUBMITTED
- DRAFT -> CANCELED
- SUBMITTED -> CANCELED
- SUBMITTED -> CLOSED

Terminal states:
- CANCELED (no transitions)
- CLOSED (no transitions)

## Error mapping (domain-level)
- OrderNotFound -> 404
- InvalidOrderState / RuleViolation -> 409

## Persistence model (PostgreSQL)

### Table: orders
Columns:
- id (PK)
- type (varchar or enum)
- status (varchar or enum)

- table_id (nullable)
- customer_name (nullable)
- customer_phone (nullable)

- currency char(3) NOT NULL
- subtotal_amount numeric(12,2) NOT NULL DEFAULT 0
- discount_amount numeric(12,2) NOT NULL DEFAULT 0
- tax_amount numeric(12,2) NOT NULL DEFAULT 0
- total_amount numeric(12,2) NOT NULL DEFAULT 0

- created_at timestamptz NOT NULL
- updated_at timestamptz NOT NULL

Indexes:
- idx_orders_status (status)
- idx_orders_created_at (created_at)

### Table: order_items
Columns:
- id (PK)
- order_id (FK -> orders.id, ON DELETE CASCADE)

- product_id (FK optional, depends on Menu module)
- name_snapshot text NOT NULL
- unit_price_amount_snapshot numeric(12,2) NOT NULL

- quantity int NOT NULL
- line_total_amount numeric(12,2) NOT NULL
- notes text (nullable)

- created_at timestamptz NOT NULL

Indexes:
- idx_order_items_order_id (order_id)

Constraints:
- quantity > 0
- unit_price_amount_snapshot >= 0
- line_total_amount >= 0
