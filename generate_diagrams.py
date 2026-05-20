#!/usr/bin/env python3
"""
High-Quality UML Diagram Generator
Creates professional UML diagrams using matplotlib and custom shapes
Generates high-resolution PNG images (minimum 1920x1080)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Rectangle, FancyArrow
from matplotlib.patches import Circle, Ellipse, Wedge
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io

# Professional color scheme
COLORS = {
    'bg': '#FFFFFF',
    'primary': '#1E40AF',  # Deep blue
    'secondary': '#1E3A8A',  # Navy
    'accent': '#3B82F6',  # Bright blue
    'border': '#475569',  # Dark gray
    'text': '#0F172A',  # Almost black
    'light_bg': '#EBF3FF',  # Light blue
    'light_text': '#64748B'  # Medium gray
}

def create_usecase_diagram():
    """Generate Use Case Diagram for PixelAlchemy"""
    fig, ax = plt.subplots(1, 1, figsize=(20, 12), dpi=100)
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Title
    ax.text(10, 11.5, 'PixelAlchemy: Use Case Diagram', 
            fontsize=28, weight='bold', color=COLORS['secondary'], ha='center',
            bbox=dict(boxstyle='round,pad=0.8', facecolor=COLORS['light_bg'], 
                     edgecolor=COLORS['border'], linewidth=2))

    # Actor (User) on left
    actor_x, actor_y = 2, 6
    # Draw stick figure
    head = Circle((actor_x, actor_y + 0.8), 0.4, color=COLORS['primary'], ec=COLORS['primary'], linewidth=2)
    ax.add_patch(head)
    body = mpatches.Rectangle((actor_x - 0.15, actor_y), 0.3, 0.8, 
                              color=COLORS['primary'], ec=COLORS['primary'], linewidth=2, fill=False)
    ax.add_patch(body)
    left_arm = mpatches.Rectangle((actor_x - 0.6, actor_y + 0.55), 0.45, 0.15,
                                  color=COLORS['primary'], ec=COLORS['primary'], linewidth=2, fill=False)
    ax.add_patch(left_arm)
    right_arm = mpatches.Rectangle((actor_x + 0.15, actor_y + 0.55), 0.45, 0.15,
                                   color=COLORS['primary'], ec=COLORS['primary'], linewidth=2, fill=False)
    ax.add_patch(right_arm)
    left_leg = mpatches.Rectangle((actor_x - 0.15, actor_y - 0.8), 0.15, 0.8,
                                  color=COLORS['primary'], ec=COLORS['primary'], linewidth=2, fill=False)
    ax.add_patch(left_leg)
    right_leg = mpatches.Rectangle((actor_x, actor_y - 0.8), 0.15, 0.8,
                                   color=COLORS['primary'], ec=COLORS['primary'], linewidth=2, fill=False)
    ax.add_patch(right_leg)
    
    ax.text(actor_x, actor_y - 1.3, 'User', fontsize=13, weight='bold', 
           color=COLORS['text'], ha='center')

    # System boundary box (oval)
    system_box = FancyBboxPatch((4.5, 0.5), 14, 10.5, boxstyle="round,pad=0.1",
                               facecolor=COLORS['bg'], edgecolor=COLORS['border'],
                               linewidth=2.5, zorder=1)
    ax.add_patch(system_box)
    ax.text(11.5, 10.8, 'PixelAlchemy System', fontsize=14, weight='bold',
           color=COLORS['secondary'], ha='center',
           bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['light_bg'], 
                    edgecolor=COLORS['border'], linewidth=1.5))

    # Use cases - organized in 3 columns
    usecases = [
        # Column 1 (Canvas Editor)
        {'name': 'Draw Pixel Art', 'pos': (6, 9)},
        {'name': 'Use Eraser', 'pos': (6, 7.5)},
        {'name': 'Fill Bucket', 'pos': (6, 6)},
        {'name': 'Undo/Redo', 'pos': (6, 4.5)},
        {'name': 'Save Artwork', 'pos': (6, 3)},
        # Column 2 (Filters & Color)
        {'name': 'Load Image', 'pos': (11, 9)},
        {'name': 'Apply Filter', 'pos': (11, 7.5)},
        {'name': 'Save Filtered Image', 'pos': (11, 6)},
        {'name': 'View Color Wheel', 'pos': (11, 4.5)},
        {'name': 'Take Quiz', 'pos': (11, 3)},
        # Column 3 (Pattern & Gallery)
        {'name': 'Generate Pattern', 'pos': (16, 9)},
        {'name': 'Export Pattern', 'pos': (16, 7.5)},
        {'name': 'View Gallery', 'pos': (16, 6)},
        {'name': 'Delete Artwork', 'pos': (16, 4.5)},
    ]

    for uc in usecases:
        x, y = uc['pos']
        # Ellipse for use case
        ellipse = mpatches.Ellipse((x, y), 2.2, 0.7, facecolor=COLORS['light_bg'],
                                  edgecolor=COLORS['primary'], linewidth=2)
        ax.add_patch(ellipse)
        ax.text(x, y, uc['name'], fontsize=11, weight='bold', color=COLORS['text'],
               ha='center', va='center')
        
        # Arrow from actor to use case
        arrow = FancyArrowPatch((actor_x + 0.5, actor_y + (0.4 if y > 6 else -0.4)),
                               (x - 1.1, y), arrowstyle='->', mutation_scale=20,
                               color=COLORS['primary'], linewidth=1.5, zorder=2)
        ax.add_patch(arrow)

    plt.tight_layout()
    plt.savefig('uml_usecase.png', dpi=150, bbox_inches='tight', facecolor=COLORS['bg'])
    print("✅ Generated uml_usecase.png")
    plt.close()

def create_class_diagram():
    """Generate Class Diagram for PixelAlchemy"""
    fig, ax = plt.subplots(1, 1, figsize=(20, 12), dpi=100)
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Title
    ax.text(10, 11.5, 'PixelAlchemy: Class Diagram', 
            fontsize=28, weight='bold', color=COLORS['secondary'], ha='center',
            bbox=dict(boxstyle='round,pad=0.8', facecolor=COLORS['light_bg'], 
                     edgecolor=COLORS['border'], linewidth=2))

    # Define classes
    classes = [
        {
            'name': 'PixelAlchemyApp',
            'methods': ['+ start()', '+ stop()', '+ switch_tab(String)'],
            'pos': (10, 9.5)
        },
        {
            'name': 'CanvasEditor',
            'methods': ['+ draw_pixel()', '+ use_eraser()', '+ fill_bucket()', 
                       '+ undo()', '+ redo()', '+ save_artwork()'],
            'pos': (3, 6)
        },
        {
            'name': 'FiltersLab',
            'methods': ['+ load_image()', '+ select_filter()', '+ apply_filter()',
                       '+ show_preview()', '+ save_filtered_image()'],
            'pos': (10, 6)
        },
        {
            'name': 'ColorTheory',
            'methods': ['+ view_color_wheel()', '+ generate_palette()', '+ take_quiz()'],
            'pos': (17, 6)
        },
        {
            'name': 'PatternMaker',
            'methods': ['+ generate_pattern()', '+ modify_parameters()',
                       '+ export_pattern()'],
            'pos': (5, 2.5)
        },
        {
            'name': 'Gallery',
            'methods': ['+ view_gallery()', '+ load_artwork()', '+ delete_artwork()'],
            'pos': (12, 2.5)
        },
        {
            'name': 'DatabaseManager',
            'methods': ['+ connect()', '+ save_image()', '+ load_images()',
                       '+ delete_image()'],
            'pos': (19, 2.5)
        }
    ]

    # Draw class boxes
    for cls in classes:
        x, y = cls['pos']
        box_height = 0.4 + len(cls['methods']) * 0.25 + 0.4
        
        # Main box
        box = FancyBboxPatch((x - 1.2, y - box_height/2), 2.4, box_height,
                            boxstyle="round,pad=0.05", facecolor=COLORS['light_bg'],
                            edgecolor=COLORS['primary'], linewidth=2)
        ax.add_patch(box)
        
        # Class name
        ax.text(x, y + box_height/2 - 0.3, cls['name'], fontsize=11, weight='bold',
               color=COLORS['text'], ha='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['light_bg'],
                        edgecolor=COLORS['primary'], linewidth=1))
        
        # Methods
        method_y = y + box_height/2 - 0.6
        for method in cls['methods']:
            ax.text(x - 1.1, method_y, method, fontsize=8, color=COLORS['text'],
                   ha='left', va='center', family='monospace')
            method_y -= 0.25

    # Draw composition arrows (App to modules)
    app_pos = (10, 9.5)
    composition_targets = [(3, 6), (10, 6), (17, 6), (5, 2.5), (12, 2.5)]
    for target in composition_targets:
        arrow = FancyArrowPatch((app_pos[0], app_pos[1] - 0.5), (target[0], target[1] + 0.5),
                               arrowstyle='->', mutation_scale=15, color=COLORS['primary'],
                               linewidth=2, linestyle='--', zorder=2)
        ax.add_patch(arrow)
        ax.text((app_pos[0] + target[0])/2 + 0.3, (app_pos[1] + target[1])/2,
               '<<uses>>', fontsize=8, color=COLORS['text'], style='italic')

    # Draw dependency arrows (modules to DatabaseManager)
    db_pos = (19, 2.5)
    for source in [(3, 6), (10, 6), (17, 6), (5, 2.5), (12, 2.5)]:
        arrow = FancyArrowPatch((source[0] + 1.2, source[1] - 0.2), (db_pos[0] - 1.2, db_pos[1] + 0.2),
                               arrowstyle='->', mutation_scale=12, color=COLORS['accent'],
                               linewidth=1.5, linestyle=':', zorder=2)
        ax.add_patch(arrow)

    plt.tight_layout()
    plt.savefig('uml_class.png', dpi=150, bbox_inches='tight', facecolor=COLORS['bg'])
    print("✅ Generated uml_class.png")
    plt.close()

def create_sequence_diagram():
    """Generate Sequence Diagram for filter application scenario"""
    fig, ax = plt.subplots(1, 1, figsize=(20, 12), dpi=100)
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Title
    ax.text(10, 11.5, 'PixelAlchemy: Sequence Diagram - Apply Image Filter', 
            fontsize=28, weight='bold', color=COLORS['secondary'], ha='center',
            bbox=dict(boxstyle='round,pad=0.8', facecolor=COLORS['light_bg'], 
                     edgecolor=COLORS['border'], linewidth=2))

    # Actors/objects
    actors = [
        {'name': 'User', 'x': 2},
        {'name': 'FiltersLab', 'x': 7},
        {'name': 'PIL/Pillow', 'x': 12},
        {'name': 'DatabaseManager', 'x': 17}
    ]

    # Draw actor boxes and lifelines
    for actor in actors:
        x = actor['x']
        # Actor box
        box = FancyBboxPatch((x - 0.6, 10.5), 1.2, 0.7, boxstyle="round,pad=0.05",
                            facecolor=COLORS['light_bg'], edgecolor=COLORS['primary'],
                            linewidth=2)
        ax.add_patch(box)
        ax.text(x, 10.85, actor['name'], fontsize=11, weight='bold', color=COLORS['text'],
               ha='center', va='center')
        
        # Lifeline (dashed vertical)
        ax.plot([x, x], [10.5, 1], 'k--', linewidth=1, color=COLORS['border'], alpha=0.5)

    # Interactions (sequence of messages)
    interactions = [
        {'from': 0, 'to': 1, 'y': 10, 'label': '1. Load Image', 'type': 'call'},
        {'from': 1, 'to': 0, 'y': 9.5, 'label': 'Image Loaded', 'type': 'return'},
        {'from': 0, 'to': 1, 'y': 9, 'label': '2. Select Filter', 'type': 'call'},
        {'from': 1, 'to': 0, 'y': 8.5, 'label': 'Filter Selected', 'type': 'return'},
        {'from': 0, 'to': 1, 'y': 8, 'label': '3. Apply Filter', 'type': 'call'},
        {'from': 1, 'to': 2, 'y': 7.5, 'label': 'Process (Threaded)', 'type': 'call'},
        {'from': 2, 'to': 1, 'y': 7, 'label': 'Filtered Data', 'type': 'return'},
        {'from': 1, 'to': 0, 'y': 6.5, 'label': '4. Show Preview', 'type': 'return'},
        {'from': 0, 'to': 1, 'y': 6, 'label': '5. Save Filtered Image', 'type': 'call'},
        {'from': 1, 'to': 3, 'y': 5.5, 'label': 'save_image(data)', 'type': 'call'},
        {'from': 3, 'to': 1, 'y': 5, 'label': 'Success', 'type': 'return'},
        {'from': 1, 'to': 0, 'y': 4.5, 'label': 'Confirmation', 'type': 'return'},
    ]

    for interaction in interactions:
        from_x = actors[interaction['from']]['x']
        to_x = actors[interaction['to']]['x']
        y = interaction['y']
        
        # Arrow
        arrow_style = '->' if interaction['type'] == 'call' else '-'
        arrow = FancyArrowPatch((from_x, y), (to_x, y),
                               arrowstyle=arrow_style, mutation_scale=15,
                               color=COLORS['primary'], linewidth=1.5)
        ax.add_patch(arrow)
        
        # Label
        mid_x = (from_x + to_x) / 2
        ax.text(mid_x, y + 0.2, interaction['label'], fontsize=10, color=COLORS['text'],
               ha='center', bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg'],
                                     edgecolor='none', alpha=0.8))

    plt.tight_layout()
    plt.savefig('uml_sequence.png', dpi=150, bbox_inches='tight', facecolor=COLORS['bg'])
    print("✅ Generated uml_sequence.png")
    plt.close()

def create_activity_diagram():
    """Generate Activity Diagram for PixelAlchemy user workflow"""
    fig, ax = plt.subplots(1, 1, figsize=(20, 14), dpi=100)
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.axis('off')

    # Title
    ax.text(10, 13.5, 'PixelAlchemy: Activity Diagram - App Flow', 
            fontsize=28, weight='bold', color=COLORS['secondary'], ha='center',
            bbox=dict(boxstyle='round,pad=0.8', facecolor=COLORS['light_bg'], 
                     edgecolor=COLORS['border'], linewidth=2))

    # Start circle
    start_circle = Circle((10, 12.5), 0.35, facecolor=COLORS['secondary'],
                         edgecolor=COLORS['secondary'], linewidth=2)
    ax.add_patch(start_circle)
    
    # Activity boxes and flow
    activities = [
        {'text': 'User opens app', 'y': 11.5, 'x': 10, 'width': 2.5, 'height': 0.6},
        {'text': 'Selects a tab', 'y': 10.5, 'x': 10, 'width': 2.5, 'height': 0.6},
    ]

    # Draw initial activities
    for activity in activities:
        box = FancyBboxPatch((activity['x'] - activity['width']/2, activity['y'] - activity['height']/2),
                            activity['width'], activity['height'],
                            boxstyle="round,pad=0.05", facecolor=COLORS['light_bg'],
                            edgecolor=COLORS['primary'], linewidth=2)
        ax.add_patch(box)
        ax.text(activity['x'], activity['y'], activity['text'], fontsize=11, weight='bold',
               color=COLORS['text'], ha='center', va='center')

    # Decision diamond
    decision_x, decision_y = 10, 9
    diamond_size = 1.2
    diamond = Polygon([
        [decision_x, decision_y + diamond_size],
        [decision_x + diamond_size, decision_y],
        [decision_x, decision_y - diamond_size],
        [decision_x - diamond_size, decision_y]
    ], facecolor=COLORS['light_bg'], edgecolor=COLORS['primary'], linewidth=2)
    ax.add_patch(diamond)
    ax.text(decision_x, decision_y, 'Tab\nSelection?', fontsize=10, weight='bold',
           color=COLORS['text'], ha='center', va='center')

    # Branch activities
    branches = [
        {'text': 'Canvas Editor:\nDraw/Erase/Fill', 'x': 2.5, 'y': 7},
        {'text': 'Filters Lab:\nLoad/Apply Filter', 'x': 7, 'y': 7},
        {'text': 'Color Theory:\nView Wheel/Quiz', 'x': 11.5, 'y': 7},
        {'text': 'Pattern Maker:\nGenerate/Export', 'x': 16, 'y': 7},
        {'text': 'Gallery:\nView/Delete', 'x': 19.5, 'y': 7},
    ]

    for branch in branches:
        box = FancyBboxPatch((branch['x'] - 1.3, branch['y'] - 0.6),
                            2.6, 1.2, boxstyle="round,pad=0.05",
                            facecolor=COLORS['light_bg'], edgecolor=COLORS['accent'],
                            linewidth=2)
        ax.add_patch(box)
        ax.text(branch['x'], branch['y'], branch['text'], fontsize=9, weight='bold',
               color=COLORS['text'], ha='center', va='center')
        
        # Arrow from decision to branch
        arrow = FancyArrowPatch((decision_x, decision_y - diamond_size),
                               (branch['x'], branch['y'] + 0.6),
                               arrowstyle='->', mutation_scale=15,
                               color=COLORS['primary'], linewidth=1.5)
        ax.add_patch(arrow)

    # Converging activities
    converging = [
        {'text': 'Saves result', 'y': 5.2, 'x': 10, 'width': 2.5, 'height': 0.6},
        {'text': 'Views in Gallery', 'y': 4.2, 'x': 10, 'width': 2.5, 'height': 0.6},
        {'text': 'Exits App', 'y': 3.2, 'x': 10, 'width': 2.5, 'height': 0.6},
    ]

    for activity in converging:
        box = FancyBboxPatch((activity['x'] - activity['width']/2, activity['y'] - activity['height']/2),
                            activity['width'], activity['height'],
                            boxstyle="round,pad=0.05", facecolor=COLORS['light_bg'],
                            edgecolor=COLORS['primary'], linewidth=2)
        ax.add_patch(box)
        ax.text(activity['x'], activity['y'], activity['text'], fontsize=11, weight='bold',
               color=COLORS['text'], ha='center', va='center')

    # Arrows from branches to converging (simplified - show from center branches)
    for branch in [branches[1], branches[2], branches[3]]:
        arrow = FancyArrowPatch((branch['x'], branch['y'] - 0.6),
                               (10, 5.5), arrowstyle='->', mutation_scale=15,
                               color=COLORS['primary'], linewidth=1.5, alpha=0.6)
        ax.add_patch(arrow)

    # Arrows between converging activities
    for i in range(len(converging) - 1):
        arrow = FancyArrowPatch((10, converging[i]['y'] - converging[i]['height']/2),
                               (10, converging[i+1]['y'] + converging[i+1]['height']/2),
                               arrowstyle='->', mutation_scale=15,
                               color=COLORS['primary'], linewidth=2)
        ax.add_patch(arrow)

    # End circle
    end_circle = Circle((10, 2.2), 0.35, facecolor=COLORS['secondary'],
                       edgecolor=COLORS['secondary'], linewidth=2)
    ax.add_patch(end_circle)
    
    # Arrow to end
    arrow = FancyArrowPatch((10, converging[-1]['y'] - converging[-1]['height']/2),
                           (10, 2.55), arrowstyle='->', mutation_scale=15,
                           color=COLORS['primary'], linewidth=2)
    ax.add_patch(arrow)

    plt.tight_layout()
    plt.savefig('uml_activity.png', dpi=150, bbox_inches='tight', facecolor=COLORS['bg'])
    print("✅ Generated uml_activity.png")
    plt.close()

def main():
    """Generate all UML diagrams"""
    print("=" * 70)
    print("HIGH-QUALITY UML DIAGRAM GENERATION")
    print("=" * 70)
    print(f"Using matplotlib for professional diagram rendering")
    print(f"Target resolution: 1920x1080+ (DPI-optimized)")
    print(f"Output format: PNG with professional styling")
    print("=" * 70)
    print()

    try:
        print("📊 Generating Use Case Diagram...")
        create_usecase_diagram()
        
        print("📊 Generating Class Diagram...")
        create_class_diagram()
        
        print("📊 Generating Sequence Diagram...")
        create_sequence_diagram()
        
        print("📊 Generating Activity Diagram...")
        create_activity_diagram()
        
        print()
        print("=" * 70)
        print("✨ All diagrams generated successfully!")
        print("=" * 70)
        print("Generated files:")
        print("  • uml_usecase.png")
        print("  • uml_class.png")
        print("  • uml_sequence.png")
        print("  • uml_activity.png")
        print()
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating diagrams: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
