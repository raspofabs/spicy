# Requirements

## Static aspects

#### CDU_SW_REQ_cookie_order_persistence

The **CDU** maintains a persistent data store for inventory levels and unfulfilled orders.

Implements:

- [CDU_SYS_ARCH_cookie_storage](#CDU_SYS_ARCH_cookie_storage)

#### CDU_SW_REQ_ordering_page

The **CDU** maintains a web-page where cookies can be ordered.

The ordering page takes as input, the **KIDS** ID and the number of cookies.
The output is a message as an ETA, or just a confirmation if cookies are immediately available.

Implements:

- [CDU_SYS_ARCH_cookie_website](#cdu_sys_arch_cookie_website)

#### CDU_SW_REQ_cookie_operator_terminal

The **CDU** notifies the operators for new orders of cookies through an operator terminal.

Implements:

- [CDU_SYS_ARCH_operations_terminal](#cdu_sys_arch_operations_terminal)
