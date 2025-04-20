# Software Architecture

The architecture is where the more difficult decisions are made.

# CDU_SW_ARCH_web_based_operation

The **CDU** uses a web server to provide pages for both customers and operators.

Fulfils:

- CDU_SW_REQ_ordering_page
- CDU_SW_REQ_cookie_operator_terminal

# CDU_SW_ARCH_event_based_operator_triggers

The **CDU** has a triggering event for when there are not enough cookies or
bags to fulfil a current or expected future order.

Fulfils:

- CDU_SW_REQ_cookie_operator_terminal

# CDU_SW_ARCH_database_backed

The **CDU** uses a simple database to store data. No stored procedures. Just
use code in the processes to handle the logic. This way the database itself can
easily be moved, migrated, redesigned.

Fulfils:

- CDU_SW_REQ_cookie_order_persistence
