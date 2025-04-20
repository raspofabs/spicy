#### TD_SYS_REQ_bag_ordering

The **TD** shall maintain a stock of paper bags sufficient
to deliver all current cookies in stock.

The correct number of bags is related to the historic ordering data.

Derived from:

- [TD_STK_REQ_cookie_orders](#td_stk_req_cookie_orders)
- [TD_STK_REQ_bags_for_cookies](#td_stk_req_bags_for_cookies)

Specification:

- **Type:** functional
- **Qualification relevant:** no

Verification Criteria:

- Bag orders are notifications to order, so they can be verified by reviewing
  the operator terminal output.

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

- [TD_SYS_REQ_bag_ordering](#td_sys_req_bag_ordering)
- [TD_SYS_REQ_cookie_baking](#td_sys_req_cookie_baking)
