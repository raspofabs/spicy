# Ordering a cookie

<!-- toc -->

The **KIDS** need to be able to order cookies from the cookie ordering page.

## Bake cookies to order

    ID: FEAT_COOKIE_BAKING

A **CDU** operator will use the oven to bake some cookies.

Fulfils:

    CDU_STK_NEED_get_a_cookie

### Features, functions, and technical properties

The oven bakes cookies.

### Description of usage

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

### Impact analysis of feature

    TI class: TI2

If the oven fails, everyone is doomed to a life without cookies.

### Detectability analysis of feature

    TD class: TD1

The only people who cannot detect a cookie failure are those who hate cookies.
And those people are not allowed to be operators.


## Just put the cookies in the bag bro

    ID: FEAT_COOKIE_BAGGING

A **CDU** operator will bag the cookies

Fulfils:

    CDU_STK_NEED_bag_for_cookies

### Features, functions, and technical properties

The bag for cookie deliveries

### Description of usage

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

### Impact analysis of feature

    TI class: TI2

If the bag breaks, the cookie will fall.

### Detectability analysis of feature

    TD class: TD1

An empty bag is much lighter than a bag full of cookies.
