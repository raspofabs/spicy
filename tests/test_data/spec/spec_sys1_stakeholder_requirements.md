# Stakeholder needs

The needs statement is formatted, "The <stakeholder(s)> needs the <entity> to ..."
e.g. "The _Captain_ needs the _ship_ to reach at least 30 knots when on calm seas."
These can be transformed into requirements statements, "The <entity> shall ..."
e.g. "The _ship_ shall attain a nautical speed of at least 30 knots when operated at full power for one minute from a standstill in calm seas conditions."

CDU is the Cookie Delivery Unit.
CDU is a complete system for resolving the lack of
cookies for Key Industry Data Specialists (Kids)

#### CDU_STK_NEED_1_get_a_cookie

The **KIDS** need the **CDU** to provide them with cookies.

#### CDU_STK_NEED_2_bag_for_cookies

The **KIDS** need the **CDU** to provide cookies in bags.

# Formalised requirements

Stakeholder requirements are written from
the perspective of the user and fulfil needs.
Requirements statements are of the form, "The <entity> shall ..."

The need they fulfil is linked because some needs can only be satisfied by a
combination of requirements.

#### CDU_STK_REQ_1_cookie_orders

**CDU** shall provide a cookie ordering mechanism.

Implements:

- [CDU_STK_NEED_1_get_a_cookie](#cdu_stk_need_1_get_a_cookie)

#### CDU_STK_REQ_2_cookie_availability

**CDU** shall fulfil cookie orders at short notice.

Short notice is a soft requirement of less than a minute in the normal case.
Delays of an hour or more are acceptable if
there was a rush on the cookies and they are now all gone.
A rush can be defined as an unusual number of orders
for cookies in the last hour.

Implements:

- [CDU_STK_NEED_1_get_a_cookie](#cdu_stk_need_1_get_a_cookie)

#### CDU_STK_REQ_3_bags_for_cookies

**CDU** shall deliver cookies in _paper_ bags.

There is an assumption that paper bags best preserve
the essential cookie-ness of cookies.

Implements:

- [CDU_STK_NEED_2_bag_for_cookies](#cdu_stk_need_2_bag_for_cookies)
