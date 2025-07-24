import numpy as np
from manim import *

class SE3Visualization(ThreeDScene):
    """
    A Manim scene to visualize a transformation in the Special Euclidean group SE(3),
    which represents a full rigid-body motion (rotation and translation).
    This is often called a "twist".
    """
    def construct(self):
        # --- 1. Scene Setup ---
        self.set_camera_orientation(phi=70 * DEGREES, theta=-110 * DEGREES, zoom=0.9)
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-3, 3, 1],
            x_length=10,
            y_length=10,
            z_length=6,
        )

        title = Text("SE(3) Transformation: A Rigid Body Motion (Pose)").scale(0.8).to_edge(UP)
        subtitle = Text("Rotation + Translation = Twist", font_size=36).next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(title, subtitle)

        self.add(axes)

        # --- 2. Create a Camera-like Object ---
        # We'll build a simple camera from primitive shapes to represent our rigid body.
        camera_body = Prism(dimensions=[1, 1.5, 0.7]).set_color(GRAY_BROWN)
        camera_lens = Cylinder(
            radius=0.3,
            height=0.6,
            direction=OUT
        ).set_color(DARK_GRAY).next_to(camera_body, OUT, buff=0)
        
        camera_object = VGroup(camera_body, camera_lens)
        camera_object.move_to(np.array([-4, -2, 0]))
        
        # Add a dot to the center to make tracing its path easier to see
        center_dot = Dot3D(camera_object.get_center(), color=YELLOW, radius=0.05)

        self.play(FadeIn(camera_object), FadeIn(center_dot))
        self.wait(1)

        # --- 3. Define the SE(3) Transformation ---
        # An element of se(3) (a twist) defines this motion.
        # It has a rotational part and a translational part.
        rotation_angle = 1.5 * PI  # The amount of rotation
        rotation_axis = UP         # The axis of rotation
        translation_vector = RIGHT * 8 + UP * 4 # The total translation

        # --- 4. Animate the Transformation ---
        # A tracer will draw the path of the camera's center.
        # The resulting helical path is characteristic of a twist.
        path_tracer = TracedPath(center_dot.get_center, stroke_color=YELLOW, stroke_width=5)
        self.add(path_tracer)

        # We apply the rotation and translation simultaneously in one play() call.
        # Manim's 'Rotate' is about a point, while the translation is a 'shift'.
        # We also need to animate the dot moving with the camera.
        self.play(
            Rotate(
                camera_object,
                angle=rotation_angle,
                axis=rotation_axis,
                about_point=camera_object.get_center()
            ),
            camera_object.animate.shift(translation_vector),
            UpdateFromFunc(center_dot, lambda m: m.move_to(camera_object.get_center())),
            run_time=8,
            rate_func=linear
        )
        self.wait(2)

        # Final camera move to appreciate the full path
        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, zoom=0.8, run_time=2)
        self.wait(3)