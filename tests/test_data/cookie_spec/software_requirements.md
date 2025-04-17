# Requirements

## Static aspects

#### CDU_SW_REQ_cookie_order_persistence

The **CDU** maintains a persistent data store for inventory levels and unfulfilled orders.

Decomposes:

- [CDU_SYS_ELEMENT_stock_database](#cdu_sys_element_stock_database)

Realises:

- [CDU_SYS_REQ_cookie_stock](#cdu_sys_req_cookie_stock)
- [CDU_SYS_REQ_bag_stock](#cdu_sys_req_bag_stock)

#### CDU_SW_REQ_ordering_page

The **CDU** maintains a web-page where cookies can be ordered.

The ordering page takes as input, the **KIDS** ID and the number of cookies.
The output is a message as an ETA, or just a confirmation if cookies are immediately available.

Decomposes:

- [CDU_SYS_ELEMENT_cookie_website](#cdu_sys_arch_cookie_website)

Realises:

- [CDU_SYS_REQ_cookie_ordering](#cdu_sys_arch_cookie_website)

#### CDU_SW_REQ_cookie_operator_terminal

The **CDU** notifies the operators for new orders of cookies through an operator terminal.

Decomposes:

- [CDU_SYS_ELEMENT_operations_terminal](#CDU_SYS_ELEMENT_operations_terminal)

Realises:

- [CDU_SYS_REQ_stock_and_order_tracking](#cdu_sys_req_stock_and_order_tracking)

## Dynamic aspects

#### CDU_SW_REQ_cookie_delivery

The **CDU** delivers cookies in reasonable time, or begins baking and then notifies the **KIDS** about the ETA (eating time approximation)

Decomposes:

- [CDU_SYS_ELEMENT_operations_terminal](#cdu_sys_element_operations_terminal)

Realises:

- [CDU_SYS_REQ_cookie_baking](#cdu_sys_req_cookie_baking)
