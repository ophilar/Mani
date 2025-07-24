import numpy as np
from scipy.spatial.transform import Rotation
from manim import *

class SO3CompositionVsAddition(ThreeDScene):
    """
    A Manim scene that contrasts the composition of two rotations in the SO(3) group
    with the addition of their corresponding vectors in the so(3) Lie algebra.
    It demonstrates that for small rotations, addition in the algebra approximates
    composition in the group.
    """
    def construct(self):
        # --- 1. Scene Setup ---
        self.set_camera_orientation(phi=60 * DEGREES, theta=-100 * DEGREES, zoom=0.8)
        title = Text("Group Composition vs. Algebra Addition").scale(0.8).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)

        # Create the three visual areas
        manifold_group, algebra_group, object_group = self.setup_visual_areas()
        self.play(
            FadeIn(manifold_group),
            FadeIn(algebra_group),
            FadeIn(object_group),
            run_time=1.5
        )
        self.wait(0.5)

        # --- 2. Run comparison for LARGE rotations ---
        subtitle_large = Text("Case 1: Large Rotations", font_size=32).to_corner(UL)
        self.add_fixed_in_frame_mobjects(subtitle_large)
        self.play(Write(subtitle_large))

        # Define two large rotation vectors in the tangent plane's coordinates
        v1 = RIGHT * 1.5  # 1.5 radians around Y-axis
        v2 = UP * 1.5     # 1.5 radians around X-axis

        # Run the main animation logic
        final_mobjects = self.run_comparison(v1, v2, manifold_group, algebra_group, object_group)

        # Highlight the non-equivalence
        inequality_text = MathTex(r"g_1 g_2 \neq \exp(\mathbf{v}_1 + \mathbf{v}_2)", font_size=48).to_corner(DR)
        self.add_fixed_in_frame_mobjects(inequality_text)
        self.play(Write(inequality_text))
        self.wait(2)

        # --- 3. Cleanup and Reset ---
        self.play(
            FadeOut(inequality_text),
            FadeOut(subtitle_large),
            *[FadeOut(mob) for mob in final_mobjects]
        )
        # Reset the cube to its original state
        cube = object_group.get_submob_by_tex("cube")
        cube.become(Cube(side_length=1.2, fill_opacity=0.8, fill_color=PURPLE).move_to(cube.get_center()))
        self.wait(1)

        # --- 4. Run comparison for SMALL rotations ---
        subtitle_small = Text("Case 2: Small Rotations (The Approximation)", font_size=32).to_corner(UL)
        self.add_fixed_in_frame_mobjects(subtitle_small)
        self.play(Write(subtitle_small))

        v1_small = RIGHT * 0.4
        v2_small = UP * 0.4

        final_mobjects_small = self.run_comparison(v1_small, v2_small, manifold_group, algebra_group, object_group)

        # Highlight the approximation
        approx_text = MathTex(r"g_1 g_2 \approx \exp(\mathbf{v}_1 + \mathbf{v}_2)", font_size=48).to_corner(DR)
        self.add_fixed_in_frame_mobjects(approx_text)
        self.play(Write(approx_text))
        self.wait(3)

    def setup_visual_areas(self):
        """Creates and positions the manifold, algebra, and object displays."""
        # Manifold (Sphere)
        manifold_group = VGroup()
        sphere = Sphere(radius=2, resolution=(32, 32)).set_color(BLUE).set_opacity(0.2)
        identity_dot = Dot3D(sphere.get_top(), color=YELLOW)
        manifold_group.add(sphere, identity_dot).move_to(LEFT * 4)

        # Lie Algebra (Tangent Plane)
        algebra_group = VGroup()
        plane = Square(side_length=3.5, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.2).set_shade_in_3d(True)
        algebra_group.add(plane).move_to(manifold_group.get_center() + sphere.get_top())

        # 3D Object (Cube)
        object_group = VGroup()
        axes = ThreeDAxes(x_range=[-2,2], y_range=[-2,2], z_range=[-2,2], x_length=3, y_length=3, z_length=3)
        cube = Cube(side_length=1.2, fill_opacity=0.8, fill_color=PURPLE).set_shade_in_3d(True)
        cube.set_default_tex("cube") # Name for easy retrieval
        object_group.add(axes, cube).move_to(RIGHT * 4)

        return manifold_group, algebra_group, object_group

    def run_comparison(self, v1_vec, v2_vec, manifold_group, algebra_group, object_group):
        """The core animation logic for a given pair of vectors."""
        sphere = manifold_group[0]
        plane = algebra_group[0]
        cube = object_group.get_submob_by_tex("cube")
        
        # --- Part A: Vector addition in the algebra ---
        v1_arrow = Arrow3D(plane.get_center(), plane.get_center() + v1_vec, color=RED)
        v2_arrow = Arrow3D(plane.get_center(), plane.get_center() + v2_vec, color=ORANGE)
        v_sum_vec = v1_vec + v2_vec
        v_sum_arrow = Arrow3D(plane.get_center(), plane.get_center() + v_sum_vec, color=TEAL, thickness=0.03)
        
        self.play(GrowArrow(v1_arrow), GrowArrow(v2_arrow))
        self.play(TransformFromCopy(VGroup(v1_arrow, v2_arrow), v_sum_arrow))
        
        # Map the sum to the manifold
        g_sum_point = sphere.get_center() + normalize(plane.get_center() + v_sum_vec - sphere.get_center()) * sphere.radius
        g_sum_dot = Dot3D(g_sum_point, color=TEAL, radius=0.1)
        sum_path = ArcBetweenPoints(v_sum_arrow.get_end(), g_sum_point, color=TEAL)
        
        # Create a copy of the cube to show the result of the summed rotation
        cube_sum_final = cube.copy().set_opacity(0.4)
        
        self.play(
            Create(sum_path), Create(g_sum_dot),
            Rotate(
                cube_sum_final,
                angle=np.linalg.norm(v_sum_vec),
                axis=normalize(v_sum_vec),
                about_point=cube_sum_final.get_center()
            ),
            run_time=2
        )
        self.add(cube_sum_final)
        self.wait(1)

        # --- Part B: Group composition on the manifold ---
        # 1. First rotation (v1)
        g1_point = sphere.get_center() + normalize(plane.get_center() + v1_vec - sphere.get_center()) * sphere.radius
        g1_dot = Dot3D(g1_point, color=RED, radius=0.1)
        path1 = ArcBetweenPoints(v1_arrow.get_end(), g1_point, color=RED)
        
        self.play(
            Create(path1), Create(g1_dot),
            Rotate(
                cube,
                angle=np.linalg.norm(v1_vec),
                axis=normalize(v1_vec),
                about_point=cube.get_center()
            ),
            run_time=2
        )

        # 2. Second rotation (v2)
        # Use scipy to calculate the true composition
        rot1 = Rotation.from_rotvec(v1_vec)
        rot2 = Rotation.from_rotvec(v2_vec)
        rot_comp = rot2 * rot1 # Composition: apply rot1, then rot2
        v_comp_vec = rot_comp.as_rotvec()

        # The final point on the manifold after composition
        g_comp_point = sphere.get_center() + normalize(v_comp_vec) * sphere.radius
        g_comp_dot = Dot3D(g_comp_point, color=PURPLE, radius=0.1)
        
        # The path for the second part of the composition
        path2 = ArcBetweenPoints(g1_point, g_comp_point, color=ORANGE)

        self.play(
            Create(path2), Create(g_comp_dot),
            Rotate(
                cube,
                angle=np.linalg.norm(v2_vec),
                axis=normalize(v2_vec),
                about_point=cube.get_center()
            ),
            run_time=2
        )
        
        # Return all created mobjects for easy cleanup
        return VGroup(
            v1_arrow, v2_arrow, v_sum_arrow, sum_path, g_sum_dot,
            path1, g1_dot, path2, g_comp_dot, cube_sum_final
        )