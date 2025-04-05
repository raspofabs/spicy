# System elements

For each element, we need the static aspects, the dynamic aspects, and more.

#### CDU_SYS_INT_order_triggers_baking

The ordering system needs to integrate with the baking service and trigger
baking when an order demands more cookies than are in stock.

Integrates:

- [CDU_SYS_ELEMENT_cookie_oven](#spec_sys3_system_architecture/cdu_sys_element_cookie_oven)
- [CDU_SYS_ELEMENT_stock_database](#spec_sys3_system_architecture/cdu_sys_element_stock_database)
- [CDU_SYS_ELEMENT_operations_terminal](#spec_sys3_system_architecture/cdu_sys_element_operations_terminal)

Case:

- CDU_SYS_INT_TEST_trigger_baking

#### CDU_SYS_INT_order_triggers_baking

The ordering system needs to integrate with the baking service and trigger
baking when an order demands more cookies than are in stock.

Integrates:

- [CDU_SYS_ELEMENT_cookie_storage](#spec_sys3_system_architecture/cdu_sys_element_cookie_storage)
- [CDU_SYS_ELEMENT_cookie_website](#spec_sys3_system_architecture/cdu_sys_element_cookie_website)
- [CDU_SYS_ELEMENT_stock_database](#spec_sys3_system_architecture/cdu_sys_element_stock_database)

Case:

- CDU_SYS_INT_TEST_trigger_baking
