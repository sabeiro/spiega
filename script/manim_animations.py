"""
Blender Twin IoT Animation Scenes
=================================
Manim animation scripts for IoT presentation.
"""

from manim import *

# Global color palette
SENSOR_COLOR = BLUE
BATTERY_COLOR = RED

# =============================================================================
# Intro
# =============================================================================


class IntroScene(Scene):
    """Simple introduction scene for Blender Twin presentation."""
    def construct(self):
        title = Text("Blender Twin IoT Project", font_size=48)
        subtitle = Text("Real-time sensor data integration", font_size=32)
        subtitle.to_edge(DOWN)
        self.play(Create(title))
        self.play(Create(subtitle))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

# =============================================================================
# Sensor Network
# =============================================================================


class SensorNetworkScene(Scene):
    """Visualize Bluetooth mesh network with multiple sensor nodes."""
    def construct(self):
        # Configuration
        sensor_count = 6
        node_spacing = 2
        mesh_radius = 3  # meters
        # Create scene background
        background = Square(color=WHITE, fill_opacity=0.0)
        # Position sensor nodes around center
        node_positions = np.array([
            [1, 1, 0],      # Central gateway
            [mesh_radius, 0, 0],
            [-mesh_radius, 0, 0],
            [0, mesh_radius, 0],
            [0, -mesh_radius, 0],
            [mesh_radius,mesh_radius,0],
        ])
        # Create sensor nodes with labels
        sensor_labels = [
            "Gateway",
            "daisy seed",  # Temperature
            "axoloti",     # Audio/Sound
            "xiao seeed",        # BLE Mesh
            "M5Stack",        # BLE Mesh
            "ESP32",  # I2S/Touch
        ]
        for i in range(sensor_count):
            pos = node_positions[i]
            label = Text(sensor_labels[i], font_size=20)
            label_node = label.next_to(Circle().scale(0.5),DL,buff=0.3)
            # Animate node creation
            self.play(Create(label_node),FadeIn(Dot(point=pos,radius=0.03,color=YELLOW)))
            self.play(label_node.animate.shift(DOWN*pos[0], RIGHT*pos[1]))
        # Create BLE connection lines
        self.play(Create(DashedLine(start=ORIGIN,end=[mesh_radius, 0, 0],color=BLUE,)))
        self.play(Create(DashedLine(start=ORIGIN,end=[0,mesh_radius, 0],color=BLUE,)))
        self.play(Create(DashedLine(start=ORIGIN,end=[-mesh_radius, 0, 0],color=BLUE,)))
        self.play(Create(DashedLine(start=ORIGIN,end=[0,-mesh_radius, 0],color=BLUE,)))
        legend = VGroup(Tex("BLE Mesh", font_size=20),Line(DashedLine(color=BLUE)).scale(0.3),)
        legend_arr = VGroup(legend)
        legend_arr.arrange(RIGHT, buff=0.1).to_corner(DR)
        self.play(FadeIn(legend_arr), Write(legend_arr))
        # Complete animation
        self.wait(2)
        self.play(FadeOut(background))


# =============================================================================
# MQTT Flow
# =============================================================================


class MQTTFlowScene(Scene):
    """Demonstrate MQTT publish/subscribe architecture."""
    def construct(self):
        # Create MQTT broker central node
        broker = Text("MQTT Broker", font_size=48)
        broker.to_edge(UP)
        # Create topic branches
        topics = VGroup(
            Text("axoloti/audio", font_size=30),
            Text("daisy/sensor", font_size=30),
            Text("xiao/bat", font_size=30),
        )
        # Position topics
        topics[0].align_to(topics[0], LEFT)
        topics[1].align_to(topics[0], LEFT)
        topics[2].align_to(topics[0], LEFT)
        self.play(
            Write(broker),
            Create(topics[0]),
            Create(topics[1]),
            Create(topics[2]),
            lag_ratio=0.1
        )
        # Create subscription arrows
        arrows = VGroup(
            Arrow(broker, topics[0], color=GREEN, buff=0.05),
            Arrow(broker, topics[1], color=GREEN, buff=0.05),
            Arrow(broker, topics[2], color=GREEN, buff=0.05),
        )
        # Simulate message flow
        message = Text(
            "Publish: temperature=25.3°C",
            font_size=24, 
            color=YELLOW
        )
        # Publish animation
        broker_circle = Circle(color=BLUE, radius=0.3)
        self.play(Create(broker_circle))
        # Subscribe notifications
        notification = Text(
            "Subscribed!",
            font_size=24, 
            color=BLUE
        )
        notification_arr = VGroup(notification)
        self.play(Write(notification_arr))
        # Fade out
        self.play(
            FadeOut(broker), 
            FadeOut(topics), 
            FadeOut(notification_arr)
        )


# =============================================================================
# Bridge Architecture
# =============================================================================


