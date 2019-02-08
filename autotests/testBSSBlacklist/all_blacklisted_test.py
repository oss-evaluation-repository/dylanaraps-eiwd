#!/usr/bin/python3

import unittest
import sys

sys.path.append('../util')
import iwd
from iwd import IWD
from iwd import PSKAgent
from iwd import NetworkType

from hostapd import HostapdCLI
from hostapd import hostapd_map

from wiphy import wiphy_map
from hwsim import Hwsim

import time

class Test(unittest.TestCase):

    def test_connection_success(self):
        hwsim = Hwsim()

        bss_radio = [None, None]
        bss_hostapd = [None, None]

        for wname in wiphy_map:
            wiphy = wiphy_map[wname]
            intf = list(wiphy.values())[0]

            if intf.config and '1' in intf.config:
                bss_idx = 0
            elif intf.config and '2' in intf.config:
                bss_idx = 1
            else:
                continue

            for path in hwsim.radios:
                radio = hwsim.radios[path]
                if radio.name == wname:
                    break

            bss_radio[bss_idx] = radio
            bss_hostapd[bss_idx] = HostapdCLI(intf)

        rule0 = hwsim.rules.create()
        rule0.source = bss_radio[0].addresses[0]
        rule0.bidirectional = True
        rule0.signal = -2000

        rule1 = hwsim.rules.create()
        rule1.source = bss_radio[1].addresses[0]
        rule1.bidirectional = True
        rule1.signal = -8000

        wd = IWD(True)

        psk_agent = PSKAgent(["secret123", 'secret123'])
        wd.register_psk_agent(psk_agent)

        devices = wd.list_devices(1)
        device = devices[0]

        condition = 'not obj.scanning'
        wd.wait_for_object_condition(device, condition)

        device.scan()

        condition = 'not obj.scanning'
        wd.wait_for_object_condition(device, condition)

        ordered_network = device.get_ordered_network("TestBlacklist")

        self.assertEqual(ordered_network.type, NetworkType.psk)

        condition = 'not obj.connected'
        wd.wait_for_object_condition(ordered_network.network_object, condition)

        # Have both APs drop all packets, both should get blacklisted
        rule0.drop = True
        rule1.drop = True

        with self.assertRaises(iwd.FailedEx):
            ordered_network.network_object.connect()

        rule0.drop = False
        rule1.drop = False

        # This connect should work
        ordered_network.network_object.connect()

        condition = 'obj.connected'
        wd.wait_for_object_condition(ordered_network.network_object, condition)

        self.assertIn(device.address, bss_hostapd[0].list_sta())

        wd.unregister_psk_agent(psk_agent)

        del wd

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        IWD.clear_storage()

if __name__ == '__main__':
    unittest.main(exit=True)