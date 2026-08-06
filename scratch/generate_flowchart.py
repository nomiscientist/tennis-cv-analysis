import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set up canvas figure with dark background
fig, ax = plt.subplots(figsize=(12, 16), dpi=300)
fig.patch.set_facecolor('#0b0f19')
ax.set_facecolor('#0b0f19')
ax.set_xlim(0, 100)
ax.set_ylim(0, 135)
ax.axis('off')

# Style definitions
font_title = {'family': 'sans-serif', 'weight': 'bold', 'size': 18, 'color': '#00f2fe'}
font_subtitle = {'family': 'sans-serif', 'weight': 'normal', 'size': 10, 'color': '#94a3b8'}
font_box_title = {'family': 'sans-serif', 'weight': 'bold', 'size': 9, 'color': '#ffffff'}
font_box_sub = {'family': 'sans-serif', 'weight': 'normal', 'size': 7.5, 'color': '#e2e8f0'}
font_section = {'family': 'sans-serif', 'weight': 'bold', 'size': 8.5, 'color': '#cbd5e1'}

# Header Title
ax.text(50, 131, "TENNIS CV — AI MATCH COMPUTER VISION & ANALYTICS HUB", **font_title, ha='center')
ax.text(50, 128.5, "End-to-End User Workflow & Distributed Spatial-Temporal Pipeline Architecture", **font_subtitle, ha='center')

def draw_box(x, y, w, h, bg, border, title, subtitle="", rx=2):
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                 boxstyle="round,pad=0.3",
                                 linewidth=1.5, edgecolor=border, facecolor=bg, zorder=3)
    ax.add_patch(rect)
    if subtitle:
        ax.text(x, y + h*0.18, title, **font_box_title, ha='center', va='center', zorder=4)
        ax.text(x, y - h*0.22, subtitle, **font_box_sub, ha='center', va='center', zorder=4)
    else:
        ax.text(x, y, title, **font_box_title, ha='center', va='center', zorder=4)

def draw_diamond(x, y, w, h, bg, border, title):
    poly = patches.Polygon([[x, y+h/2], [x+w/2, y], [x, y-h/2], [x-w/2, y]],
                           linewidth=1.5, edgecolor=border, facecolor=bg, zorder=3)
    ax.add_patch(poly)
    ax.text(x, y, title, **font_box_title, ha='center', va='center', zorder=4)

def draw_arrow(x1, y1, x2, y2, color='#64748b', style='->', lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw, mutation_scale=12), zorder=2)

# Containers / Subgraphs
# Computer Vision Pipeline Box (Left)
cv_bg = patches.FancyBboxPatch((4, 48), 43, 63, boxstyle="round,pad=0.5",
                               linewidth=1.0, edgecolor='#1e293b', facecolor='#0f172a', alpha=0.7, zorder=1)
ax.add_patch(cv_bg)
ax.text(7, 108, "COMPUTER VISION & DETECTION PIPELINE", **font_section, ha='left')

# Analytics Pipeline Box (Right)
an_bg = patches.FancyBboxPatch((53, 48), 43, 63, boxstyle="round,pad=0.5",
                               linewidth=1.0, edgecolor='#1e293b', facecolor='#0f172a', alpha=0.7, zorder=1)
ax.add_patch(an_bg)
ax.text(56, 108, "SPATIAL & METRIC ANALYTICS PIPELINE", **font_section, ha='left')

# 1. Top Section Nodes
draw_box(50, 123, 16, 4, '#2563eb', '#60a5fa', "START", rx=2)
draw_box(50, 116, 32, 5, '#1e293b', '#475569', "User Uploads Broadcast Video (.mp4)", "Input Video Stream @ 1280x720 Native HD")
draw_box(50, 109, 36, 4.5, '#7c3aed', '#a78bfa', "Python Execution & Inference Engine", "Main Pipeline Orchestrator & Frame Decoder")

draw_arrow(50, 121, 50, 118.5)
draw_arrow(50, 113.5, 50, 111.25)

# Split from Execution Engine to Both Sub-Pipelines
draw_arrow(50, 106.75, 25.5, 103.5)
draw_arrow(50, 106.75, 74.5, 103.5)

