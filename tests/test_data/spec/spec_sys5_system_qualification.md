# System elements

For each element, we need the static aspects, the dynamic aspects, and more.

#### TD_SYS_QUAL_order_cookies

The **TD** must be tested by ordering cookies.

Tests:

- [TD_SYS_REQ_cookie_ordering](#TD_sys_req_cookie_ordering)
- [TD_SYS_REQ_stock_and_order_tracking](#TD_sys_req_stock_and_order_tracking)
- [TD_SYS_REQ_cookie_baking](#TD_sys_req_cookie_baking)
- [TD_SYS_REQ_calculate_nominal_stock_level](#TD_sys_req_calculate_nominal_stock_level)

Cases:

- TD_SYS_TEST_order_a_cookie
- TD_SYS_TEST_order_too_many_cookies
- TD_SYS_TEST_too_many_orders

Results:

- TD_SYS_TEST_order_a_cookie: PASS
- TD_SYS_TEST_order_too_many_cookies: PASS
- TD_SYS_TEST_too_many_orders: PASS

#### TD_SYS_QUAL_operator_test

The **TD** operations terminal must be tested.

Tests:

- [TD_SYS_REQ_cookie_ordering](#TD_sys_req_cookie_ordering)
- [TD_SYS_REQ_stock_and_order_tracking](#TD_sys_req_stock_and_order_tracking)
- [TD_SYS_REQ_cookie_stock](#TD_sys_req_stock_and_order_tracking)
- [TD_SYS_REQ_bag_stock](#TD_sys_req_stock_and_order_tracking)
- [TD_SYS_REQ_bag_ordering](#TD_sys_req_bag_ordering)
- [TD_SYS_REQ_cookie_baking](#TD_sys_req_cookie_baking)

What cases:

- TD_SYS_TEST_order_a_cookie
- TD_SYS_TEST_check_stock_level
- TD_SYS_TEST_order_bags

Results:

- TD_SYS_TEST_order_a_cookie: PASS
- TD_SYS_TEST_order_a_cookie: FAIL
- TD_SYS_TEST_check_stock_level: FAIL
