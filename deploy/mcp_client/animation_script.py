import bpy
import math
import mathutils

# ==============================================================================
# ANIMATION SCRIPT - Grouped Sine Wave Movement with Different Phases
# ==============================================================================
# Configuration - adjust these values:
FRAME_END = 250              # Animation terminates at frame 250
DELTA_Z = 2.0                # Height movement (amplitude) - reduce for subtle movement
SINE_CYCLES = 2              # Number of full sine cycles in animation

# ==============================================================================
def clear_animation():
    """Clear all existing animation for mesh objects."""
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        if obj.animation_data and obj.animation_data_action:
            action = obj.animation_data.action
            for layer in action.layers:
                if layer.strip:
                    for fcurve in layer.strip.channelbag.fcurves:
                        fcurve.keyframe_points.clear()
    print(f"Cleared existing animations")

def animate_groups():
    """Main animation setup."""
    frame_list = list(range(0, FRAME_END + 1))
    
    seen_groups = set()
    total_groups = 0
    
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        
        # Extract group ID (first word before underscore)
        name_parts = obj.name.lower().split('_')
        group = name_parts[0] if name_parts else obj.name
        
        if group in seen_groups:
            continue
        seen_groups.add(group)
        total_groups += 1
        
        # Get original position
        original_pos = obj.location.copy()
        
        # Phase offset based on group (distribute phases evenly across groups)
        phase_offset = -total_groups * math.pi / (total_groups if total_groups > 1 else 1)
        
        # Keyframe at frame 0: start position (original location)
        obj.location[:] = original_pos
        obj.keyframe_insert('location', frame=frame_list[0])
        
        # Keyframe at frame 250: end of animation
        # Calculate sine wave position at frame 250
        time_progress = frame_list[-1] / FRAME_END
        sine_value = math.sin(2 * math.pi * time_progress + phase_offset)
        offset = sine_value * DELTA_Z
        obj.location[2] = original_pos[2] + offset
        obj.keyframe_insert('location', frame=frame_list[-1])
        
        NUM_CYCLES_POINTS = 12
        keyframe_interval = max(1, int(len(frame_list) / SINE_CYCLES / NUM_CYCLES_POINTS))
        for i in range(0, len(frame_list), keyframe_interval):
            frame = frame_list[i]
            time_progress = frame / FRAME_END
            sine_value = math.sin(2 * math.pi * time_progress + phase_offset)
            offset = sine_value * DELTA_Z
            obj.location[2] = original_pos[2] + offset
            obj.keyframe_insert('location', frame=frame)
    
    print(f"Analyzed {len(seen_groups)} groups")
    print(f"Keyframes set for {total_groups} objects")
    print(f"Animation: {FRAME_END} frames, Amplitude: {DELTA_Z}, Cycles: {SINE_CYCLES}")

def main():
    """Main entry point."""
    clear_animation()
    animate_groups()
    print("Animation setup complete!")

if __name__ == "__main__":
    main()
