# Software Components

## CDU_SW_COMP_cookie_order_database

The **CDU** keeps a database to hold information on inventory levels and unfulfilled orders.

Implements:

- CDU_SW_ARCH_database_backed

Fulfils:

- [CDU_SW_REQ_cookie_order_persistence](#cdu_sw_req_cookie_order_persistence)


## CDU_SW_COMP_cookie_ordering_website

The web page on which the **KIDS** can order cookies.

They must also be able to review the order status and ETA.

Implements:

- CDU_SW_ARCH_web_based_operation
- CDU_SW_ARCH_dynamic_status

Fulfils:

- [CDU_SW_REQ_ordering_page](#cdu_sw_req_ordering_page)
- [CDU_SW_REQ_cookie_delivery](#cdu_sw_req_cookie_delivery)


## CDU_SW_COMP_inventory_checker_logic

The constantly running or interval triggered logic which raises a warning which
can be rendered on the operator terminal to request more cookies are baked or
more bags are ordered.

Implements:

- CDU_SW_ARCH_event_based_operator_triggers

Fulfils:

- CDU_SW_REQ_cookie_operator_terminal

## CDU_SW_COMP_operator_terminal

The operator terminal. This will also be a web-page, running on the same server.
It needs to have buttons to acknowledge orders and mark the oven as in-use, so the "bake more cookies" alert goes away.
It needs to have a button to confirm more bags have been ordered.
It needs to have inputs for when cookies have finished baking and bags have arrived.

Implements:

- CDU_SW_ARCH_web_based_operation

Fulfils:

- CDU_SW_REQ_cookie_operator_terminal
