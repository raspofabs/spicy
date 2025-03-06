# Ordering a cookie

<!-- toc -->

The **KIDS** need to be able to order cookies from the cookie ordering page.

## Order a cookie for delivery on the web-page

    ID: FEAT_COOKIE_ORDERING_PAGE

A **KIDS** will use the web page to order a cookie.

Fulfils:

    CDU_STK_REQ_cookie_orders
    CDU_STK_REQ_cookie_availability

### Features, functions, and technical properties

THe web page will provide a way to enter the **KIDS** details.
They will expect a cookie quickly, or at least a notification that a new batch
is being cooked with an ETA.


### Description of usage

- **Purpose:**
    To capture an order for cookies from a specific **KIDS**, and get them their cookie.
- **Inputs:**
    Input from the **KIDS**, their ID, the number of cookies they want.
- **Outputs:**
    A confirmation notification, the cookies delivered quickly, or if slower, a
    message giving them an ETA.
- **Usage procedure:**
    Go to the web page,
    enter **KIDS** ID,
    select how many cookies,
    press the button,
    get the cookies (or a message).
- **Environmental constraints:**
    The **KIDS** must know their ID.
    The **KIDS** must be able to access the web-page.

### Impact analysis of feature

    TI class: TI2

If the button works, but no message or cookie arrives,
that would lead to a sad **KIDS**.

### Detectability analysis of feature

    TD class: TD1

The **KIDS** are very aware of how many cookies they have.
