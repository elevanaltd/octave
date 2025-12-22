"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def sample_octave_content():
    """Sample OCTAVE content for testing."""
    return """===SAMPLE===
META:
  TYPE::"TEST"
  VERSION::"1.0"

§1::SECTION_ONE
KEY::"value"

===END==="""
