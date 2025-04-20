# Use Cases for Ordering cookies - qualification plan classification document

<!-- toc -->

The **KIDS** need to be able to order cookies from the cookie ordering page.

# Order a cookie for delivery on the web-page

    ID: FEAT_COOKIE_ORDERING_PAGE

A **KIDS** will use the web page to order a cookie.

NOTE: Low TCL

Fulfils:

    CDU_STK_NEED_get_a_cookie

## Features, functions, and technical properties

THe web page will provide a way to enter the **KIDS** details.
They will expect a cookie quickly, or at least a notification that a new batch
is being cooked with an ETA.


## Description of usage

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

## Impact analysis of feature

    TI class: TI2

If the button works, but no message or cookie arrives,
that would lead to a sad **KIDS**.

## Detectability analysis of feature

    TD class: TD1

The **KIDS** are very aware of how many cookies they have.


# Use an oven

NOTE: High TCL

    ID: FEAT_HOT_OVEN

A **CDU** operator will use the oven to bake some cookies.

Fulfils:

    CDU_STK_NEED_get_a_cookie

## Features, functions, and technical properties

The oven bakes cookies.

## Description of usage

- **Purpose:** To turn a cookie debt into cookies.
- **Inputs:** Ingredients, electricity, and love.
- **Outputs:** A life-affirming, warm and delicious batch of cookies.
- **Usage procedure:** Put uncooked cookies in oven.
- **Environmental constraints:** The **Operator** must be tall enough to open the oven door.

## Impact analysis of feature

    TI class: TI2

If the oven fails, everyone is doomed to a life without cookies.

## Detectability analysis of feature

    TD class: TD2

The failure might be slight undercooking, which goes unnoticed until the first bite!


# Bake cookies to order

    ID: FEAT_COOKIE_BAKING

A **CDU** operator will use the oven to bake some cookies.

Fulfils:

    CDU_STK_NEED_get_a_cookie

## Features, functions, and technical properties

The oven bakes cookies.

## Description of usage

- **Purpose:**
    To turn a cookie debt into cookies.
- **Inputs:**
    Ingredients, electricity, and love.
- **Outputs:**
    A life-affirming, warm and delicious batch of cookies.
- **Usage procedure:**
    Put uncooked cookies in oven.
    Wait.
    Take out the cooked cookies and shove them into the fully qualified **CDU** cookie dumpster.
- **Environmental constraints:**
    The **Operator** must be tall enough to open the oven door.

## Impact analysis of feature

    TI class: TI2

If the oven fails, everyone is doomed to a life without cookies.

## Detectability analysis of feature

    TD class: TD1

The only people who cannot detect a cookie failure are those who hate cookies.
And those people are not allowed to be operators.


# Just put the cookies in the bag bro

    ID: FEAT_COOKIE_BAGGING

A **CDU** operator will bag the cookies

Fulfils:

    CDU_STK_NEED_bag_for_cookies

## Features, functions, and technical properties

The bag for cookie deliveries

## Description of usage

- **Purpose:**
    To make it less greasy.
- **Inputs:**
    Paper bag. Ennui. Cookies.
- **Outputs:**
    Social stigma and a paper bag with cookies in it.
- **Usage procedure:**
    Put cookies in the bag bro.
- **Environmental constraints:**
    The **Operator** must operate. No need for your life story.

## Impact analysis of feature

    TI class: TI2

If the bag breaks, the cookie will fall.

## Detectability analysis of feature

    TD class: TD1

An empty bag is much lighter than a bag full of cookies.
