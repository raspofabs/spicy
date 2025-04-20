# Software Units

# CDU_SW_UNIT_cookie_ordering_server

The **CDU** runs a server process to handle the database transactions and accept web page requests.

Implements:

- [CDU_SW_COMP_cookie_database](#cdu_sw_comp_cookie_database)


# CDU_SW_UNIT_cookie_stock_and_orders_database

The **CDU** maintains a database to store stock and order information.

Implements:

- CDU_SW_COMP_cookie_order_database


# CDU_SW_UNIT_cookie_ordering_web_page_frontend

The **CDU** server presents itself via a web page which can order cookies.

Implements:

- CDU_SW_COMP_cookie_ordering_website


# CDU_SW_UNIT_cookie_operator_terminal_web_page_frontend

The **CDU** server presents itself via a web page which can operate the system.

Implements:

- CDU_SW_COMP_operator_terminal
- CDU_SW_COMP_inventory_checker_logic
