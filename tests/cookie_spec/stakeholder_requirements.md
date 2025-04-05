# Stakeholder requirements

Stakeholder requirements are written from
the perspective of the user and fulfil needs.
Requirements statements are of the form, "The <entity> shall ..."

The need they fulfil is linked because some needs can only be satisfied by a
combination of requirements.

#### CDU_STK_REQ_cookie_orders

**CDU** shall provide a cookie ordering mechanism.

Implements:

- [CDU_STK_NEED_get_a_cookie](#cdu_stk_need_get_a_cookie)

#### CDU_STK_REQ_cookie_availability

**CDU** shall fulfil cookie orders at short notice.

Short notice is a soft requirement of less than a minute in the normal case.
Delays of an hour or more are acceptable if
there was a rush on the cookies and they are now all gone.
A rush can be defined as an unusual number of orders
for cookies in the last hour.

Specification:

- **Safety related:** yes

Implements:

- [CDU_STK_NEED_get_a_cookie](#cdu_stk_need_get_a_cookie)

#### CDU_STK_REQ_bags_for_cookies

**CDU** shall deliver cookies in _paper_ bags.

There is an assumption that paper bags best preserve
the essential cookie-ness of cookies.

Implements:

- [CDU_STK_NEED_bag_for_cookies](#cdu_stk_need_bag_for_cookies)

#### REJECTED_CDU_STK_REQ_cookie_flavours

**CDU** shall provide a variety of flavours

Implements:

- [CDU_STK_NEED_variety](#cdu_stk_need_variety)

#### REJECTED_CDU_STK_REQ_milk

**CDU** shall provide milk
