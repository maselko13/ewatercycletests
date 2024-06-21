"""Module containing the scenarios that are generated
 for the sake of the ScenarioTests test bank.

This module contains all the methods that are used
to generate scenarios by altering generic forcing data.
"""

from pathlib import Path
import xarray as xr
import ewatercycle
from ewatercycle.base.forcing import GenericLumpedForcing, GenericDistributedForcing
import random
import math

shape = Path(ewatercycle.__file__).parent / "testing/data/Rhine/Rhine.shp"
cmip_dataset = {
        "dataset": "EC-Earth3",
        "project": "CMIP6",
        "grid": "gr",
        "exp": "historical",
        "ensemble": "r6i1p1f1",
    }

def get_correct_forcing_lumped(name):
    """
    For Lumped model get the correct custom forcing data for the correct test.
    """
    if "zero" in name:
        return get_zeroes_lumped_scenario()
    elif 'permanent' in name:
        return get_non_zeroes_lumped_scenario()
    elif "decrease" in name:
        return get_decreasing_scenario()
    elif "increase" in name:
        return get_increasing_scenario()
    elif "mid" in name:
        return get_mid_spike_lumped_scenario()
    elif "start" in name:
        return get_start_spike_lumped_scenario()
    elif "end" in name:
        return get_end_spike_lumped_scenario()
    elif "first_half" in name:
        return get_first_half_precip_lumped_scenario()
    elif "second_half" in name:
        return get_second_half_precip_lumped_scenario()
    elif "pre_existing" in name:
        return get_zeroes_lumped_scenario()
    else:
        return


def get_correct_forcing_distributed(name):
    """
    For Distributed model get the correct custom forcing data for the correct test.
    """
    if "zero" in name:
        return get_zeroes_distributed_scenario()
    elif 'permanent' in name:
        return get_non_zeroes_distributed_scenario()
    elif "decrease" in name:
        return get_decreasing_scenario()
    elif "increase" in name:
        return get_increasing_scenario()
    elif "mid" in name:
        return get_mid_spike_distributed_scenario()
    elif "start" in name:
        return get_start_spike_distributed_scenario()
    elif "end" in name:
        return get_end_spike_distributed_scenario()
    elif "first_half" in name:
        return get_first_half_precip_distributed_scenario()
    elif "second_half" in name:
        return get_second_half_precip_distributed_scenario()
    elif "pre_existing" in name:
        return get_zeroes_distributed_scenario()
    else:
        return

