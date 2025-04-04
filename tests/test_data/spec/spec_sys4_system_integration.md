# System elements

For each element, we need the static aspects, the dynamic aspects, and more.

#### TD_SYS_INT_order_triggers_baking

The ordering system needs to integrate with the baking service and trigger
baking when an order demands more cookies than are in stock.

Integrates:

- [TD_SYS_ELEMENT_cookie_oven](#spec_sys3_system_architecture/TD_sys_element_cookie_oven)
- [TD_SYS_ELEMENT_stock_database](#spec_sys3_system_architecture/TD_sys_element_stock_database)

Case:

- TD_SYS_INT_TEST_trigger_baking
