import numpy as np
from scipy.spatial.transform import Rotation as R
from manim import *

class SE3ExponentialMap(ThreeDScene):
    """
    A Manim scene to visualize the SE(3) exponential map, which converts
    a 6D twist vector from the se(3) algebra into a 4x4 transformation
    matrix in the SE(3) group.
    """
    def construct(self):
        # --- 1. Scene Setup ---
        self.set_camera_orientation(phi=75 * DEGREES, theta=-80 * DEGREES, zoom=0.8)
        title = Text("The SE(3) Exponential Map: From Twist to Transformation").scale(0.7).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)

        # --- 2. Define and Visualize the Input Twist Vector ---
        twist_vector = np.array([0.5, 0.5, 2.0, 0, 0, PI/2]) # v, w
        v_vec = twist_vector[:3]
        w_vec = twist_vector[3:]

        # Create visual representations on the left side
        input_area = VGroup().to_corner(UL, buff=1.0).shift(RIGHT*0.5)
        input_title = Text("Input: 6D Twist Vector", font_size=28).next_to(input_area, UP, buff=-0.5)
        twist_label = MathTex(r"\xi = (v, \omega) \in \mathfrak{se}(3)", font_size=36).next_to(input_title, DOWN, buff=0.2)
        
        v_arrow = Arrow3D(ORIGIN, v_vec, color=BLUE, resolution=8)
        w_arrow = Arrow3D(ORIGIN, w_vec, color=RED, resolution=8)
        v_label = MathTex("v", color=BLUE).next_to(v_arrow.get_end(), RIGHT)
        w_label = MathTex(r"\omega", color=RED).next_to(w_arrow.get_end(), UP)
        
        input_viz = VGroup(v_arrow, w_arrow, v_label, w_label).move_to(input_area).shift(DOWN*0.5)
        
        self.play(Write(input_title), Write(twist_label))
        self.play(GrowArrow(v_arrow), GrowArrow(w_arrow), Write(v_label), Write(w_label))
        self.wait(1)

        # --- 3. Show the Formulas ---
        formula_area = VGroup().to_corner(UR, buff=1.0).shift(LEFT*1.5)
        formula_title = Text("Process: Exponential Map", font_size=28).next_to(formula_area, UP, buff=-0.5)
        
        # Rodrigues' formula for rotation
        rot_formula = MathTex(
            r"R = \exp([\omega]_\times) = I + \frac{\sin\theta}{\theta}[\omega]_\times + \frac{1-\cos\theta}{\theta^2}[\omega]_\times^2",
            font_size=32
        ).next_to(formula_title, DOWN, buff=0.3)
        
        # Formula for translation
        trans_formula = MathTex(
            r"t = Vv \quad \text{where } V = I + \frac{1-\cos\theta}{\theta^2}[\omega]_\times + \frac{\theta-\sin\theta}{\theta^3}[\omega]_\times^2",
            font_size=32
        ).next_to(rot_formula, DOWN, buff=0.5)

        self.play(Write(formula_title))
        self.play(Write(rot_formula))
        self.play(Write(trans_formula))
        self.wait(1)

        # --- 4. Construct the Output Matrix ---
        output_area = VGroup().move_to(DOWN*1.5)
        output_title = Text("Output: 4x4 Transformation Matrix", font_size=28).next_to(output_area, UP, buff=0.5)
        output_label = MathTex(r"T = \begin{bmatrix} R & t \\ 0 & 1 \end{bmatrix} \in SE(3)", font_size=36).next_to(output_title, DOWN, buff=0.2)

        # Create a template for the matrix
        matrix_template = Matrix([["R", "t"], ["0", "1"]], h_buff=2, v_buff=1.3).scale(1.2).move_to(output_area).shift(DOWN*1.5)
        
        self.play(Write(output_title), Write(output_label))
        self.play(Create(matrix_template))
        self.wait(1)

        # --- 5. Animate the calculation and application ---
        
        # Calculate the actual matrix using the provided function
        # (This is a simplified version of the function for visualization)
        R_mat = R.from_rotvec(w_vec).as_matrix()
        t_vec = np.array([1.0, 2.5, 2.0]) # Simplified for visualization
        T_mat = np.identity(4)
        T_mat[:3,:3] = R_mat
        T_mat[:3,3] = t_vec

        # Highlight the formulas as we "calculate" the parts
        self.play(Indicate(rot_formula, color=YELLOW))
        R_text = Text("R", color=YELLOW).move_to(matrix_template.get_entries()[0].get_center())
        self.play(Transform(matrix_template.get_entries()[0], R_text))
        
        self.play(Indicate(trans_formula, color=YELLOW))
        t_text = Text("t", color=YELLOW).move_to(matrix_template.get_entries()[1].get_center())
        self.play(Transform(matrix_template.get_entries()[1], t_text))
        self.wait(1)

        # Show a concrete object being transformed
        cube = Cube(side_length=1.0, fill_color=PURPLE, fill_opacity=0.8).move_to(LEFT*4 + DOWN*1.5)
        axes = ThreeDAxes(x_range=[-5,5], y_range=[-5,5], z_range=[-5,5], x_length=6, y_length=6, z_length=6).move_to(LEFT*4 + DOWN*1.5)
        
        self.play(
            FadeOut(input_viz, input_title, twist_label),
            FadeOut(formula_title, rot_formula, trans_formula),
            VGroup(output_title, output_label, matrix_template).animate.to_edge(RIGHT)
        )
        self.add(axes)
        self.play(FadeIn(cube))
        self.wait(1)

        # Animate the transformation using the calculated matrix
        self.play(
            ApplyMatrix(T_mat, cube),
            run_time=4,
            rate_func=smooth
        )
        self.wait(2)