import bpy
import math
import mathutils

# =============================================================================
# ANIMATION SCRIPT: Grouped Sine Wave Movement
# =============================================================================
# Usage: Copy this script to Blender File → Scripting → New Script, then run it
#
# Configuration parameters:
FRAME_END = 250              # Animation terminates at frame
DELTA_Z = 2.0                # Height movement (z-axis amplitude)
SINE_CYCLES = 2              # Number of full sine cycles in animation
KEYFRAME_INTERVAL = 15       # Create keyframes every N frames

# =============================================================================
def clear_animation():
    """Clear all existing animation data from scene objects."""
    for obj in bpy.data.objects:
        if obj.animation_data:
            obj.data = None
    bpy.data.objects.update()
    print("Cleared existing animations")

# =============================================================================
def animate_groups():
    """
    Main animation function.
    
    Groups objects by their first name segment (before underscore).
    Each group gets a different phase offset for staggered sine wave motion.
    """
    frame_list = list(range(0, FRAME_END + 1))
    
    # Sort objects by name for consistent grouping
    mesh_objects = sorted([obj for obj in bpy.data.objects if obj.type == 'MESH'])
    
    print(f"\nFound {len(mesh_objects)} mesh objects")
    
    for i, obj in enumerate(mesh_objects, 1):
        original_pos = obj.location.copy()
        
        # Calculate phase offset based on group index
        phase_offset = -i * math.pi / len(mesh_objects) if len(mesh_objects) > 1 else 0
        
        # Frame 0: Start position (sine at offset phase)
        time_progress = 0.0
        sine_value = math.sin(2 * math.pi * time_progress + phase_offset)
        obj.location[2] = original_pos[2] + (sine_value * DELTA_Z)
        obj.keyframe_insert('location', frame=frame_list[0])
        
        # Frame 250: End of animation
        time_progress = 1.0
        sine_value = math.sin(2 * math.pi * time_progress + phase_offset)
        obj.location[2] = original_pos[2] + (sine_value * DELTA_Z)
        obj.keyframe_insert('location', frame=frame_list[-1])
        
        # Intermediate keyframes
        for frame_idx in range(KEYFRAME_INTERVAL, len(frame_list), KEYFRAME_INTERVAL):
            frame = frame_list[frame_idx]
            time_progress = frame / FRAME_END
            sine_value = math.sin(2 * math.pi * time_progress + phase_offset)
            obj.location[2] = original_pos[2] + (sine_value * DELTA_Z)
            obj.keyframe_insert('location', frame=frame)
        
        # Update dependency graph
        obj.update_tag()
    
    print(f"\n✓ Animation keyframes created for {len(mesh_objects)} groups")
    print(f"  Animation: {FRAME_END} frames")
    print(f"  Amplitude: {DELTA_Z}")
    print(f"  Cycles: {SINE_CYCLES}")

# =============================================================================
def preview_animation():
    """Preview the animation by playing it."""
    screen = bpy.context.window_manager.windows[0].screen
    scene = bpy.context.scene
    view_layer = scene.view_layers[0]
    
    print("\n🎬 Starting animation preview...")
    print("  (Animation will play, press ESC or Ctrl+Z to stop)")
    
    # Set render settings
    render = bpy.context.scene.render
    render.fps = 24
    render.fps_base = 1
    
    # Play animation
    playback = screen.playback
    playback.use_still = False
    playback.use_anim = True
    playback.loop = 'ALL'
    playback.time = 0
    
    return True

# =============================================================================
def main():
    """Main entry point for the script."""
    print("=" * 60)
    print("SINE WAVE ANIMATION SETUP")
    print("=" * 60)
    print(f"\nParameters:")
    print(f"  End frame: {FRAME_END}")
    print(f"  Amplitude: {DELTA_Z}")
    print(f"  Cycles: {SINE_CYCLES}")
    print(f"\n  Keyframe interval: {KEYFRAME_INTERVAL} frames")
    print("=" * 60)
    
    clear_animation()
    animate_groups()
    
    print("\n✨ Animation setup complete!")
    print("   To preview: Go to Timeline, click Play button ▶")
    print("=" * 60)
    return True

# =============================================================================
# Run the script when executed directly
# =============================================================================
if __name__ == "__main__":
    main()
