import numpy as np
from manim import *

class PoseGraphOptimization(Scene):
    """
    A Manim scene to visualize the core concepts of Pose Graph Optimization in SLAM.
    1. Shows how visual odometry accumulates drift.
    2. Shows the creation of a loop closure constraint.
    3. Visualizes the optimization process that corrects the graph.
    """
    def construct(self):
        # --- Act 1: Visual Odometry and Drift ---
        title = Text("Pose Graph Optimization").scale(0.9).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Store created mobjects in the scene context for later access
        self.nodes_true = []
        self.graph_dots = VGroup()
        self.graph_edges = VGroup()

        self.show_drift_animation()
        self.wait(1)

        # --- Act 2: Loop Closure ---
        self.show_loop_closure_animation()
        self.wait(1)

        # --- Act 3: Optimization ---
        self.show_optimization_animation()
        self.wait(3)

    def show_drift_animation(self):
        """Animates the creation of a drifted path from odometry."""
        subtitle = Text("1. Visual Odometry Accumulates Drift", font_size=32).to_corner(UL)
        self.play(Write(subtitle))

        # Define the ground truth path
        true_path = Arc(radius=3, start_angle=PI, angle=1.25 * PI, color=GREEN_B)
        true_path_label = Text("True Path", color=GREEN_B, font_size=24).next_to(true_path, DOWN, buff=0.5)
        self.play(Create(true_path), Write(true_path_label))

        # Generate drifted path by adding accumulating noise
        self.nodes_true = [true_path.point_from_proportion(p) for p in np.linspace(0, 1, 11)]
        nodes_drifted_coords = [self.nodes_true[0]]
        
        noise_level = 0.0
        for i in range(1, len(self.nodes_true)):
            noise_level += 0.08
            # Keep noise in the XY plane for this 2D visualization
            noise = np.array([np.random.normal(0, noise_level), np.random.normal(0, noise_level), 0])
            nodes_drifted_coords.append(self.nodes_true[i] + noise)

        # Create the graph mobjects (nodes and edges)
        self.graph_dots.add(*[Dot(p, color=BLUE) for p in nodes_drifted_coords])
        for i in range(len(self.graph_dots) - 1):
            edge = Line(self.graph_dots[i].get_center(), self.graph_dots[i+1].get_center(), stroke_color=BLUE, stroke_width=3)
            self.graph_edges.add(edge)

        # Animate the path being created frame by frame
        estimated_path_label = Text("Estimated Path (from Odometry)", color=BLUE, font_size=24).next_to(true_path, UP, buff=1.5)
        self.play(Write(estimated_path_label))
        
        self.play(Create(self.graph_dots[0]))
        for i in range(len(self.graph_dots) - 1):
            self.play(
                Create(self.graph_edges[i]),
                Create(self.graph_dots[i+1]),
                run_time=0.25
            )
        
        # Store for later cleanup
        self.subtitle = subtitle
        self.true_path_group = VGroup(true_path, true_path_label)
        self.estimated_path_label = estimated_path_label

    def show_loop_closure_animation(self):
        """Animates the detection of a loop closure."""
        self.play(FadeOut(self.subtitle))
        subtitle = Text("2. A Loop Closure is Detected", font_size=32).to_corner(UL)
        self.play(Write(subtitle))
        self.subtitle = subtitle

        # Highlight the first and last nodes that form the loop
        first_node, last_node = self.graph_dots[0], self.graph_dots[-1]
        self.play(Flash(first_node, color=YELLOW, flash_radius=0.5), Flash(last_node, color=YELLOW, flash_radius=0.5))

        # Create the loop closure edge (a new, powerful constraint)
        loop_closure_edge = DashedLine(last_node.get_center(), first_node.get_center(), color=RED, stroke_width=5)
        loop_label = Text("Loop Constraint", color=RED, font_size=24).next_to(loop_closure_edge, UP, buff=0.2)
        self.play(Create(loop_closure_edge), Write(loop_label))

        self.loop_closure_group = VGroup(loop_closure_edge, loop_label)

    def show_optimization_animation(self):
        """Animates the graph relaxation process."""
        self.play(FadeOut(self.subtitle))
        subtitle = Text("3. Pose Graph Optimization", font_size=32).to_corner(UL)
        self.play(Write(subtitle))

        # Display the objective function that the optimizer minimizes
        objective_function = MathTex(r"\min_{\mathbf{X}} \sum_{(i,j)} \mathbf{e}_{ij}^T \mathbf{\Omega}_{ij} \mathbf{e}_{ij}", font_size=42).to_corner(DR)
        self.play(Write(objective_function))
        self.wait(1)

        # Create the target graph (where the nodes should be)
        target_dots = VGroup(*[Dot(p, color=GREEN_B) for p in self.nodes_true])
        
        # Use updaters to make the edges follow the dots during the animation
        self.graph_edges.add_updater(
            lambda m: m.become(VGroup(*[
                Line(self.graph_dots[i].get_center(), self.graph_dots[i+1].get_center(), stroke_color=BLUE, stroke_width=3)
                for i in range(len(self.graph_dots) - 1)
            ]))
        )
        self.loop_closure_group[0].add_updater(
            lambda m: m.become(DashedLine(self.graph_dots[-1].get_center(), self.graph_dots[0].get_center(), color=RED, stroke_width=5))
        )

        # The main optimization animation: transform the drifted dots to the correct positions
        self.play(Transform(self.graph_dots, target_dots), run_time=3, rate_func=smooth)
        
        # Updaters are no longer needed after the animation
        self.graph_edges.clear_updaters()
        self.loop_closure_group[0].clear_updaters()
        self.wait(1)

        # Conclude with a success message
        final_text = Text("Graph is now globally consistent", color=GREEN_B, font_size=32).next_to(objective_function, UP, buff=0.5)
        self.play(Write(final_text))