from manim import *

class SO3RotationVisualization(ThreeDScene):
    """
    A Manim scene to visualize a 3D rotation, representing an element
    of the Special Orthogonal group SO(3).
    """
    def construct(self):
        # Set up the 3D coordinate system for context
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            z_length=8,
        )

        # Set the camera's position and orientation for a better view
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Create a cube that will be rotated
        cube = Cube(side_length=2, fill_opacity=0.7, fill_color=BLUE_E)
        
        # Add a title that remains fixed on the screen during the animation
        title = Text("SO(3): Rotation in 3D Space").to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)

        # Display the axes and the cube in their initial state
        self.add(axes, cube)
        self.wait(1)

        # Animate the rotation of the cube. This transformation is an
        # element of SO(3).
        self.play(
            Rotate(cube, angle=2 * PI, axis=UP, about_point=ORIGIN),
            run_time=6,
            rate_func=linear
        )
        self.wait(2)