# System elements

For each element, we need the static aspects, the dynamic aspects, and more.

#### TD_SYS_ELEMENT_cookie_storage

The **TD** maintains a cookie locker where tins of cookies are placed.
The same locker also provides storage for the paper bags.

Software element: No

Implements:

- [TD_SYS_REQ_cookie_stock](#TD_sys_req_cookie_stock)
- [TD_SYS_REQ_bag_stock](#TD_sys_req_bag_stock)

#### TD_SYS_ELEMENT_cookie_website

The **TD** runs a simple server where the **KIDS** can order cookies.
The orders are stored in the stock_database and viewable by the **TD** to
determine stock levels.

Software element: Yes

Implements:

- [TD_SYS_REQ_cookie_ordering](#TD_sys_req_cookie_ordering)
- [TD_SYS_REQ_stock_and_order_tracking](#TD_sys_req_stock_and_order_tracking)

#### TD_SYS_ELEMENT_stock_database

The **TD** keeps a database of the current cookie stock levels, the current open orders, and how many bags are in stock.

Software element: Yes

Implements:

- [TD_SYS_REQ_stock_and_order_tracking](#TD_sys_req_stock_and_order_tracking)
- [TD_SYS_REQ_calculate_nominal_stock_level](#TD_sys_req_calculate_nominal_stock_level)

#### TD_SYS_ELEMENT_operations_terminal

The **TD** has an operations terminal.

The terminal has:

- low-stock alerts
- order listing - where orders can also be confirmed as fulfilled.
- baking order listing - including confirming baking in progress, or complete.
- bag stock listng, including ordering and receipt confirmation.

The front page shows the alerts for any low-stock items, so operators will know to act.
Open orders which are fulfilled can be marked as such here by an operator.
Any time an operator begins baking, or finishes baking, the fact can be added to the database.
Any time an operator orders bags, or receives them, the fact can be added to the database.

Software element: Yes

Implements:

- [TD_SYS_REQ_bag_ordering](#TD_sys_req_bag_ordering)
- [TD_SYS_REQ_cookie_baking](#TD_sys_req_cookie_baking)

#### TD_SYS_ELEMENT_cookie_oven

The **TD** has an operational oven in which cookies can be baked.

The oven has:

- information on how long it will take until cookies are finished baking.
- a capacity.

Any time an operator begins baking, the oven will be in-use.
Any time an operator finishes baking, the oven will be free-to-use.

Software element: No

Implements:

- [TD_SYS_REQ_cookie_baking](#TD_sys_req_cookie_baking)
