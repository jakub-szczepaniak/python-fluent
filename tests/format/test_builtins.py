from __future__ import absolute_import, unicode_literals

import unittest
from datetime import date, datetime
from decimal import Decimal

from fluent.context import MessageContext
from fluent.types import fluent_date, fluent_number

from ..syntax import dedent_ftl


class TestNumberBuiltin(unittest.TestCase):

    def setUp(self):
        self.ctx = MessageContext(['en-US'], use_isolating=False)
        self.ctx.add_messages(dedent_ftl("""
            implicit-call    = { 123456 }
            implicit-call2   = { $arg }
            defaults         = { NUMBER(123456) }
            percent-style    = { NUMBER(1.234, style: "percent") }
            currency-style   = { NUMBER(123456, style: "currency", currency: "USD") }
            from-arg         = { NUMBER($arg) }
            merge-params     = { NUMBER($arg, useGrouping: 0) }
        """))

    def test_implicit_call(self):
        val, errs = self.ctx.format('implicit-call', {})
        self.assertEqual(val, "123,456")
        self.assertEqual(len(errs), 0)

    def test_implicit_call2_int(self):
        val, errs = self.ctx.format('implicit-call2', {'arg': 123456})
        self.assertEqual(val, "123,456")
        self.assertEqual(len(errs), 0)

    def test_implicit_call2_float(self):
        val, errs = self.ctx.format('implicit-call2', {'arg': 123456.0})
        self.assertEqual(val, "123,456")
        self.assertEqual(len(errs), 0)

    def test_implicit_call2_decimal(self):
        val, errs = self.ctx.format('implicit-call2', {'arg': Decimal('123456.0')})
        self.assertEqual(val, "123,456")
        self.assertEqual(len(errs), 0)

    def test_defaults(self):
        val, errs = self.ctx.format('defaults', {})
        self.assertEqual(val, "123,456")
        self.assertEqual(len(errs), 0)

    def test_percent_style(self):
        val, errs = self.ctx.format('percent-style', {})
        self.assertEqual(val, "123%")
        self.assertEqual(len(errs), 0)

    def test_currency_style(self):
        val, errs = self.ctx.format('currency-style', {})
        self.assertEqual(val, "$123,456.00")
        self.assertEqual(len(errs), 0)

    def test_from_arg_int(self):
        val, errs = self.ctx.format('from-arg', {'arg': 123456})
        self.assertEqual(val, "123,456")
        self.assertEqual(len(errs), 0)

    def test_from_arg_float(self):
        val, errs = self.ctx.format('from-arg', {'arg': 123456.0})
        self.assertEqual(val, "123,456")
        self.assertEqual(len(errs), 0)

    def test_from_arg_decimal(self):
        val, errs = self.ctx.format('from-arg', {'arg': Decimal('123456.0')})
        self.assertEqual(val, "123,456")
        self.assertEqual(len(errs), 0)

    def test_partial_application(self):
        number = fluent_number(123456.78, currency="USD", style="currency")
        val, errs = self.ctx.format('from-arg', {'arg': number})
        self.assertEqual(val, "$123,456.78")
        self.assertEqual(len(errs), 0)

    def test_merge_params(self):
        number = fluent_number(123456.78, currency="USD", style="currency")
        val, errs = self.ctx.format('merge-params',
                                    {'arg': number})
        self.assertEqual(val, "$123456.78")
        self.assertEqual(len(errs), 0)


class TestDatetimeBuiltin(unittest.TestCase):

    def setUp(self):
        self.ctx = MessageContext(['en-US'], use_isolating=False)
        self.ctx.add_messages(dedent_ftl("""
            implicit-call    = { $date }
            explicit-call    = { DATETIME($date) }
            call-with-arg    = { DATETIME($date, dateStyle: "long") }
        """))

    def test_implicit_call_date(self):
        val, errs = self.ctx.format('implicit-call', {'date': date(2018, 2, 1)})
        self.assertEqual(val, "Feb 1, 2018")
        self.assertEqual(len(errs), 0)

    def test_implicit_call_datetime(self):
        val, errs = self.ctx.format('implicit-call', {'date': datetime(2018, 2, 1, 14, 15, 16)})
        self.assertEqual(val, "Feb 1, 2018")
        self.assertEqual(len(errs), 0)

    def test_explicit_call_date(self):
        val, errs = self.ctx.format('explicit-call', {'date': date(2018, 2, 1)})
        self.assertEqual(val, "Feb 1, 2018")
        self.assertEqual(len(errs), 0)

    def test_explicit_call_datetime(self):
        val, errs = self.ctx.format('explicit-call', {'date': datetime(2018, 2, 1, 14, 15, 16)})
        self.assertEqual(val, "Feb 1, 2018")
        self.assertEqual(len(errs), 0)

    def test_explicit_call_date_fluent_date(self):
        val, errs = self.ctx.format('explicit-call', {'date':
                                                      fluent_date(
                                                          date(2018, 2, 1),
                                                          dateStyle='short')
                                                      })
        self.assertEqual(val, "2/1/18")
        self.assertEqual(len(errs), 0)

    def test_arg(self):
        val, errs = self.ctx.format('call-with-arg', {'date': date(2018, 2, 1)})
        self.assertEqual(val, "February 1, 2018")
        self.assertEqual(len(errs), 0)

    def test_arg_overrides_fluent_date(self):
        val, errs = self.ctx.format('call-with-arg', {'date':
                                                      fluent_date(
                                                          date(2018, 2, 1),
                                                          dateStyle='short')
                                                      })
        self.assertEqual(val, "February 1, 2018")
        self.assertEqual(len(errs), 0)
