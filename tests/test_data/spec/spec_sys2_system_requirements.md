# Requirements

#### CDU_SYS_REQ_1_1_cookie_ordering

The **CDU** shall respond to **KIDS** order requests.

Derived from:

- [CDU_STK_REQ_1_cookie_orders](#cdu_stk_req_1_cookie_orders)

#### CDU_SYS_REQ_1_2_stock_and_order_tracking

**CDU** shall maintain a list of orders and inventory
to provide details on stock levels.

Derived from:

- [CDU_STK_REQ_1_cookie_orders](#cdu_stk_req_1_cookie_orders)

#### CDU_SYS_REQ_2_1_cookie_stock

The **CDU** shall specify a location where it is possible to
maintain a stock of cookies.

Derived from:

- [CDU_STK_REQ_2_cookie_availability](#cdu_stk_req_2_cookie_availability)

#### CDU_SYS_REQ_2_2_calculate_nominal_stock_level

The **CDU** shall calculate the required level of stock
to ensure timely cookie delivery.

The correct stock level is related to the historic ordering data.

Derived from:

- [CDU_STK_REQ_1_cookie_orders](#cdu_stk_req_1_cookie_orders)
- [CDU_STK_REQ_2_cookie_availability](#cdu_stk_req_2_cookie_availability)

#### CDU_SYS_REQ_2_3_cookie_baking

The **CDU** shall bake more cookies in response to
low-stock warnings or surge-nomming.

The correct quantity to bake is related to the current stock
and the set of open orders.

Derived from:

- [CDU_STK_REQ_1_cookie_orders](#cdu_stk_req_1_cookie_orders)
- [CDU_STK_REQ_2_cookie_availability](#cdu_stk_req_2_cookie_availability)

#### CDU_SYS_REQ_3_1_bag_stock

The **CDU** shall specify a location where it is possible to
maintain a stock of paper bags.

Derived from:

- [CDU_STK_REQ_3_bags_for_cookies](#cdu_stk_req_3_bags_for_cookies)

#### CDU_SYS_REQ_3_2_bag_ordering

The **CDU** shall maintain a stock of paper bags sufficient
to deliver all current cookies in stock.

The correct number of bags is related to the historic ordering data.

Derived from:

- [CDU_STK_REQ_1_cookie_orders](#cdu_stk_req_1_cookie_orders)
- [CDU_STK_REQ_3_bags_for_cookies](#cdu_stk_req_3_bags_for_cookies)
