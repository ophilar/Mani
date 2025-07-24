# SLAM Manim Visualizations

Educational Manim animations for Simultaneous Localization and Mapping (SLAM) and robotics concepts. This project provides visual explanations of complex mathematical concepts in robotics, from basic rotations to advanced SLAM algorithms.

## 🎯 Overview

This collection of Manim scenes visualizes fundamental concepts in robotics and SLAM:

- **SO(3) Rotations**: Basic 3D rotations and the Special Orthogonal group
- **Lie Algebras**: so(3) manifold and exponential maps
- **SE(3) Transformations**: Rigid body motions and twists
- **BCH Formula**: Baker-Campbell-Hausdorff commutator terms
- **SLAM Concepts**: Pose Graph Optimization and Keyframe Management

## 🌐 Live Website

**Visit the live website**: [https://yourusername.github.io/slam-manim-visualizations](https://yourusername.github.io/slam-manim-visualizations)

The website features:
- **Interactive Gallery**: Watch all animations with embedded videos
- **Mathematical Concepts**: Learn about SO(3), SE(3), Lie algebras, and SLAM
- **Getting Started Guide**: Step-by-step instructions for running animations
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [uv](https://docs.astral.sh/uv/) (modern Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd slam-manim-visualizations
   ```

2. **Install dependencies with uv**:
   ```bash
   uv sync
   ```

3. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate     # On Windows
   ```

### Generate Website

To create the website with video previews:

```bash
# Generate preview videos and website
python scripts/generate_previews.py

# Or use the setup script (includes website generation)
python scripts/setup.py
```

### Running Animations

#### Basic Usage

```bash
# Render a specific scene
manim -pql so3_visualization.py SO3RotationVisualization

# Render with higher quality
manim -pqh so3_visualization.py SO3RotationVisualization

# Render and show immediately
manim -pql --preview so3_visualization.py SO3RotationVisualization
```

#### Available Scenes

| File | Scene Class | Description |
|------|-------------|-------------|
| `so3_visualization.py` | `SO3RotationVisualization` | Basic 3D rotation visualization |
| `so3_manifold_visualization.py` | `SO3ManifoldAndLieAlgebra` | SO(3) manifold and Lie algebra relationship |
| `so3_composition_vs_addition.py` | `SO3CompositionVsAddition` | Group composition vs algebra addition |
| `se3_visualization.py` | `SE3Visualization` | SE(3) rigid body motion (twist) |
| `se3_exponential_map.py` | `SE3ExponentialMap` | SE(3) exponential map from twist to transformation |
| `se3_relative_pose.py` | `SE3RelativePose` | Relative pose transformations between cameras |
| `bch_commutator_visualization.py` | `BCHCommutatorVisualization` | BCH formula commutator terms |
| `pose_graph_optimization_visualization.py` | `PoseGraphOptimization` | Pose Graph Optimization in SLAM |
| `slam_keyframes_visualization.py` | `SLAMKeyframesVisualization` | Keyframe-based SLAM complexity management |

#### Quality Options

- `-pql`: Preview quality (low) - fast rendering
- `-pqm`: Medium quality - balanced speed/quality
- `-pqh`: High quality - best visual output
- `-pqk`: 4K quality - highest resolution

## 📚 Mathematical Concepts

### SO(3) - Special Orthogonal Group
- **Purpose**: Represents 3D rotations
- **Properties**: Orthogonal matrices with determinant 1
- **Applications**: Camera orientation, robot joint rotations

### SE(3) - Special Euclidean Group
- **Purpose**: Represents rigid body motions (rotation + translation)
- **Properties**: 4×4 homogeneous transformation matrices
- **Applications**: Robot poses, camera poses in SLAM

### Lie Algebras
- **so(3)**: Tangent space of SO(3) at identity
- **se(3)**: Tangent space of SE(3) at identity
- **Applications**: Velocity representations, optimization

### SLAM Concepts
- **Pose Graph Optimization**: Global consistency through loop closures
- **Keyframes**: Computational complexity management
- **Drift Correction**: Handling accumulated sensor errors

## ⚙️ Configuration

The project uses a centralized configuration system in `config.py`:

```python
from config import ANIMATION, COLORS, MATH, SCENE

# Customize animation timing
ANIMATION.default_wait_time = 1.5

# Change color scheme
COLORS.rotation_color = "ORANGE"

# Adjust mathematical parameters
MATH.small_rotation_angle = 0.3
```

### Key Configuration Options

- **Animation Timing**: Control wait times and animation durations
- **Color Schemes**: Customize visual appearance
- **Mathematical Parameters**: Adjust vector magnitudes and angles
- **Performance Settings**: Choose resolution based on hardware

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
uv sync --extra dev

# Install pre-commit hooks (optional)
pre-commit install
```

### Website Development

The website is built with HTML, CSS, and JavaScript and hosted on GitHub Pages:

```bash
# Generate the website with video previews
python scripts/generate_previews.py

# Test the website locally (requires Python HTTP server)
cd docs
python -m http.server 8000
# Visit http://localhost:8000
```

#### Website Structure

```
docs/
├── index.html          # Main landing page
├── gallery.html        # Video gallery page
├── styles.css          # Main stylesheet
├── script.js           # Interactive JavaScript
├── _config.yml         # GitHub Pages configuration
├── previews/           # Generated video previews
└── animations.json     # Animation metadata
```

### Code Quality

```bash
# Format code
black .
isort .

# Lint code
pylint *.py

# Run tests
pytest
```

### Adding New Scenes

1. Create a new Python file following the naming convention
2. Inherit from appropriate Manim scene class
3. Use configuration from `config.py`
4. Add comprehensive docstrings
5. Update this README with scene description

## 🎬 Rendering Tips

### Performance Optimization

- Use `-pql` for development and testing
- Use `-pqh` for final presentations
- Adjust resolution in `config.py` for your hardware

### Common Issues

- **Memory**: Reduce resolution for complex scenes
- **Rendering Time**: Use lower quality for iterative development
- **Dependencies**: Ensure all packages are installed with `uv sync`

## 📖 Learning Resources

### Mathematical Background
- [A Mathematical Introduction to Robotic Manipulation](http://www.cds.caltech.edu/~murray/books/MLS/pdf/mls94-complete.pdf)
- [State Estimation for Robotics](http://asrl.utias.utoronto.ca/~tdb/bib/barfoot_ser17.pdf)

### Manim Documentation
- [Manim Community Documentation](https://docs.manim.community/)
- [Manim Tutorials](https://docs.manim.community/en/stable/tutorials/)

### SLAM Resources
- [Visual SLAM: From Theory to Practice](https://github.com/gaoxiang12/slambook)
- [ORB-SLAM3 Paper](https://arxiv.org/abs/2007.11898)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Ensure code quality checks pass
6. Submit a pull request

### Contribution Guidelines

- Follow existing code style and structure
- Add comprehensive docstrings
- Use configuration parameters from `config.py`
- Test animations with different quality settings
- Update documentation for new features

## 🌐 GitHub Pages Setup

To enable the website for your repository:

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Add website and video previews"
   git push origin main
   ```

2. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Click "Settings" → "Pages"
   - Set "Source" to "Deploy from a branch"
   - Select "main" branch and "/docs" folder
   - Click "Save"

3. **Your website will be available at**:
   `https://yourusername.github.io/slam-manim-visualizations`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Manim Community](https://github.com/ManimCommunity/manim) for the animation framework
- The robotics and SLAM research community for mathematical foundations
- Contributors and users who provide feedback and improvements

## 📞 Support

For questions, issues, or contributions:

1. Check existing [Issues](../../issues)
2. Create a new issue with detailed description
3. Include system information and error messages
4. Provide minimal reproduction examples

---

**Happy Learning! 🚀** 