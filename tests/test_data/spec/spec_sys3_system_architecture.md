# System elements

For each element, we need the static aspects, the dynamic aspects, and more.

#### CDU_SYS_ELEMENT_cookie_storage

The **CDU** maintains a cookie locker where tins of cookies are placed.
The same locker also provides storage for the paper bags.

Implements:

- [CDU_SYS_REQ_cookie_stock](#cdu_sys_req_cookie_stock)
- [CDU_SYS_REQ_bag_stock](#cdu_sys_req_bag_stock)

#### CDU_SYS_ELEMENT_cookie_website

The **CDU** runs a simple server where the **KIDS** can order cookies.
The orders are stored in the stock_database and viewable by the **CDU** to
determine stock levels.

Implements:

- [CDU_SYS_REQ_cookie_ordering](#cdu_sys_req_cookie_ordering)
- [CDU_SYS_REQ_stock_and_order_tracking](#cdu_sys_req_stock_and_order_tracking)

#### CDU_SYS_ELEMENT_stock_database

The **CDU** keeps a database of the current cookie stock levels, the current open orders, and how many bags are in stock.

Implements:

- [CDU_SYS_REQ_stock_and_order_tracking](#cdu_sys_req_stock_and_order_tracking)
- [CDU_SYS_REQ_calculate_nominal_stock_level](#cdu_sys_req_calculate_nominal_stock_level)

#### CDU_SYS_ELEMENT_operations_terminal

The **CDU** has an operations terminal.

The terminal has:

- low-stock alerts
- order listing - where orders can also be confirmed as fulfilled.
- baking order listing - including confirming baking in progress, or complete.
- bag stock listng, including ordering and receipt confirmation.

The front page shows the alerts for any low-stock items, so operators will know to act.
Open orders which are fulfilled can be marked as such here by an operator.
Any time an operator begins baking, or finishes baking, the fact can be added to the database.
Any time an operator orders bags, or receives them, the fact can be added to the database.

- [CDU_SYS_REQ_bag_ordering](#cdu_sys_req_bag_ordering)
- [CDU_SYS_REQ_cookie_baking](#cdu_sys_req_cookie_baking)

#### CDU_SYS_ELEMENT_cookie_oven

The **CDU** has an operational oven in which cookies can be baked.

The oven has:

- information on how long it will take until cookies are finished baking.
- a capacity.

Any time an operator begins baking, the oven will be in-use.
Any time an operator finishes baking, the oven will be free-to-use.

- [CDU_SYS_REQ_cookie_baking](#cdu_sys_req_cookie_baking)
