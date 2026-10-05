"""Unit tests for the Field model."""

import pytest
from app.models.field import Field


def test_field_creation_valid() -> None:
    f = Field("F01", 1000.0, "Wheat", 35.0, 40.0, 5)
    assert f.field_id == "F01"
    assert f.area == 1000.0
    assert f.crop == "Wheat"
    assert f.moisture_threshold == 35.0
    assert f.water_requirement == 40.0
    assert f.priority == 5


def test_field_invalid_area() -> None:
    with pytest.raises(ValueError, match="area must be positive"):
        Field("F01", 0.0, "Wheat", 35.0, 40.0, 5)


def test_field_invalid_threshold() -> None:
    with pytest.raises(ValueError, match="moisture_threshold"):
        Field("F01", 100.0, "Wheat", 105.0, 40.0, 5)


def test_field_invalid_priority() -> None:
    with pytest.raises(ValueError, match="priority must be between 1 and 5"):
        Field("F01", 100.0, "Wheat", 35.0, 40.0, 6)
