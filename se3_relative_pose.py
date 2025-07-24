import numpy as np
from scipy.spatial.transform import Rotation as R
from manim import *

class SE3RelativePose(ThreeDScene):
    """
    A Manim scene to visualize the SE(3) transformation that maps
    one camera pose to another.
    """
    def create_camera_object(self, color=GRAY_BROWN):
        """Creates a VGroup representing a simple camera."""
        camera_body = Prism(dimensions=[0.7, 1.0, 0.5]).set_color(color)
        camera_lens = Cylinder(
            radius=0.2,
            height=0.4,
            direction=OUT
        ).set_color(DARK_GRAY).next_to(camera_body, OUT, buff=0)
        # Add a small "up" indicator
        up_indicator = Triangle(fill_opacity=1, color=RED).scale(0.1).next_to(camera_body, UP, buff=0)
        camera_object = VGroup(camera_body, camera_lens, up_indicator)
        return camera_object

    def construct(self):
        # --- 1. Scene Setup ---
        self.set_camera_orientation(phi=75 * DEGREES, theta=-75 * DEGREES, zoom=1)
        axes = ThreeDAxes(x_length=8, y_length=8, z_length=6)
        world_label = Text("World Frame", font_size=24).next_to(axes, OUT, buff=0.5)

        title = Text("Relative SE(3) Transformation Between Poses").scale(0.7).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.add(axes, world_label)

        # --- 2. Define Two Camera Poses (4x4 Homogeneous Matrices) ---
        # Pose A: The starting pose of the camera in the world frame
        rot_A_mat = R.from_euler('xyz', [10, 70, 0], degrees=True).as_matrix()
        trans_A_vec = np.array([-2, -1, 0.5])
        pose_A = np.eye(4)
        pose_A[:3, :3] = rot_A_mat
        pose_A[:3, 3] = trans_A_vec

        # Pose B: The target pose of the camera in the world frame
        rot_B_mat = R.from_euler('xyz', [-20, -45, 15], degrees=True).as_matrix()
        trans_B_vec = np.array([2, 2, -0.5])
        pose_B = np.eye(4)
        pose_B[:3, :3] = rot_B_mat
        pose_B[:3, 3] = trans_B_vec

        # --- 3. Create and Place the Camera Objects ---
        camera_A = self.create_camera_object(color=BLUE)
        camera_A.apply_matrix(pose_A) # Apply the pose transformation
        label_A = MathTex("T_{WA}", color=BLUE).next_to(camera_A, UP, buff=0.3)

        camera_B = self.create_camera_object(color=GREEN)
        camera_B.apply_matrix(pose_B).set_opacity(0.4) # Make target semi-transparent
        label_B = MathTex("T_{WB}", color=GREEN).next_to(camera_B, UP, buff=0.3)

        self.play(
            FadeIn(camera_A), Write(label_A),
            FadeIn(camera_B), Write(label_B),
            run_time=1.5
        )
        self.wait(1)

        # --- 4. Calculate and Explain the Relative Transformation ---
        # The transformation from A to B is: T_BA = inv(T_WA) * T_WB
        pose_A_inv = np.linalg.inv(pose_A)
        relative_pose_B_from_A = pose_A_inv @ pose_B

        formula = MathTex(
            r"T_{BA} = T_{WA}^{-1} \cdot T_{WB}",
            font_size=48
        ).to_corner(DR)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))
        self.wait(1)

        # --- 5. Animate the Transformation ---
        # Create a new camera that will move from A to B
        camera_moving = self.create_camera_object(color=YELLOW)
        camera_moving.apply_matrix(pose_A) # Start it at the exact same pose as A

        # Add a tracer to show the path
        path_tracer = TracedPath(camera_moving.get_center, stroke_color=YELLOW, stroke_width=6)

        self.add(path_tracer)
        self.play(
            FadeIn(camera_moving, scale=1.2)
        )
        
        # The core animation: apply the relative transformation matrix.
        # ApplyMatrix transforms the mobject from its current state.
        self.play(
            ApplyMatrix(relative_pose_B_from_A, camera_moving),
            run_time=5,
            rate_func=smooth
        )
        self.wait(0.5)

        # Make the moving camera flash to confirm it has reached the target
        self.play(
            Flash(camera_moving, color=WHITE, flash_radius=1.5)
        )
        self.wait(1)

        # Fade out the moving camera to show it landed perfectly on the target
        self.play(FadeOut(camera_moving))
        self.wait(3)