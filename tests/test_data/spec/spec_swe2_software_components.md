# Components

#### CDU_SW_COMP_cookie_order_database

The **CDU** keeps a database to hold information on inventory levels and unfulfilled orders.

Implements:

- [CDU_SW_REQ_cookie_order_persistence](#cdu_sw_req_cookie_order_persistence)

#### CDU_SW_COMP_cookie_ordering_website

The web page on which the **KIDS** can order cookies.

Implements:

- [CDU_SW_REQ_ordering_page](#)

#### CDU_SW_COMP_inventory_checker_logic

The constantly running or interval triggered logic which raises a warning which
can be rendered on the operator terminal to request more cookies are baked or
more bags are ordered.

Implements:

- [CDU_SW_REQ_cookie_baking_trigger](#cdu_sw_req_cookie_baking_trigger)
- [CDU_SW_REQ_bag_ordering_trigger](#cdu_sw_req_bag_ordering_trigger)

#### CDU_SW_COMP_operator_terminal

The operator terminal. This will also be a web-page, running on the same server.
It needs to have buttons to acknowledge orders and mark the oven as in-use, so the "bake more cookies" alert goes away.
It needs to have a button to confirm more bags have been ordered.
It needs to have inputs for when cookies have finished baking and bags have arrived.

Implements:

- CDU_SW_REQ_cookie_operator_terminal
