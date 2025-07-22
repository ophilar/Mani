from manim import (
    ThreeDScene, Text, MathTex, VGroup, Sphere, Dot3D, Cube, ThreeDAxes, Square,
    Arrow3D, ArcBetweenPoints, FadeIn, FadeOut, Create, Write, GrowArrow, Rotate,
    ORIGIN, UP, DOWN, LEFT, RIGHT, PURPLE, BLUE, YELLOW, GREEN, RED, ORANGE,
    DEGREES, smooth, normalize
)

class SO3ManifoldAndLieAlgebra(ThreeDScene):
    """
    A Manim scene visualizing the relationship between the SO(3) manifold,
    represented by a sphere, and its Lie algebra so(3), represented by
    the tangent space at the identity element.
    """
    def construct(self):
        # --- Scene and Camera Setup ---
        self.set_camera_orientation(phi=65 * DEGREES, theta=-120 * DEGREES, zoom=0.9)
        
        # Add a title that remains fixed on the screen
        title = Text("SO(3) Manifold & its Lie Algebra so(3)").scale(0.8).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)

        # --- Group 1: The Manifold (Sphere) ---
        manifold_group = VGroup()
        manifold_sphere = Sphere(
            radius=2, 
            resolution=(32, 32) # Higher resolution for smoothness
        ).set_color(BLUE).set_opacity(0.2)
        
        manifold_label = Text("SO(3) Manifold\n(Space of Rotations)").scale(0.6).next_to(manifold_sphere, DOWN, buff=0.3)

        # Identity Element 'e' (no rotation)
        identity_point_location = manifold_sphere.get_top()
        identity_dot = Dot3D(identity_point_location, color=YELLOW, radius=0.08)
        identity_label = MathTex("e", color=YELLOW).next_to(identity_dot, UP, buff=0.2)
        
        manifold_group.add(manifold_sphere, manifold_label, identity_dot, identity_label)
        manifold_group.move_to(LEFT * 3.5)
        
        # --- Group 2: The Lie Algebra (Tangent Plane) ---
        # Position this group relative to the manifold group
        algebra_group = VGroup()
        tangent_plane = Square(
            side_length=3.5, 
            stroke_color=GREEN, 
            fill_color=GREEN, 
            fill_opacity=0.2
        ).set_shade_in_3d(True)
        
        algebra_label = Text("Lie Algebra so(3)\n(Tangent Space at 'e')").scale(0.5).next_to(tangent_plane, RIGHT, buff=0.3).shift(UP*0.5)
        algebra_group.add(tangent_plane, algebra_label)
        # Ensure it's perfectly tangent to the sphere
        algebra_group.move_to(manifold_group.get_center() + identity_point_location)

        # --- Group 3: The Concrete 3D Object ---
        object_group = VGroup()
        axes = ThreeDAxes(x_range=[-2,2], y_range=[-2,2], z_range=[-2,2], x_length=3, y_length=3, z_length=3)
        cube = Cube(side_length=1.2, fill_opacity=0.8, fill_color=PURPLE).set_shade_in_3d(True)
        object_label = Text("Object in ℝ³").scale(0.6).next_to(axes, DOWN, buff=0.2)
        object_group.add(axes, cube, object_label)
        object_group.move_to(RIGHT * 4)

        # --- Animation Sequence ---
        self.play(
            FadeIn(manifold_group, shift=DOWN),
            FadeIn(object_group, shift=DOWN),
            run_time=1.5
        )
        self.wait(0.5)

        self.play(
            Create(tangent_plane),
            Write(algebra_label),
            run_time=1.5
        )
        self.wait(1)

        # --- Visualize the Mapping from Algebra to Group ---
        
        # 1. Define a vector in the Lie Algebra (an "infinitesimal rotation")
        # The direction of this vector is the axis of rotation.
        # The length of this vector is the angle of rotation.
        algebra_vector_direction = normalize(RIGHT + UP * 0.5) # A direction on the plane
        algebra_vector_length = 1.8
        rotation_angle = algebra_vector_length # Angle is the vector's magnitude
        rotation_axis = algebra_vector_direction # Axis is the vector's direction

        algebra_vector = Arrow3D(
            start=tangent_plane.get_center(),
            end=tangent_plane.get_center() + algebra_vector_direction * algebra_vector_length,
            color=RED,
            resolution=12
        )
        algebra_vector_label = MathTex(r"\mathbf{v} \in \mathfrak{so}(3)", color=RED).scale(0.8).next_to(algebra_vector, DOWN, buff=0.2)

        self.play(
            GrowArrow(algebra_vector),
            Write(algebra_vector_label)
        )
        self.wait(1)

        # 2. Show the exponential map projecting the vector onto the manifold
        exp_map_label = MathTex(r"g = \exp(\mathbf{v})", color=ORANGE).scale(0.9).move_to(ORIGIN).to_edge(UP, buff=1.5)
        
        # The path from the algebra vector to the manifold point (a visual geodesic)
        exp_path = ArcBetweenPoints(
            algebra_vector.get_end(),
            # Project the point onto the sphere surface
            manifold_sphere.get_center() + normalize(algebra_vector.get_end() - manifold_sphere.get_center()) * manifold_sphere.radius,
            color=ORANGE,
            stroke_width=6
        )
        
        # The resulting group element 'g' on the manifold
        group_element_dot = Dot3D(exp_path.get_end(), color=ORANGE, radius=0.08)
        group_element_label = MathTex("g \in SO(3)", color=ORANGE).scale(0.8).next_to(group_element_dot, LEFT, buff=0.2)

        self.play(
            Write(exp_map_label)
        )
        self.wait(0.5)

        # Animate the mapping and the corresponding 3D rotation simultaneously
        self.play(
            Create(exp_path),
            Create(group_element_dot),
            Write(group_element_label),
            Rotate(
                cube,
                angle=rotation_angle,
                axis=rotation_axis,
                about_point=cube.get_center()
            ),
            run_time=4,
            rate_func=smooth
        )
        self.wait(1)

        # --- Cleanup for the next part ---
        self.play(
            FadeOut(algebra_vector),
            FadeOut(algebra_vector_label),
            FadeOut(exp_path),
            FadeOut(group_element_dot),
            FadeOut(group_element_label),
            FadeOut(exp_map_label),
            # Reset the cube to its original orientation
            Rotate(
                cube,
                angle=-rotation_angle,
                axis=rotation_axis,
                about_point=cube.get_center()
            ),
            run_time=1.5
        )
        self.wait(1)

        # --- Part 2: Illustrate the Linear Approximation with a small vector ---
        approximation_text = Text(
            "For small vectors, the Lie Algebra\n"
            "is a linear approximation of the manifold.",
            font_size=28,
            line_spacing=0.8
        ).to_corner(DR)
        self.add_fixed_in_frame_mobjects(approximation_text)
        self.play(Write(approximation_text))
        self.wait(1)

        # 1. Define a SMALL vector in the Lie Algebra
        algebra_vector_direction_small = normalize(LEFT + UP * 0.8)
        algebra_vector_length_small = 0.4 # Much smaller length
        rotation_angle_small = algebra_vector_length_small
        rotation_axis_small = algebra_vector_direction_small

        algebra_vector_small = Arrow3D(
            start=tangent_plane.get_center(),
            end=tangent_plane.get_center() + algebra_vector_direction_small * algebra_vector_length_small,
            color=RED,
            resolution=8
        )
        algebra_vector_label_small = MathTex(r"\mathbf{v}_{\text{small}}", color=RED).scale(0.7).next_to(algebra_vector_small, DOWN, buff=0.1)

        self.play(GrowArrow(algebra_vector_small), Write(algebra_vector_label_small))
        self.wait(1)

        # 2. Show the exponential map for the small vector, highlighting the approximation
        exp_map_label_approx = MathTex(r"g = \exp(\mathbf{v}) \approx e + \mathbf{v}", color=ORANGE).scale(0.9).move_to(ORIGIN).to_edge(UP, buff=1.5)

        exp_path_small = ArcBetweenPoints(
            algebra_vector_small.get_end(),
            manifold_sphere.get_center() + normalize(algebra_vector_small.get_end() - manifold_sphere.get_center()) * manifold_sphere.radius,
            color=ORANGE,
            stroke_width=6
        )
        group_element_dot_small = Dot3D(exp_path_small.get_end(), color=ORANGE, radius=0.08)

        self.play(Write(exp_map_label_approx))
        self.wait(0.5)

        # Animate the small mapping and the tiny corresponding rotation
        self.play(
            Create(exp_path_small),
            Create(group_element_dot_small),
            Rotate(
                cube,
                angle=rotation_angle_small,
                axis=rotation_axis_small,
                about_point=cube.get_center()
            ),
            run_time=3
        )
        self.wait(1)

        # Final camera move to appreciate the scene
        self.move_camera(phi=75 * DEGREES, theta=-60 * DEGREES, zoom=1.2, run_time=2)
        self.wait(3)