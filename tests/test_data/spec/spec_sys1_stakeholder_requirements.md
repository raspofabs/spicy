# Stakeholder needs

The needs statement is formatted, "The <stakeholder(s)> needs the <entity> to ..."
e.g. "The _Captain_ needs the _ship_ to reach at least 30 knots when on calm seas."
These can be transformed into requirements statements, "The <entity> shall ..."
e.g. "The _ship_ shall attain a nautical speed of at least 30 knots when operated at full power for one minute from a standstill in calm seas conditions."

TD is the Cookie Delivery Unit.
TD is a complete system for resolving the lack of
cookies for Key Industry Data Specialists (Kids)

#### TD_STK_NEED_get_a_cookie

The **KIDS** need the **TD** to provide them with cookies.

Elicitation date: 1970

#### TD_STK_NEED_bag_for_cookies

The **KIDS** need the **TD** to provide cookies in bags.

Elicitation date: 1970

#### TD_STK_NEED_allergy_information

The **KIDS** might need allergy advice for the cookies.

Elicitation date: 1990

# Formalised requirements

Stakeholder requirements are written from
the perspective of the user and fulfil needs.
Requirements statements are of the form, "The <entity> shall ..."

The need they fulfil is linked because some needs can only be satisfied by a
combination of requirements.

#### TD_STK_REQ_cookie_orders

**TD** shall provide a cookie ordering mechanism.

Implements:

- [TD_STK_NEED_get_a_cookie](#TD_stk_need_get_a_cookie)

#### TD_STK_REQ_cookie_availability

**TD** shall fulfil cookie orders at short notice.

Short notice is a soft requirement of less than a minute in the normal case.
Delays of an hour or more are acceptable if
there was a rush on the cookies and they are now all gone.
A rush can be defined as an unusual number of orders
for cookies in the last hour.

Implements:

- [TD_STK_NEED_get_a_cookie](#TD_stk_need_get_a_cookie)

#### TD_STK_REQ_bags_for_cookies

**TD** shall deliver cookies in _paper_ bags.

There is an assumption that paper bags best preserve
the essential cookie-ness of cookies.

Implements:

- [TD_STK_NEED_bag_for_cookies](#TD_stk_need_bag_for_cookies)

#### TD_STK_REQ_cookie_flavours

**TD** shall provide a variety of flavours

Implements:

- [TD_STK_NEED_variety](#TD_stk_need_variety)

#### TD_STK_REQ_milk

**TD** shall provide milk