class BridgeArchitecture(Scene):
    """Show ESP32-WROOM-32 bridging all platforms."""

    def construct(self):
        # Create title
        title = Text(
            "ESP32 Bridge Architecture",
            font_size=54,
            color=YELLOW
        )
        
        self.play(Write(title))
        
        # Create nodes
        nodes = VGroup()
        
        # Platform labels
        platform_labels = [
            "daisy_seed",
            "ESP32-WROOM",
            "axoloti",
            "xiao",
            "Cloud MQTT"
        ]
        
        # Create and animate nodes
        node_positions = {
            0: UP,
            1: LEFT,
            2: RIGHT,
            3: DOWN,
            4: UL
        }
        
        for i, label in enumerate(platform_labels):
            node = Text(label, font_size=30, color=WHITE)
            node.next_to(node_positions[i], buff=0.5)
            nodes.add(node)
            
            self.play(Create(node))

        # Create connecting lines
        lines = VGroup(
            Arrow(nodes[0], nodes[1], buff=0.2),
            Arrow(nodes[0], nodes[2], buff=0.2),
            Arrow(nodes[0], nodes[3], buff=0.2),
            Arrow(nodes[1], nodes[2], buff=0.2),
            Arrow(nodes[1], nodes[4], buff=0.2),
            Arrow(nodes[2], nodes[3], buff=0.2),
            Arrow(nodes[2], nodes[4], buff=0.2),
            Arrow(nodes[3], nodes[4], buff=0.2),
        )
        self.play(Create(lines))
        
        # Add legend
        legend = VGroup(
            Text("I2C/PWM", font_size=24),
            Text("BLE Mesh", font_size=24),
            Text("WiFi MQTT", font_size=24),
        )
        
        legend.arrange(UP, buff=0.3).to_corner(DR).scale(0.9)
        self.play(Write(legend))
        
        # Complete animation
        self.wait(3)
        self.play(
            FadeOut(nodes),
            FadeOut(lines),
            FadeOut(legend),
            FadeOut(title)
        )


# =============================================================================
# Full Animation
# =============================================================================


class FullAnimation(Scene):
    """Complete Blender Twin project animation."""

    def construct(self):
        # Title sequence
        title = Text(
            "Blender Twin IoT",
            font_size=60,
            color=YELLOW
        )
        title.to_edge(UP)
        self.play(Write(title))
        
        # Hardware overview
        hardware = Text(
            "ESP32-WROOM-32",
            font_size=40
        )
        self.play(Create(hardware))
        
        # Create nodes
        nodes = VGroup(
            Text("daisy_seed", font_size=40, color=RED),
            Text("ESP32-WROOM", font_size=40, color=BLUE),
            Text("axoloti", font_size=40, color=GREEN),
            Text("xiao", font_size=40, color=YELLOW),
        )
        
        # Position nodes
        nodes[0].to_edge(DL)
        nodes[1].to_edge(DOWN)
        nodes[2].to_edge(DR)
        nodes[3].to_edge(UL)
        
        self.play(Create(nodes[0]))
        self.play(Create(nodes[1]))
        self.play(Create(nodes[2]))
        self.play(Create(nodes[3]))
        
        # Create connections
        lines = VGroup(
            Arrow(nodes[0], nodes[1], buff=0.2),
            Arrow(nodes[0], nodes[2], buff=0.2),
            Arrow(nodes[0], nodes[3], buff=0.2),
            Arrow(nodes[1], nodes[2], buff=0.2),
            Arrow(nodes[1], nodes[4], buff=0.2),
            Arrow(nodes[2], nodes[3], buff=0.2),
            Arrow(nodes[2], nodes[4], buff=0.2),
            Arrow(nodes[3], nodes[4], buff=0.2),
        )
        
        # Add descriptions
        descriptions = VGroup(
            Text("I2C/PWM", font_size=24, color=BLUE),
            Text("BLE Mesh", font_size=24, color=RED),
            Text("WiFi MQTT", font_size=24, color=GREEN),
            Text("Audio DSP", font_size=24, color=YELLOW),
        )
        
        descriptions.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(Create(descriptions))
        
        # Fade out
        self.play(FadeOut(title))
        self.play(FadeOut(nodes))
        self.play(FadeOut(lines))
        self.play(FadeOut(descriptions))


class ThreeDSurfacePlot(ThreeDScene):
    def construct(self):
        resolution_fa = 24
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)
        def param_gauss(u, v):
            x = u
            y = v
            sigma, mu = 0.4, [0.0, 0.0]
            d = np.linalg.norm(np.array([x - mu[0], y - mu[1]]))
            z = np.exp(-(d ** 2 / (2.0 * sigma ** 2)))
            return np.array([x, y, z])
        gauss_plane = Surface(
            param_gauss,
            resolution=(resolution_fa, resolution_fa),
            v_range=[-2, +2],
            u_range=[-2, +2]
        )
        gauss_plane.scale(2, about_point=ORIGIN)
        gauss_plane.set_style(fill_opacity=1,stroke_color=GREEN)
        gauss_plane.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)
        axes = ThreeDAxes()
        self.add(axes,gauss_plane)
        
# =============================================================================
# Run
# =============================================================================


if __name__ == "__main__":
    # Uncomment to run specific scene:
    # IntroScene().render()
    # SensorNetworkScene().render()
    # MQTTFlowScene().render()
    # BridgeArchitecture().render()
    FullAnimation().render()
