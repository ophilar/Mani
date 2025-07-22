from manim import *

class BCHCommutatorVisualization(ThreeDScene):
    """
    A Manim scene to visualize the Lie bracket (commutator) term
    from the Baker-Campbell-Hausdorff (BCH) formula for so(3),
    which corresponds to the cross product.
    """
    def construct(self):
        # --- 1. Scene Setup ---
        self.set_camera_orientation(phi=60 * DEGREES, theta=-70 * DEGREES, zoom=1)
        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
            x_length=6, y_length=6, z_length=6
        )
        
        title = Text("BCH Formula's Commutator Term for so(3)").scale(0.8).to_edge(UP)
        subtitle = MathTex(r"[v_1, v_2] \equiv v_1 \times v_2", font_size=48).next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(title, subtitle)

        # We visualize the algebra as the tangent space at the origin
        plane = Square(
            side_length=6,
            stroke_color=GREEN,
            fill_color=GREEN,
            fill_opacity=0.15
        ).set_shade_in_3d(True).rotate(90*DEGREES, axis=RIGHT) # Make it the XY plane

        self.add(axes, plane)
        self.wait()

        # --- 2. Define and Draw Vectors in the Algebra ---
        v1 = np.array([2.5, 0, 0]) # A rotation vector along the world x-axis
        v2 = np.array([0, 2, 0])   # A rotation vector along the world y-axis

        v1_arrow = Arrow3D(start=ORIGIN, end=v1, color=RED, resolution=8)
        v2_arrow = Arrow3D(start=ORIGIN, end=v2, color=ORANGE, resolution=8)
        v1_label = MathTex(r"\mathbf{v}_1", color=RED).next_to(v1_arrow, RIGHT)
        v2_label = MathTex(r"\mathbf{v}_2", color=ORANGE).next_to(v2_arrow, UP)

        self.play(
            GrowArrow(v1_arrow),
            Write(v1_label),
            run_time=1.5
        )
        self.play(
            GrowArrow(v2_arrow),
            Write(v2_label),
            run_time=1.5
        )
        self.wait(1)

        # --- 3. Visualize the Commutator (Cross Product) ---
        # For so(3), the Lie bracket is the cross product
        v_commutator = np.cross(v1, v2)

        commutator_arrow = Arrow3D(
            start=ORIGIN,
            end=v_commutator,
            color=PURPLE,
            thickness=0.03,
            resolution=8
        )
        commutator_label = MathTex(r"[ \mathbf{v}_1, \mathbf{v}_2 ]", color=PURPLE).next_to(commutator_arrow, OUT)

        # Show the parallelogram to give intuition for the cross product
        parallelogram = Polygon(
            ORIGIN, v1, v1 + v2, v2,
            stroke_color=WHITE,
            stroke_opacity=0.7,
            fill_color=BLUE,
            fill_opacity=0.5
        ).set_shade_in_3d(True)

        bch_formula_text = MathTex(
            r"\log(e^{\mathbf{v}_1} e^{\mathbf{v}_2}) = \mathbf{v}_1 + \mathbf{v}_2 + \frac{1}{2}[\mathbf{v}_1, \mathbf{v}_2] + \dots",
            font_size=36
        ).to_corner(DL)
        self.add_fixed_in_frame_mobjects(bch_formula_text)

        self.play(
            Write(bch_formula_text),
            Create(parallelogram),
            run_time=2
        )
        self.wait(1)

        self.play(
            GrowArrow(commutator_arrow),
            Write(commutator_label),
            run_time=2
        )
        self.wait(1)

        # --- 4. Final Touches ---
        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, zoom=1.2, run_time=3)
        self.wait(3)