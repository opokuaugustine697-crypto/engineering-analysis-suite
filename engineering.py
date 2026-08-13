"""Engineering calculation classes and functions used by the Streamlit app."""

import math
from dataclasses import dataclass


@dataclass
class Fluid:
    """Represent a fluid with density and dynamic viscosity."""

    name: str
    density: float  # kg/m^3
    viscosity: float  # Pa.s


@dataclass
class Pipe:
    """Represent a circular pipe and calculate flow quantities."""

    diameter: float  # m
    length: float  # m
    roughness: float  # m

    def velocity(self, flow_rate: float) -> float:
        """Return average pipe velocity in m/s from volumetric flow rate in m^3/s."""
        if self.diameter <= 0:
            raise ValueError("Pipe diameter must be greater than zero.")
        if flow_rate < 0:
            raise ValueError("Flow rate cannot be negative.")
        area = math.pi * self.diameter**2 / 4
        return flow_rate / area

    def reynolds_number(self, flow_rate: float, fluid: Fluid) -> float:
        """Return Reynolds number for the pipe flow."""
        if fluid.density <= 0 or fluid.viscosity <= 0:
            raise ValueError("Fluid density and viscosity must be greater than zero.")
        velocity = self.velocity(flow_rate)
        return fluid.density * velocity * self.diameter / fluid.viscosity

    def friction_factor(self, flow_rate: float, fluid: Fluid) -> float:
        """Return Darcy friction factor using laminar or Haaland turbulent flow."""
        re = self.reynolds_number(flow_rate, fluid)
        if re == 0:
            return 0.0
        if re < 2300:
            return 64 / re
        relative_roughness = self.roughness / self.diameter
        return 1 / (
            -1.8 * math.log10(
                (relative_roughness / 3.7) ** 1.11 + 6.9 / re
            )
        ) ** 2

    def pressure_drop(self, flow_rate: float, fluid: Fluid) -> float:
        """Return Darcy-Weisbach pressure drop in Pa."""
        if self.length < 0 or self.roughness < 0:
            raise ValueError("Length and roughness cannot be negative.")
        velocity = self.velocity(flow_rate)
        friction = self.friction_factor(flow_rate, fluid)
        return friction * (self.length / self.diameter) * (
            fluid.density * velocity**2 / 2
        )


def conduction_heat_rate(
    thermal_conductivity: float,
    area: float,
    hot_temperature: float,
    cold_temperature: float,
    thickness: float,
) -> float:
    """Return steady one-dimensional wall heat-transfer rate in W."""
    if thermal_conductivity <= 0 or area <= 0 or thickness <= 0:
        raise ValueError("Conductivity, area, and thickness must be positive.")
    return thermal_conductivity * area * (hot_temperature - cold_temperature) / thickness


def cooling_time(
    initial_temperature: float,
    target_temperature: float,
    ambient_temperature: float,
    h: float,
    area: float,
    mass: float,
    specific_heat: float,
) -> float:
    """Return lumped-capacitance cooling time in seconds.

    The analytical solution is:
        (T - T_inf)/(T0 - T_inf) = exp(-h*A*t/(m*c))
    """
    if h <= 0 or area <= 0 or mass <= 0 or specific_heat <= 0:
        raise ValueError("h, area, mass, and specific heat must be positive.")
    if (initial_temperature - ambient_temperature) == 0:
        raise ValueError("Initial temperature must differ from ambient temperature.")
    ratio = (target_temperature - ambient_temperature) / (
        initial_temperature - ambient_temperature
    )
    if ratio <= 0 or ratio >= 1:
        raise ValueError(
            "For cooling, target temperature must lie strictly between ambient and initial temperature."
        )
    return -(mass * specific_heat / (h * area)) * math.log(ratio)


def cooling_temperature(
    time_seconds: float,
    initial_temperature: float,
    ambient_temperature: float,
    h: float,
    area: float,
    mass: float,
    specific_heat: float,
) -> float:
    """Return object temperature in °C at a specified time using Newton cooling."""
    if h <= 0 or area <= 0 or mass <= 0 or specific_heat <= 0:
        raise ValueError("h, area, mass, and specific heat must be positive.")
    return ambient_temperature + (initial_temperature - ambient_temperature) * math.exp(
        -h * area * time_seconds / (mass * specific_heat)
    )
