# Requirements

## Static aspects

#### TD_SW_REQ_cookie_order_persistence

The **TD** maintains a persistent data store for inventory levels and unfulfilled orders.

Required by:

- [TD_SYS_ELEMENT_cookie_storage](#TD_SYS_ARCH_cookie_storage)

#### TD_SW_REQ_ordering_page

The **TD** maintains a web-page where cookies can be ordered.

The ordering page takes as input, the **KIDS** ID and the number of cookies.
The output is a message as an ETA, or just a confirmation if cookies are immediately available.

Required by:

- [TD_SYS_ELEMENT_cookie_website](#TD_sys_arch_cookie_website)

#### TD_SW_REQ_cookie_operator_terminal

The **TD** notifies the operators for new orders of cookies through an operator terminal.

Required by:

- [TD_SYS_ELEMENT_operations_terminal](#TD_SYS_ELEMENT_operations_terminal)

## Dynamic aspects

#### TD_SW_REQ_cookie_delivery

The **TD** delivers cookies in reasonable time, or begins baking and then notifies the **KIDS** about the ETA (eating time approximation)

Required by:

- [TD_SYS_ELEMENT_operations_terminal](#TD_sys_element_operations_terminal)
