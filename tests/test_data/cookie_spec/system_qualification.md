# System Qualification

Once the system is integrated, we need to verify the system requirements are met.


#### CDU_SYS_QUAL_order_cookies

The **CDU** must be tested by ordering cookies.

Tests:

- [CDU_SYS_REQ_cookie_ordering](#cdu_sys_req_cookie_ordering)
- [CDU_SYS_REQ_stock_and_order_tracking](#cdu_sys_req_stock_and_order_tracking)
- [CDU_SYS_REQ_cookie_baking](#cdu_sys_req_cookie_baking)
- [CDU_SYS_REQ_calculate_nominal_stock_level](#cdu_sys_req_calculate_nominal_stock_level)

Cases:

- CDU_SYS_TEST_order_a_cookie
- CDU_SYS_TEST_order_too_many_cookies
- CDU_SYS_TEST_too_many_orders

Results:

- CDU_SYS_TEST_order_a_cookie: PASS
- CDU_SYS_TEST_order_too_many_cookies: PASS
- CDU_SYS_TEST_too_many_orders: PASS

#### CDU_SYS_QUAL_operator_test

The **CDU** operations terminal must be tested.

Qualification relevant: yes

Tests:

- [CDU_SYS_REQ_cookie_ordering](#cdu_sys_req_cookie_ordering)
- [CDU_SYS_REQ_stock_and_order_tracking](#cdu_sys_req_stock_and_order_tracking)
- [CDU_SYS_REQ_cookie_stock](#cdu_sys_req_stock_and_order_tracking)
- [CDU_SYS_REQ_bag_stock](#cdu_sys_req_stock_and_order_tracking)
- [CDU_SYS_REQ_bag_ordering](#cdu_sys_req_bag_ordering)
- [CDU_SYS_REQ_cookie_baking](#cdu_sys_req_cookie_baking)

Cases:

- CDU_SYS_TEST_order_a_cookie
- CDU_SYS_TEST_check_stock_level
- CDU_SYS_TEST_order_bags

Results:

- CDU_SYS_TEST_order_a_cookie: PASS
- CDU_SYS_TEST_check_stock_level: FAIL
- CDU_SYS_TEST_order_bags: FAIL
