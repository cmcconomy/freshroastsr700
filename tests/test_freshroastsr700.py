# -*- coding: utf-8 -*-
# Roastero, released under GPLv3

import unittest
import freshroastsr700
from freshroastsr700 import exceptions


class TestFreshroastsr700(unittest.TestCase):
    """A test class for the freshroastsr700 module."""
    def setUp(self):
        """Sets up the freshroastsr700 object for testing."""
        self.roaster = freshroastsr700.freshroastsr700()

    def test_init_var_header(self):
        """Verifies _header is created on initialization properly."""
        self.assertEqual(self.roaster._header, b'\xAA\xAA')

    def test_init_var_temp_unit(self):
        """Verifies _temp_unit is created on initialization properly."""
        self.assertEqual(self.roaster._temp_unit, b'\x61\x74')

    def test_init_var_flags(self):
        """Verifies _flags is created on initialization properly."""
        self.assertEqual(self.roaster._flags, b'\x63')

    def test_init_var_control(self):
        """Verifies _control is created on initialization properly."""
        self.assertEqual(self.roaster._control, b'\x02\x01')

    def test_init_var_footer(self):
        """Verifies _footer is created on initialization properly."""
        self.assertEqual(self.roaster._footer, b'\xAA\xFA')

    def test_init_var_fan_speed(self):
        """Verifies _fan_speed is created on initialization properly."""
        self.assertEqual(self.roaster._fan_speed, 1)

    def test_init_var_heat_setting(self):
        """Verifies _heat_setting is created on initialization properly."""
        self.assertEqual(self.roaster._heat_setting, 0)

    def test_init_var_time_remaining(self):
        """Verifies _time_remaining is created on initialization properly."""
        self.assertEqual(self.roaster._time_remaining, 0.0)

    def test_init_var_current_temp(self):
        """Verifies current_temp is created on initialization properly."""
        self.assertEqual(self.roaster.current_temp, 150)

    def test_generate_packet(self):
        """Verifies packet generated is equal to the expected hex value."""
        packet = self.roaster.generate_packet()
        self.assertEqual(
            packet, b'\xaa\xaaatc\x02\x01\x01\x00\x00\x00\x00\xaa\xfa')

    def test_open_packet_not_150(self):
        """Verifies the supplied hex will set the current temperature to 352."""
        self.roaster.open_packet(
            b'\xaa\xaaatc\x02\x01\x01\x00\x00\x01\x60\xaa\xfa')
        self.assertEqual(self.roaster._current_temp, 352)

    def test_open_packet_before_over_150(self):
        """Verifies the supplied hex for 65280 will set the current temperature
        to 150."""
        self.roaster.open_packet(
            b'\xaa\xaaatc\x02\x01\x01\x00\x00\xff\x00\xaa\xfa')
        self.assertEqual(self.roaster._current_temp, 150)

    def test_idle(self):
        """Verifies that idle appropriatly sets the current state of the
        roaster."""
        self.roaster.idle()
        self.assertEqual(self.roaster.current_state, b'\x02\x01')

    def test_roast(self):
        """Verifies that roast appropriatly sets the current state of the
        roaster."""
        self.roaster.roast()
        self.assertEqual(self.roaster.current_state, b'\x04\x02')

    def test_cool(self):
        """Verifies that cool appropriatly sets the current state of the
        roaster."""
        self.roaster.cool()
        self.assertEqual(self.roaster.current_state, b'\x04\x04')

    def test_sleep(self):
        """Verifies that sleep appropriatly sets the current state of the
        roaster."""
        self.roaster.sleep()
        self.assertEqual(self.roaster.current_state, b'\x08\x01')

    def test_getting_var_fan_speed(self):
        """Verifies that the getter for fan speed is working."""
        self.assertEqual(self.roaster.fan_speed, 1)

    def test_setting_var_fan_speed_high(self):
        """Verifies that setting the fan speed too high raises an exception."""
        with self.assertRaises(exceptions.RoasterValueError):
            self.roaster.fan_speed = 10

    def test_setting_var_fan_speed_low(self):
        """Verifies that setting the fan speed too low raises an exception."""
        with self.assertRaises(exceptions.RoasterValueError):
            self.roaster.fan_speed = 0

    def test_getting_time_remaining(self):
        """Verifies that the getter for time remaining is working."""
        self.assertEqual(self.roaster.time_remaining, 0.0)

    def test_setting_var_time_remaining_high(self):
        """Verifies that setting the time_remaining value too high raises an 
        exception."""
        with self.assertRaises(exceptions.RoasterValueError):
            self.roaster.time_remaining = 11