# Requirements

#### TD_SYS_REQ_cookie_ordering

The **TD** shall respond to **KIDS** order requests.

Derived from:

- [TD_STK_REQ_cookie_orders](#TD_stk_req_cookie_orders)

Verification Criteria:

- Check the order list on the operator terminal to verify ordering is successful.

#### TD_SYS_REQ_stock_and_order_tracking

**TD** shall maintain a list of orders and inventory
to provide details on stock levels.

Derived from:

- [TD_STK_REQ_cookie_orders](#TD_stk_req_cookie_orders)

Verification Criteria:

- Check the order list is present on the operator terminal.

#### TD_SYS_REQ_cookie_stock

The **TD** shall specify a location where it is possible to
maintain a stock of cookies.

Derived from:

- [TD_STK_REQ_cookie_availability](#TD_stk_req_cookie_availability)

Verification Criteria:

- Check there is a cookie cupboard.

#### TD_SYS_REQ_calculate_nominal_stock_level

The **TD** shall calculate the required level of stock
to ensure timely cookie delivery.

The correct stock level is related to the historic ordering data.

Derived from:

- [TD_STK_REQ_cookie_orders](#TD_stk_req_cookie_orders)
- [TD_STK_REQ_cookie_availability](#TD_stk_req_cookie_availability)

Verification Criteria:

- Check the stock level is visible on the operator terminal.

#### TD_SYS_REQ_cookie_baking

The **TD** shall bake more cookies in response to
low-stock warnings or surge-nomming.

The correct quantity to bake is related to the current stock
and the set of open orders.

Derived from:

- [TD_STK_REQ_cookie_orders](#TD_stk_req_cookie_orders)
- [TD_STK_REQ_cookie_availability](#TD_stk_req_cookie_availability)

Verification criteria:

- Baking orders can be checked on the operator terminal output.
- Quantity needs to be checked too.

#### TD_SYS_REQ_bag_stock

The **TD** shall specify a location where it is possible to
maintain a stock of paper bags.

Derived from:

- [TD_STK_REQ_bags_for_cookies](#TD_stk_req_bags_for_cookies)

#### TD_SYS_REQ_bag_ordering

The **TD** shall maintain a stock of paper bags sufficient
to deliver all current cookies in stock.

The correct number of bags is related to the historic ordering data.

Derived from:

- [TD_STK_REQ_cookie_orders](#TD_stk_req_cookie_orders)
- [TD_STK_REQ_bags_for_cookies](#TD_stk_req_bags_for_cookies)

Verification Criteria:

- Bag orders are notifications to order, so they can be verified by reviewing
  the operator terminal output.
