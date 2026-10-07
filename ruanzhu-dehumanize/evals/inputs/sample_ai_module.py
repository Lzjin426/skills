# -*- coding: utf-8 -*-
"""
Gear Contact Stress Calculation Module.

This module implements Hertzian contact stress calculation for spur gears
based on ISO 6336 standard.

Copyright (c) 2026 Wind Power Research Lab.
Author: Zhang San <zhangsan@research-lab.cn>
Created on: 2026-02-18
License: Apache-2.0
"""

import math
import logging
from typing import Optional, Tuple, Dict, List
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GearParameters:
    """Represents the geometric and material parameters of a gear.

    Attributes:
        module_coefficient: The module of the gear in millimeters.
        number_of_teeth: The number of teeth on the gear.
        face_width: The face width of the gear in millimeters.
        elastic_modulus: The elastic modulus of the gear material in MPa.
        poisson_ratio: The Poisson's ratio of the gear material.
    """
    module_coefficient: float
    number_of_teeth: int
    face_width: float
    elastic_modulus: float
    poisson_ratio: float


def calculate_hertzian_contact_stress(
    pinion_parameters: GearParameters,
    wheel_parameters: GearParameters,
    transmitted_torque: float,
    pressure_angle_degrees: float = 20.0
) -> float:
    """Calculate the Hertzian contact stress between two meshing gears.

    Args:
        pinion_parameters: The parameters of the pinion gear.
        wheel_parameters: The parameters of the wheel gear.
        transmitted_torque: The torque transmitted through the gear pair in Nm.
        pressure_angle_degrees: The pressure angle in degrees (default 20.0).

    Returns:
        The Hertzian contact stress in MPa.

    Raises:
        ValueError: If any input parameter is non-positive.
    """
    try:
        if transmitted_torque <= 0:
            raise ValueError("Transmitted torque must be positive")

        pressure_angle_radians: float = math.radians(pressure_angle_degrees)

        pinion_pitch_diameter: float = (
            pinion_parameters.module_coefficient
            * pinion_parameters.number_of_teeth
        )
        wheel_pitch_diameter: float = (
            wheel_parameters.module_coefficient
            * wheel_parameters.number_of_teeth
        )

        tangential_force: float = (
            2.0 * transmitted_torque * 1000.0 / pinion_pitch_diameter
        )

        gear_ratio: float = wheel_pitch_diameter / pinion_pitch_diameter

        equivalent_elastic_modulus: float = 1.0 / (
            (1.0 - pinion_parameters.poisson_ratio ** 2)
            / pinion_parameters.elastic_modulus
            + (1.0 - wheel_parameters.poisson_ratio ** 2)
            / wheel_parameters.elastic_modulus
        )

        match pressure_angle_degrees:
            case 20.0:
                zone_factor = 2.495
            case 25.0:
                zone_factor = 2.291
            case _:
                zone_factor = 2.495

        contact_stress: float = zone_factor * math.sqrt(
            tangential_force / (
                pinion_parameters.face_width * pinion_pitch_diameter
            )
            * (gear_ratio + 1.0) / gear_ratio
            * equivalent_elastic_modulus
        )

        logger.info(f"Contact stress calculated: {contact_stress=:.2f} MPa")
        return contact_stress

    except Exception as calculation_exception:
        logger.error(
            f"Contact stress calculation failed: {calculation_exception}"
        )
        raise


def evaluate_safety_factor(
    actual_stress_value: float,
    allowable_stress_value: float
) -> Dict[str, float]:
    """Evaluate the safety factor based on actual and allowable stress.

    Args:
        actual_stress_value: The actual contact stress in MPa.
        allowable_stress_value: The allowable contact stress in MPa.

    Returns:
        A dictionary containing the safety factor and status.
    """
    safety_factor_value: float = allowable_stress_value / actual_stress_value
    evaluation_result: Dict[str, float] = {
        "safety_factor": safety_factor_value,
        "is_safe": 1.0 if safety_factor_value >= 1.2 else 0.0
    }
    return evaluation_result
