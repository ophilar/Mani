import numpy as np
from manim import *

class SLAMKeyframesVisualization(Scene):
    """
    A Manim scene to visualize why Keyframes are essential for managing
    computational complexity in real-time SLAM systems.
    """
    def construct(self):
        # --- General Scene Setup ---
        title = Text("Managing SLAM Complexity with Keyframes").scale(0.8).to_edge(UP)
        self.play(Write(title))

        # Define a path for the camera to follow
        camera_path = Ellipse(width=8, height=4, color=GRAY).shift(DOWN * 0.5)

        # --- Act 1: The Naive "All-Frames" Approach ---
        subtitle_naive = Text("Naive Approach: Every Frame is a Pose", font_size=32).to_corner(UL)
        self.play(Write(subtitle_naive))

        # Setup for the naive run
        graph_naive = VGroup()
        cost_meter_naive = self.create_cost_meter("Computation Cost", RED)
        self.play(FadeIn(cost_meter_naive, shift=DOWN))

        # Run the animation showing every frame being added
        self.run_path_animation(
            camera_path,
            graph_naive,
            cost_meter_naive.get_submobjects()[1], # The number mobject
            is_keyframe_based=False
        )
        
        cost_text_naive = Text("Too Expensive!", color=RED, font_size=36).next_to(cost_meter_naive, DOWN)
        self.play(Write(cost_text_naive))
        self.wait(2)

        # --- Cleanup for Act 2 ---
        self.play(
            FadeOut(subtitle_naive),
            FadeOut(graph_naive),
            FadeOut(cost_meter_naive),
            FadeOut(cost_text_naive)
        )

        # --- Act 2: The Smart "Keyframe" Approach ---
        subtitle_kf = Text("Smart Approach: Use Keyframes", font_size=32).to_corner(UL)
        self.play(Write(subtitle_kf))

        # Setup for the keyframe run
        graph_kf = VGroup()
        cost_meter_kf = self.create_cost_meter("Computation Cost", GREEN)
        self.play(FadeIn(cost_meter_kf, shift=DOWN))

        # Run the animation showing only keyframes being added
        self.run_path_animation(
            camera_path,
            graph_kf,
            cost_meter_kf.get_submobjects()[1], # The number mobject
            is_keyframe_based=True
        )

        cost_text_kf = Text("Manageable!", color=GREEN, font_size=36).next_to(cost_meter_kf, DOWN)
        self.play(Write(cost_text_kf))
        self.wait(3)

    def create_cost_meter(self, label_text, color):
        """Creates a label and a number to act as a cost meter."""
        label = Text(label_text, font_size=28)
        number = DecimalNumber(0, num_decimal_places=0, font_size=48).next_to(label, DOWN)
        meter = VGroup(label, number).to_corner(UR)
        number.set_color(color)
        return meter

    def run_path_animation(self, path, graph, cost_number, is_keyframe_based):
        """
        Animates a camera moving along a path and building a graph.
        
        Args:
            path: The VMobject path for the camera to follow.
            graph: The VGroup to add nodes and edges to.
            cost_number: The DecimalNumber mobject to update.
            is_keyframe_based: Boolean to control the logic.
        """
        camera = self.create_camera_icon().move_to(path.get_start())
        self.add(camera)

        # Parameters
        num_steps = 100
        keyframe_threshold = 20 if is_keyframe_based else 1
        cost_per_node = 5 if is_keyframe_based else 1

        last_kf_dot = Dot(path.get_start(), color=YELLOW, radius=0.1)
        graph.add(last_kf_dot)
        self.add(graph)
        cost_number.set_value(cost_per_node)

        for i in range(1, num_steps + 1):
            # Animate camera moving
            target_point = path.point_from_proportion(i / num_steps)
            self.play(camera.animate.move_to(target_point), run_time=0.05, rate_func=linear)

            # Check if we should add a new node/keyframe
            dist_from_last_kf = np.linalg.norm(camera.get_center() - last_kf_dot.get_center())
            
            # In a real system, this condition is more complex (feature count, etc.)
            # Here, we simplify it to a distance check.
            should_add_keyframe = (i % keyframe_threshold == 0)

            if is_keyframe_based:
                if should_add_keyframe:
                    # Create a new keyframe
                    new_dot = Dot(camera.get_center(), color=YELLOW, radius=0.1)
                    edge = Line(last_kf_dot.get_center(), new_dot.get_center(), color=WHITE, stroke_width=2)
                    
                    self.play(
                        Create(edge),
                        Create(new_dot),
                        cost_number.animate.increment(cost_per_node),
                        run_time=0.1
                    )
                    graph.add(edge, new_dot)
                    last_kf_dot = new_dot
                else:
                    # Show that the frame is processed but discarded
                    self.play(Flash(camera, color=GRAY, flash_radius=0.4, run_time=0.1))
            else: # Naive approach
                # Add a node for every single frame
                new_dot = Dot(camera.get_center(), color=BLUE, radius=0.05)
                edge = Line(last_kf_dot.get_center(), new_dot.get_center(), color=BLUE, stroke_width=1)
                
                self.add(edge, new_dot)
                graph.add(edge, new_dot)
                last_kf_dot = new_dot
                cost_number.increment(cost_per_node)

    def create_camera_icon(self):
        """Creates a simple icon for the camera."""
        body = Square(side_length=0.4, color=WHITE, fill_opacity=1).set_z_index(10)
        lens = Circle(radius=0.1, color=BLACK, fill_opacity=1).set_z_index(11)
        view_cone = Polygon(
            body.get_vertices()[0],
            body.get_vertices()[1],
            body.get_center() + DOWN*0.5 + RIGHT*0.5,
            body.get_center() + DOWN*0.5 + LEFT*0.5,
            color=YELLOW, fill_opacity=0.3, stroke_width=0
        ).set_z_index(9)
        return VGroup(body, lens, view_cone).rotate(-90*DEGREES)