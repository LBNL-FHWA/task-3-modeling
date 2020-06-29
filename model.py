import pandas as pd
import os
from utils.microtype import MicrotypeCollection
from utils.network import Network, NetworkCollection, NetworkFlowParams, BusModeParams, \
    AutoModeParams, Costs
from utils.OD import Trip, TripCollection, OriginDestination, TripGeneration
from utils.population import PopulationGroup, Population
from typing import Dict, List


class TimePeriods:
    def __init__(self):
        self.__timePeriods = dict()

    def __setitem__(self, key: str, value: float):
        self.__timePeriods[key] = value

    def __getitem__(self, item) -> float:
        return self.__timePeriods[item]

    def importTimePeriods(self, df: pd.DataFrame):
        for row in df.itertuples():
            self[row.TimePeriodID] = row.DurationInHours


class DistanceBins:
    def __init__(self):
        self.__distanceBins = dict()

    def __setitem__(self, key: str, value: float):
        self.__distanceBins[key] = value

    def __getitem__(self, item) -> float:
        return self.__distanceBins[item]

    def importDistanceBins(self, df: pd.DataFrame):
        for row in df.itertuples():
            self[row.DistanceBinID] = row.MeanDistanceInMiles


class Model:
    def __init__(self, path: str):
        self.path = path
        self.microtypes = MicrotypeCollection(path)
        self.trips = TripCollection()
        self.population = Population()
        self.distanceBins = DistanceBins()
        self.timePeriods = TimePeriods()
        self.tripGeneration = TripGeneration()
        self.originDestination = OriginDestination()
        self.readFiles()

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    def readFiles(self):
        subNetworkData = pd.read_csv(os.path.join(self.path, "SubNetworks.csv"))
        modeToSubNetworkData = pd.read_csv(os.path.join(self.path, "ModeToSubNetwork.csv"))
        self.microtypes.importMicrotypes(subNetworkData, modeToSubNetworkData)

        self.trips.importTrips(pd.read_csv(os.path.join(self.path, "MicrotypeAssignment.csv")))

        populations = pd.read_csv(os.path.join(self.path, "Population.csv"))
        populationGroups = pd.read_csv(os.path.join(self.path, "PopulatioGroups.csv"))
        self.population.importPopulation(populations, populationGroups)

        self.timePeriods.importTimePeriods(pd.read_csv(os.path.join(self.path, "TimePeriods.csv")))

        self.distanceBins.importDistanceBins(pd.read_csv(os.path.join(self.path, "DistanceBins.csv")))

        originDestinations = pd.read_csv(os.path.join(self.path, "OriginDestination.csv"))
        distanceDistribution = pd.read_csv(os.path.join(self.path, "DistanceDistribution.csv"))
        self.originDestination.importOriginDestination(originDestinations, distanceDistribution)

        tripGeneration = pd.read_csv(os.path.join(self.path, "TripGeneration.csv"))
        self.tripGeneration.importTripGeneration(tripGeneration)

    def initializeTimePeriod(self, timePeriod: str):
        self.originDestination.initializeTimePeriod(timePeriod)
        self.tripGeneration.initializeTimePeriod(timePeriod)



if __name__ == "__main__":
    a = Model("input-data")
    a.initializeTimePeriod("AM-Peak")
    print("aah")
