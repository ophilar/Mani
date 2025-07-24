"""
Configuration file for SLAM Manim visualizations.

This file contains customizable parameters for animations, including timing,
colors, resolutions, and other visual settings.
"""

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass
class AnimationConfig:
    """Configuration for animation timing and behavior."""
    
    # General timing
    default_wait_time: float = 1.0
    fast_wait_time: float = 0.5
    slow_wait_time: float = 2.0
    
    # Animation durations
    short_animation: float = 1.5
    medium_animation: float = 3.0
    long_animation: float = 5.0
    
    # Camera settings
    default_zoom: float = 0.8
    close_zoom: float = 1.2
    far_zoom: float = 0.6
    
    # Performance settings
    high_resolution: Tuple[int, int] = (32, 32)
    medium_resolution: Tuple[int, int] = (16, 16)
    low_resolution: Tuple[int, int] = (8, 8)


@dataclass
class ColorConfig:
    """Configuration for color schemes."""
    
    # Primary colors for different concepts
    rotation_color: str = "RED"
    translation_color: str = "BLUE"
    algebra_color: str = "GREEN"
    manifold_color: str = "BLUE"
    object_color: str = "PURPLE"
    
    # Secondary colors
    highlight_color: str = "YELLOW"
    success_color: str = "GREEN"
    error_color: str = "RED"
    warning_color: str = "ORANGE"
    
    # Background and text
    background_color: str = "BLACK"
    text_color: str = "WHITE"


@dataclass
class MathConfig:
    """Configuration for mathematical parameters."""
    
    # Vector magnitudes for demonstrations
    small_rotation_angle: float = 0.4  # radians
    medium_rotation_angle: float = 1.5  # radians
    large_rotation_angle: float = 2.5  # radians
    
    # Translation distances
    small_translation: float = 2.0
    medium_translation: float = 5.0
    large_translation: float = 8.0
    
    # Noise parameters for drift simulation
    initial_noise_level: float = 0.0
    noise_increment: float = 0.08
    
    # SLAM parameters
    keyframe_threshold: int = 20
    cost_per_keyframe: int = 5
    cost_per_frame: int = 1


@dataclass
class SceneConfig:
    """Configuration for scene setup."""
    
    # 3D scene dimensions
    axes_range: Tuple[float, float, float] = (-5, 5, 1)
    axes_length: Tuple[float, float, float] = (10, 10, 6)
    
    # Object sizes
    cube_size: float = 1.2
    sphere_radius: float = 2.0
    plane_size: float = 3.5
    
    # Camera orientations (phi, theta, zoom)
    default_camera: Tuple[float, float, float] = (75, -80, 0.8)
    so3_camera: Tuple[float, float, float] = (65, -120, 0.9)
    se3_camera: Tuple[float, float, float] = (70, -110, 0.9)


# Global configuration instances
ANIMATION = AnimationConfig()
COLORS = ColorConfig()
MATH = MathConfig()
SCENE = SceneConfig()


def get_resolution(quality: str = "medium") -> Tuple[int, int]:
    """Get resolution based on quality setting."""
    resolutions = {
        "low": ANIMATION.low_resolution,
        "medium": ANIMATION.medium_resolution,
        "high": ANIMATION.high_resolution,
    }
    return resolutions.get(quality, ANIMATION.medium_resolution)


def get_camera_orientation(scene_type: str = "default") -> Tuple[float, float, float]:
    """Get camera orientation based on scene type."""
    orientations = {
        "default": SCENE.default_camera,
        "so3": SCENE.so3_camera,
        "se3": SCENE.se3_camera,
    }
    return orientations.get(scene_type, SCENE.default_camera) 