def get_zeroes_lumped_scenario():
    """Get a scenario in which there is no precipitation
     throughout the data for a lumped model.

    Returns:
        GenericLumpedForcing: a scenario
        in which there is no precipitation throughout the data.
    """
    forcing = GenericLumpedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    for a in enumerate(data['pr'].values):
        data['pr'].values[a[0]] = 0
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_zeroes_distributed_scenario():
    """Get a scenario in which there is no precipitation
    throughout the data for a distributed model.

    Returns:
        GenericDistributedForcing: a scenario
        in which there is no precipitation throughout the data.
    """
    forcing = GenericDistributedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    for a in enumerate(data['pr'].values):
        for grid in data['pr'].values[a[0]]:
            for i in range(0,len(grid)):
                grid[i] = 0
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_non_zeroes_lumped_scenario():
    """Get a scenario in which there is constant precipitation
     throughout the data for a lumped model.

    Returns:
        GenericLumpedForcing: a scenario
         in which there is constant precipitation throughout the data.
    """
    forcing = GenericLumpedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    for a in enumerate(data['pr'].values):
        if data['pr'].values[a[0]] == 0:
            data['pr'].values[a[0]] = random.randrange(1, 100, 1) * 0.0000001
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_non_zeroes_distributed_scenario():
    """Get a scenario in which there is constant precipitation
     throughout the data for a distributed model.

    Returns:
        GenericDistributedForcing: a scenario
         in which there is constant precipitation throughout the data.
    """
    forcing = GenericDistributedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    for a in enumerate(data['pr'].values):
        for grid in data['pr'].values[a[0]]:
            for i in range(0, len(grid)):
                if grid[i] == 0 or math.isnan(grid[i]):
                    grid[i] = random.randrange(1, 100, 1) * 0.0000001
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_increasing_scenario():
    """Get a scenario in which precipitation increases
     throughout the data for a lumped model.

    Returns:
        GenericLumpedForcing: a scenario
         in which precipitation increases throughout the data.
    """
    forcing = GenericLumpedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    number = 0.0000001
    for a in enumerate(data['pr'].values):
        data['pr'].values[a[0]] = number
        number = number + 0.0000001
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_decreasing_scenario():
    """Get a scenario in which precipitation decreases
     throughout the data for a lumped model.

    Returns:
        GenericLumpedForcing: a scenario
         in which precipitation decreases throughout the data.
    """
    forcing = GenericLumpedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    number = 0.001
    for a in enumerate(data['pr'].values):
        data['pr'].values[a[0]] = number
        number = number - 0.0000001
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_mid_spike_lumped_scenario():
    """Get a scenario in which there's a big precipitation spike
     in the middle of the data for a lumped model.

    Returns:
        GenericLumpedForcing: a scenario in which
         there's a big precipitation spike in the middle of the data.
    """
    forcing = GenericLumpedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    number = 0.001
    spike = len(data['pr'].values) / 2
    counter = 0
    for a in enumerate(data['pr'].values):
        if counter == spike:
            data['pr'].values[a[0]] = number
        else:
            data['pr'].values[a[0]] = random.randrange(1, 100, 1) * 0.00000001
        counter = counter + 1
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_mid_spike_distributed_scenario():
    """Get a scenario in which there's a big precipitation spike
     in the middle of the data for a distributed model.

    Returns:
        GenericDistributedForcing: a scenario in which
         there's a big precipitation spike in the middle of the data.
    """
    forcing = GenericDistributedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    number = 0.001
    spike = len(data['pr'].values) / 2
    counter = 0
    for a in enumerate(data['pr'].values):
        for grid in data['pr'].values[a[0]]:
            for i in range(0, len(grid)):
                if counter == spike:
                    grid[i] = number
                else:
                    grid[i] = random.randrange(1, 100, 1) * 0.00000001
        counter = counter + 1
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_start_spike_lumped_scenario():
    """Get a scenario in which there's a big precipitation spike
     at the start of the data for a lumped model.

    Returns:
        GenericLumpedForcing: a scenario in which
         there's a big precipitation spike at the start of the data.
    """
    forcing = GenericLumpedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    number = 0.001
    spike = math.floor(len(data['pr'].values) / 10)
    counter = 0
    for a in enumerate(data['pr'].values):
        if counter == spike:
            data['pr'].values[a[0]] = number
        else:
            data['pr'].values[a[0]] = random.randrange(1, 100, 1) * 0.00000001
        counter = counter + 1
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_start_spike_distributed_scenario():
    """Get a scenario in which there's a big precipitation spike
     at the start of the data for a distributed model.

    Returns:
        GenericDistributedForcing: a scenario in which
         there's a big precipitation spike at the start of the data.
    """
    forcing = GenericDistributedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    number = 0.001
    spike = math.floor(len(data['pr'].values) / 10)
    counter = 0
    for a in enumerate(data['pr'].values):
        for grid in data['pr'].values[a[0]]:
            for i in range(0, len(grid)):
                if counter == spike:
                    grid[i] = number
                else:
                    grid[i] = random.randrange(1, 100, 1) * 0.00000001
        counter = counter + 1
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_end_spike_lumped_scenario():
    """Get a scenario in which there's a big precipitation spike
     at the end of the data for a lumped model.

    Returns:
        GenericLumpedForcing: a scenario in which
         there's a big precipitation spike at the end of the data.
    """
    forcing = GenericLumpedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    number = 0.001
    spike = math.floor(len(data['pr'].values) * 0.8)
    counter = 0
    for a in enumerate(data['pr'].values):
        if counter == spike:
            data['pr'].values[a[0]] = number
        else:
            data['pr'].values[a[0]] = random.randrange(1, 100, 1) * 0.00000001
        counter = counter + 1
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_end_spike_distributed_scenario():
    """Get a scenario in which there's a big precipitation spike
     at the end of the data for a distributed model.

    Returns:
        GenericDistributedForcing: a scenario in which
        there's a big precipitation spike at the end of the data.
    """
    forcing = GenericDistributedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    number = 0.001
    spike = math.floor(len(data['pr'].values) * 0.8)
    counter = 0
    for a in enumerate(data['pr'].values):
        for grid in data['pr'].values[a[0]]:
            for i in range(0, len(grid)):
                if counter == spike:
                    grid[i] = number
                else:
                    grid[i] = random.randrange(1, 100, 1) * 0.00000001
        counter = counter + 1
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_second_half_precip_lumped_scenario():
    """Get a scenario in which precipitation only occurs
     in the second half of the data for a lumped model.

    Returns:
        GenericLumpedForcing: a scenario in which
         precipitation only occurs in the second half of the data.
    """
    forcing = GenericLumpedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    length = len(data['pr'].values)
    for a in range(math.floor(length/2)):
        data['pr'].values[a] = 0
    for a in range(math.ceil(length/2),length):
        data['pr'].values[a] = random.randrange(1, 100, 1) * 0.0000001
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_second_half_precip_distributed_scenario():
    """Get a scenario in which precipitation only occurs
     in the second half of the data for a distributed model.

    Returns:
        GenericDistributedForcing: a scenario in which
         precipitation only occurs in the second half of the data.
    """
    forcing = GenericDistributedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    length = len(data['pr'].values)
    for a in range(math.floor(length/2)):
        for grid in data['pr'].values[a]:
            for i in range(0, len(grid)):
                grid[i] = 0
    for a in range(math.ceil(length/2),length):
        for grid in data['pr'].values[a]:
            for i in range(0, len(grid)):
                grid[i] = random.randrange(1, 100, 1) * 0.0000001
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_first_half_precip_lumped_scenario():
    """Get a scenario in which precipitation only occurs
     in the first half of the data for a lumped model.

    Returns:
        GenericLumpedForcing: a scenario in which
        precipitation only occurs in the first half of the data.
    """
    forcing = GenericLumpedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    length = len(data['pr'].values)
    for a in range(math.floor(length/2)):
        data['pr'].values[a] = random.randrange(1, 100, 1) * 0.0000001
    for a in range(math.ceil(length/2),length):
        data['pr'].values[a] = 0
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing

def get_first_half_precip_distributed_scenario():
    """Get a scenario in which precipitation only occurs
     in the first half of the data for a distributed model.

    Returns:
        GenericDistributedForcing: a scenario in which
         precipitation only occurs in the first half of the data.
    """
    forcing = GenericDistributedForcing.generate(
        dataset=cmip_dataset,
        start_time="2000-01-01T00:00:00Z",
        end_time="2000-12-31T00:00:00Z",
        shape=shape.absolute(),
    )
    path = str(forcing.directory) + "/" + forcing.filenames.get('pr')
    data = xr.open_dataset(path)
    length = len(data['pr'].values)
    for a in range(math.floor(length/2)):
        for grid in data['pr'].values[a]:
            for i in range(0, len(grid)):
                grid[i] = random.randrange(1, 100, 1) * 0.0000001
    for a in range(math.ceil(length/2),length):
        for grid in data['pr'].values[a]:
            for i in range(0, len(grid)):
                grid[i] = 0
    data.to_netcdf(str(forcing.directory) + "/" + 'data.nc')
    forcing.filenames['pr'] = 'data.nc'
    return forcing