# 2. Computer Vision Pipeline (Left Column)
draw_box(25.5, 101, 34, 4.5, '#ea580c', '#fb923c', "Frame Extractor", "OpenCV Frame Reader @ 24 FPS")
draw_box(25.5, 93, 34, 4.5, '#ea580c', '#fb923c', "Court Keypoint Regressor", "ResNet-50 Landmark Model → 14 (x,y) Points")
draw_box(25.5, 85, 34, 4.5, '#ea580c', '#fb923c', "Player BBox & Net-y Partition", "YOLOv8x Person Detector → P1 & P2 Assign")
draw_box(25.5, 77, 34, 4.5, '#ea580c', '#fb923c', "Ball Candidate Detector", "Fine-Tuned YOLOv5 → conf=0.08 Recovery")
draw_box(25.5, 69, 34, 4.5, '#ea580c', '#fb923c', "Trajectory Smoothing Engine", "5-Frame Centered Rolling Window Average")
draw_box(25.5, 61, 34, 4.5, '#ea580c', '#fb923c', "Non-Rally Cutaway Classifier", "Rule-based Close-Up Reaction Overlay Suppressor")

draw_arrow(25.5, 98.75, 25.5, 95.25)
draw_arrow(25.5, 90.75, 25.5, 87.25)
draw_arrow(25.5, 82.75, 25.5, 79.25)
draw_arrow(25.5, 74.75, 25.5, 71.25)
draw_arrow(25.5, 66.75, 25.5, 63.25)

# 3. Spatial & Metric Analytics Pipeline (Right Column)
draw_box(74.5, 99, 34, 4.5, '#059669', '#34d399', "Homography Metric Transformer", "2D DLT Matrix H → 10.97m x 23.77m Court")
draw_box(74.5, 89, 34, 4.5, '#059669', '#34d399', "Euclidean Speed & Distance Engine", "Instantaneous km/h, m/s & Total Meters")
draw_box(74.5, 79, 34, 4.5, '#0d9488', '#2dd4bf', "Player Spacing & Net Position", "Calculates Spacing (m) & Time at Net %")
draw_box(74.5, 69, 34, 4.5, '#0d9488', '#2dd4bf', "Work Rate & Coverage Area", "High-Intensity Rally % & Coverage m²")

draw_arrow(74.5, 96.75, 74.5, 91.25)
draw_arrow(74.5, 86.75, 74.5, 81.25)
draw_arrow(74.5, 76.75, 74.5, 71.25)

# Connect Left & Right to Compile Data Node
draw_arrow(25.5, 58.75, 50, 48.25)
draw_arrow(74.5, 66.75, 50, 48.25)

# 4. Central Compile & Exporter Node
draw_box(50, 46, 38, 4.5, '#7c3aed', '#c084fc', "Compile Analytics Dataset (data.json)", "Generates Frame-by-Frame Payload & Summary Stats")
draw_arrow(50, 43.75, 50, 40.25)

# 5. Dashboard Layer
draw_box(50, 38, 42, 4.5, '#0284c7', '#38bdf8', "Glassmorphic Web Dashboard Engine", "Vanilla CSS / JS HTML5 Canvas Web Application")
draw_arrow(50, 35.75, 27, 31.25)
draw_arrow(50, 35.75, 73, 31.25)

# Dashboard Components
draw_box(27, 29, 36, 4.5, '#0369a1', '#7dd3fc', "Dynamic 3D Canvas Video Player", "Renders 3D Court, Keypoints, BBoxes & Ball Arc")
draw_box(73, 29, 36, 4.5, '#0369a1', '#7dd3fc', "2D Top-Down Court & Coverage Heatmap", "Interactive Layout-Matched Court & Spacing")

draw_arrow(27, 26.75, 50, 22.5)
draw_arrow(73, 26.75, 50, 22.5)

# 6. User Interaction Node
draw_diamond(50, 20, 22, 6, '#d97706', '#fbbf24', "User Interaction?")

# Action Nodes
draw_box(16, 9, 25, 4.5, '#dc2626', '#f87171', "Multi-Track Timeline Scrubber", "Scrub frames across rally tracks")
draw_box(38.5, 9, 18, 4.5, '#dc2626', '#f87171', "Toggle 3D Overlays", "Boxes / Heatmap / Ball")
draw_box(61.5, 9, 22, 4.5, '#dc2626', '#f87171', "Filter Shot Types", "Serve / Drive / Lob / Volley")
draw_box(84, 9, 14, 4.5, '#2563eb', '#60a5fa', "END")

draw_arrow(43, 18, 16, 11.25, style='->')
draw_arrow(46.5, 17, 38.5, 11.25, style='->')
draw_arrow(53.5, 17, 61.5, 11.25, style='->')
draw_arrow(57, 18, 84, 11.25, style='->')

plt.tight_layout()
plt.savefig('output/system_architecture_flowchart.png', facecolor=fig.get_facecolor(), edgecolor='none', dpi=300)
print("Successfully generated output/system_architecture_flowchart.png!")
