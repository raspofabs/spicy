# Stakeholder requirements

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
