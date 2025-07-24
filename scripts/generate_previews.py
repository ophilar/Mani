#!/usr/bin/env python3
"""
Script to generate video previews from Manim animations for the website.

This script renders low-quality preview videos of all animations and
creates a gallery page with embedded videos.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple


class AnimationPreviewGenerator:
    """Generates preview videos and gallery for the website."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.media_dir = self.project_root / "media"
        self.docs_dir = self.project_root / "docs"
        self.preview_dir = self.docs_dir / "previews"
        
        # Animation metadata
        self.animations = {
            "so3_visualization.py": {
                "class": "SO3RotationVisualization",
                "title": "SO(3) Rotation Visualization",
                "description": "Basic 3D rotation demonstrating elements of the Special Orthogonal group.",
                "duration": "10s",
                "complexity": "Beginner",
                "icon": "fas fa-cube"
            },
            "so3_manifold_visualization.py": {
                "class": "SO3ManifoldAndLieAlgebra",
                "title": "SO(3) Manifold & Lie Algebra",
                "description": "Visualization of the relationship between SO(3) manifold and its Lie algebra so(3).",
                "duration": "15s",
                "complexity": "Intermediate",
                "icon": "fas fa-globe"
            },
            "so3_composition_vs_addition.py": {
                "class": "SO3CompositionVsAddition",
                "title": "Group Composition vs Algebra Addition",
                "description": "Comparison of group composition in SO(3) with vector addition in so(3).",
                "duration": "20s",
                "complexity": "Advanced",
                "icon": "fas fa-plus"
            },
            "se3_visualization.py": {
                "class": "SE3Visualization",
                "title": "SE(3) Rigid Body Motion",
                "description": "Demonstration of rigid body motion combining rotation and translation.",
                "duration": "12s",
                "complexity": "Intermediate",
                "icon": "fas fa-camera"
            },
            "se3_exponential_map.py": {
                "class": "SE3ExponentialMap",
                "title": "SE(3) Exponential Map",
                "description": "Conversion from twist vectors to transformation matrices via exponential mapping.",
                "duration": "18s",
                "complexity": "Advanced",
                "icon": "fas fa-expand-arrows-alt"
            },
            "se3_relative_pose.py": {
                "class": "SE3RelativePose",
                "title": "SE(3) Relative Pose",
                "description": "Relative pose transformations between camera positions.",
                "duration": "15s",
                "complexity": "Intermediate",
                "icon": "fas fa-exchange-alt"
            },
            "bch_commutator_visualization.py": {
                "class": "BCHCommutatorVisualization",
                "title": "BCH Formula Commutator",
                "description": "Visualization of the Baker-Campbell-Hausdorff formula commutator terms.",
                "duration": "12s",
                "complexity": "Advanced",
                "icon": "fas fa-brackets-curly"
            },
            "pose_graph_optimization_visualization.py": {
                "class": "PoseGraphOptimization",
                "title": "Pose Graph Optimization",
                "description": "Visualization of drift accumulation and correction through loop closures.",
                "duration": "25s",
                "complexity": "Advanced",
                "icon": "fas fa-sitemap"
            },
            "slam_keyframes_visualization.py": {
                "class": "SLAMKeyframesVisualization",
                "title": "SLAM Keyframes Management",
                "description": "Managing computational complexity with keyframe-based SLAM.",
                "duration": "20s",
                "complexity": "Intermediate",
                "icon": "fas fa-key"
            }
        }
    
    def generate_previews(self) -> bool:
        """Generate preview videos for all animations."""
        print("🎬 Generating preview videos...")
        
        # Create preview directory
        self.preview_dir.mkdir(exist_ok=True)
        
        success_count = 0
        total_count = len(self.animations)
        
        for filename, metadata in self.animations.items():
            print(f"Rendering {filename}...")
            
            try:
                # Render low-quality preview
                result = subprocess.run([
                    "uv", "run", "manim", 
                    "-pql",  # Preview quality, low
                    "--format", "mp4",
                    "--output_file", metadata["class"],
                    filename,
                    metadata["class"]
                ], cwd=self.project_root, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    # Move video to previews directory
                    source_video = self.media_dir / "videos" / f"{metadata['class']}.mp4"
                    if source_video.exists():
                        target_video = self.preview_dir / f"{metadata['class']}.mp4"
                        source_video.rename(target_video)
                        success_count += 1
                        print(f"✅ {filename} rendered successfully")
                    else:
                        print(f"⚠️  Video file not found for {filename}")
                else:
                    print(f"❌ Failed to render {filename}: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print(f"⏰ Timeout rendering {filename}")
            except Exception as e:
                print(f"❌ Error rendering {filename}: {e}")
        
        print(f"\n🎉 Generated {success_count}/{total_count} preview videos")
        return success_count > 0
    
    def create_gallery_page(self) -> None:
        """Create a gallery page with embedded videos."""
        print("📄 Creating gallery page...")
        
        gallery_html = self._generate_gallery_html()
        gallery_file = self.docs_dir / "gallery.html"
        
        with open(gallery_file, 'w') as f:
            f.write(gallery_html)
        
        print(f"✅ Gallery page created: {gallery_file}")
    
    def _generate_gallery_html(self) -> str:
        """Generate HTML for the gallery page."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SLAM Animations Gallery</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .gallery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }}
        .video-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .video-container {{
            position: relative;
            width: 100%;
            height: 0;
            padding-bottom: 56.25%; /* 16:9 aspect ratio */
        }}
        .video-container video {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 8px;
        }}
        .video-info {{
            padding: 1.5rem;
        }}
        .video-info h3 {{
            color: #fff;
            margin-bottom: 0.5rem;
        }}
        .video-info p {{
            color: #ccc;
            margin-bottom: 1rem;
        }}
        .video-meta {{
            display: flex;
            gap: 1rem;
            font-size: 0.875rem;
        }}
        .video-meta span {{
            color: #888;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: #00d4ff;
            text-decoration: none;
            margin-bottom: 2rem;
            font-weight: 500;
        }}
        .back-link:hover {{
            color: #0099cc;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">
            <i class="fas fa-arrow-left"></i>
            Back to Home
        </a>
        
        <h1 class="section-title">Animation Gallery</h1>
        <p style="text-align: center; color: #ccc; margin-bottom: 3rem;">
            Watch all the SLAM and robotics visualizations in high quality
        </p>
        
        <div class="gallery-grid">
{self._generate_video_cards()}
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""
    
    def _generate_video_cards(self) -> str:
        """Generate HTML for video cards."""
        cards = []
        
        for filename, metadata in self.animations.items():
            video_path = f"previews/{metadata['class']}.mp4"
            video_exists = (self.preview_dir / f"{metadata['class']}.mp4").exists()
            
            if video_exists:
                video_html = f"""
            <video controls>
                <source src="{video_path}" type="video/mp4">
                Your browser does not support the video tag.
            </video>"""
            else:
                video_html = f"""
            <div style="display: flex; align-items: center; justify-content: center; height: 100%; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #00d4ff;">
                <div style="text-align: center;">
                    <i class="{metadata['icon']}" style="font-size: 3rem; margin-bottom: 1rem; display: block;"></i>
                    <span style="color: #fff; font-weight: 600;">Preview not available</span>
                </div>
            </div>"""
            
            card = f"""            <div class="video-card">
                <div class="video-container">
{video_html}
                </div>
                <div class="video-info">
                    <h3>{metadata['title']}</h3>
                    <p>{metadata['description']}</p>
                    <div class="video-meta">
                        <span><i class="fas fa-clock"></i> {metadata['duration']}</span>
                        <span><i class="fas fa-star"></i> {metadata['complexity']}</span>
                    </div>
                </div>
            </div>"""
            
            cards.append(card)
        
        return '\n'.join(cards)
    
    def update_main_page(self) -> None:
        """Update the main page to link to the gallery."""
        print("📝 Updating main page...")
        
        main_page = self.docs_dir / "index.html"
        if main_page.exists():
            with open(main_page, 'r') as f:
                content = f.read()
            
            # Add gallery link to navigation
            content = content.replace(
                '<li><a href="#getting-started">Get Started</a></li>',
                '<li><a href="#getting-started">Get Started</a></li>\n                <li><a href="gallery.html">Gallery</a></li>'
            )
            
            # Add gallery button to hero section
            content = content.replace(
                '<a href="#animations" class="btn btn-secondary">\n                        <i class="fas fa-eye"></i> View Animations\n                    </a>',
                '<a href="#animations" class="btn btn-secondary">\n                        <i class="fas fa-eye"></i> View Animations\n                    </a>\n                    <a href="gallery.html" class="btn btn-secondary">\n                        <i class="fas fa-play-circle"></i> Watch Videos\n                    </a>'
            )
            
            with open(main_page, 'w') as f:
                f.write(content)
            
            print("✅ Main page updated")
    
    def create_metadata_file(self) -> None:
        """Create a JSON metadata file for the animations."""
        metadata_file = self.docs_dir / "animations.json"
        
        # Add file existence status
        for filename, metadata in self.animations.items():
            video_path = self.preview_dir / f"{metadata['class']}.mp4"
            metadata['has_preview'] = video_path.exists()
            metadata['filename'] = filename
        
        with open(metadata_file, 'w') as f:
            json.dump(self.animations, f, indent=2)
        
        print(f"✅ Metadata file created: {metadata_file}")


def main():
    """Main function to generate all previews and update the website."""
    generator = AnimationPreviewGenerator()
    
    print("🚀 SLAM Animation Preview Generator")
    print("=" * 40)
    
    # Generate preview videos
    if generator.generate_previews():
        # Create gallery page
        generator.create_gallery_page()
        
        # Update main page
        generator.update_main_page()
        
        # Create metadata file
        generator.create_metadata_file()
        
        print("\n🎉 Website generation completed!")
        print("\nNext steps:")
        print("1. Commit the generated files to your repository")
        print("2. Enable GitHub Pages in your repository settings")
        print("3. Set the source to the 'docs' folder")
        print("4. Your website will be available at: https://yourusername.github.io/slam-manim-visualizations")
    else:
        print("\n❌ Failed to generate previews. Check your Manim installation.")
        sys.exit(1)


if __name__ == "__main__":
    main() 