"""
Tests for the configuration module.
"""

import pytest
from config import ANIMATION, COLORS, MATH, SCENE, get_resolution, get_camera_orientation


def test_animation_config():
    """Test AnimationConfig default values."""
    assert ANIMATION.default_wait_time == 1.0
    assert ANIMATION.fast_wait_time == 0.5
    assert ANIMATION.slow_wait_time == 2.0
    assert ANIMATION.high_resolution == (32, 32)


def test_color_config():
    """Test ColorConfig default values."""
    assert COLORS.rotation_color == "RED"
    assert COLORS.translation_color == "BLUE"
    assert COLORS.algebra_color == "GREEN"
    assert COLORS.manifold_color == "BLUE"


def test_math_config():
    """Test MathConfig default values."""
    assert MATH.small_rotation_angle == 0.4
    assert MATH.medium_rotation_angle == 1.5
    assert MATH.large_rotation_angle == 2.5
    assert MATH.keyframe_threshold == 20


def test_scene_config():
    """Test SceneConfig default values."""
    assert SCENE.cube_size == 1.2
    assert SCENE.sphere_radius == 2.0
    assert SCENE.plane_size == 3.5


def test_get_resolution():
    """Test get_resolution function."""
    assert get_resolution("low") == (8, 8)
    assert get_resolution("medium") == (16, 16)
    assert get_resolution("high") == (32, 32)
    assert get_resolution("invalid") == (16, 16)  # default


def test_get_camera_orientation():
    """Test get_camera_orientation function."""
    assert get_camera_orientation("default") == (75, -80, 0.8)
    assert get_camera_orientation("so3") == (65, -120, 0.9)
    assert get_camera_orientation("se3") == (70, -110, 0.9)
    assert get_camera_orientation("invalid") == (75, -80, 0.8)  # default 