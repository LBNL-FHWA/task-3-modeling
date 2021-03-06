import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import pandas as pd
import pytest

from utils.microtype import Microtype
from utils.network import Network, NetworkFlowParams, AutoMode, BusMode, TravelDemand, NetworkCollection

data = pd.DataFrame(
    {"SubnetworkID": 1, "MicrotypeID": "A", "ModesAllowed": "Auto-Bus", "Dedicated": False, "Length": 1000.0,
     "Type": "Road", "vMax": 16, "avgLinkLength": 50, "densityMax": 0.144},index=[1])

@pytest.fixture
def net():
    return Network(data, 1)


def test_mfd(net):
    auto = AutoMode([net], pd.DataFrame({"VehicleSize": 1}, index=["A"]), "A")
    net.addMode(auto)
    auto.assignVmtToNetworks()
    net.updateBaseSpeed()
    bs1 = net.getBaseSpeed()
    auto.travelDemand.rateOfPmtPerHour = 500.0
    auto.updateDemand()
    auto.assignVmtToNetworks()
    net.updateBaseSpeed()
    bs2 = net.getBaseSpeed()
    assert bs2 < bs1
    busParams = pd.DataFrame(
        {"VehicleSize": 1, "Headway": 300, "PassengerWait": 5, "PassengerWaitDedicated": 2., "MinStopTime": 15.,
         "PerStartCost": 2.5, "VehicleOperatingCostPerHour": 30., "StopSpacing": 300, "CoveragePortion": 0.5}, index=["A"])
    bus = BusMode([net], busParams, "A")
    net.addMode(bus)
    bus.assignVmtToNetworks()
    net.updateBlockedDistance()
    auto.assignVmtToNetworks()
    net.updateBaseSpeed()
    bs3 = net.getBaseSpeed()
    assert bs3 < bs2
    bus.travelDemand.tripStartRatePerHour = 30
    bus.updateDemand()
    net.updateBlockedDistance()
    bus.assignVmtToNetworks()
    net.updateBlockedDistance()
    auto.assignVmtToNetworks()
    net.updateBaseSpeed()
    bs4 = net.getBaseSpeed()
    assert bs4 < bs3

    # net2 = Network(pd.DataFrame({"Length": {0: 6000}, "Dedicated": {0: True}}), 0.,
    #                NetworkFlowParams(0.068, 15.42, 1.88, 0.145, 0.177, 50))
    # net3 = Network(pd.DataFrame({"Length": {0: 11000}, "Dedicated": {0: True}}), 0.,
    #                NetworkFlowParams(0.068, 15.42, 1.88, 0.145, 0.177, 50))
    #
    # autoData = pd.DataFrame({"VehicleSize": 1}, index=["A"])
    # busData = pd.DataFrame(
    #     {"VehicleSize": 3, "Headway": 600, "PassengerWait": 5, "PassengerWaitDedicated": 2., "MinStopTime": 15.,
    #      "PerStartCost": 2.5, "VehicleOperatingCostPerHour": 30., "StopSpacing": 300}, index=["A"])
    #
    # modeToModeData = {"auto": autoData, "bus": busData}
    # subNetworkToModes = {net2: ["auto", "bus"], net3: ["auto"]}
    # networkCollection = NetworkCollection(subNetworkToModes, modeToModeData, "A")
    # m = Microtype("A", networkCollection)
    #
    # busTrips = np.arange(1000, 20000, 1000.0)
    # autoTrips = np.arange(200, 4000, 200.0)
    # out = np.zeros((len(busTrips), len(autoTrips)))
    # autoAccumulation = []
    # busAccumulation = []
    # production = []
    # speeds = []
    # occupancy = []
    # for i in range(len(busTrips)):
    #     for j in range(len(autoTrips)):
    #         m.resetDemand()
    #         # networkCollection.updateNetworks()
    #         m.addModeDemandForPMT("bus", busTrips[i], 1000)
    #         m.addModeStarts("bus", busTrips[i])
    #         m.addModeDemandForPMT("auto", autoTrips[j], 2000)
    #         networkCollection.updateModes()
    #         print(networkCollection._networks[0].N_eq)
    #         out[i, j] = m.getModeSpeed("auto")
    #         speeds.append(m.getModeSpeed("bus"))
    #         production.append(networkCollection.modes['auto']._N_tot * m.getModeSpeed("auto") + networkCollection.modes[
    #             'bus']._N_tot * m.getModeSpeed("bus"))
    #         autoAccumulation.append(networkCollection.modes['auto']._N_tot)
    #         busAccumulation.append(networkCollection.modes['bus']._N_tot)
    #         occupancy.append(networkCollection.modes['bus'].getOccupancy())
    #
    # triang = tri.Triangulation(autoAccumulation, busAccumulation)
    # interpolator = tri.LinearTriInterpolator(triang, speeds)
    # Xi, Yi = np.meshgrid(np.linspace(0, max(autoAccumulation), 50), np.linspace(0, max(busAccumulation), 50))
    # zi = interpolator(Xi, Yi)
    # plt.contourf(Xi, Yi, zi)
    # print("AH")
