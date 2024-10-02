import pygame
import sys
import math
import os
import random

# Initialize pygame
pygame.init()

# Screen dimensions (moderately increased size)
width, height = 1200, 900

# Colors
black = (0, 0, 0)

# Ball properties
ball_radius = 15
ball_position = [600, 450]
ball_velocity = [5, 5]
gravity = 0.6
ball_color = (0, 255, 0)  # Initial color of the ball

# Circular obstacle properties
circle_center = [600, 450]
circle_radius = 320
circle_thickness = 15
hue = 0  # Start hue value

# Score
bounces = 0

# Create the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball with Gravity Inside a Circle")

# Font for the score
font = pygame.font.Font(None, 48)  # Adjust font size for larger window

# Create frames directory if it doesn't exist
frames_dir = 'frames'
if not os.path.exists(frames_dir):
    os.makedirs(frames_dir)

# Frame counter
frame_counter = 0

# List to keep track of ball positions and their respective radii and colors
ball_positions = []

# Function to check collision with the circular obstacle
def check_collision(ball_pos, ball_rad, circle_center, circle_rad):
    dist = math.hypot(ball_pos[0] - circle_center[0], ball_pos[1] - circle_center[1])
    return dist + ball_rad > circle_rad

# Function to convert HSV to RGB
def hsv_to_rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    return int(r * 255), int(g * 255), int(b * 255)

# Function to generate a random color different from a given color
def random_color_different_from(exclude_color):
    while True:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if color != exclude_color:
            return color

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Apply gravity
    ball_velocity[1] += gravity

    # Predict the next position of the ball
    next_position = [ball_position[0] + ball_velocity[0], ball_position[1] + ball_velocity[1]]

    # Check for collision with the circular obstacle
    if check_collision(next_position, ball_radius, circle_center, circle_radius):
        # Reflect ball velocity based on the collision with the circular boundary
        dx = next_position[0] - circle_center[0]
        dy = next_position[1] - circle_center[1]
        dist = math.hypot(dx, dy)
        normal_x = dx / dist
        normal_y = dy / dist
        dot_product = ball_velocity[0] * normal_x + ball_velocity[1] * normal_y
        ball_velocity[0] -= 2 * dot_product * normal_x
        ball_velocity[1] -= 2 * dot_product * normal_y

        # Adjust position to ensure the ball is inside the circle after collision
        overlap = circle_radius - (dist + ball_radius)
        next_position[0] += overlap * normal_x
        next_position[1] += overlap * normal_y

        # Increase ball size
        increase_amount = 0.5  # Adjust this value to control how much the ball's size increases
        ball_radius += increase_amount

        # Adjust velocity to compensate for size increase
        ball_velocity[0] *= 1.02
        ball_velocity[1] *= 1.02

        # Increment the bounce score
        bounces += 1

        # Change the ball color to a random color different from the current circle color
        ball_color = random_color_different_from(circle_color)

    # Update ball position
    ball_position = next_position

    # Calculate the edge position for the track
    velocity_magnitude = math.hypot(ball_velocity[0], ball_velocity[1])
    edge_position_x = ball_position[0] - (ball_radius * ball_velocity[0] / velocity_magnitude)
    edge_position_y = ball_position[1] - (ball_radius * ball_velocity[1] / velocity_magnitude)

    # Save ball edge position for the track if it's inside the circle
    if not check_collision(ball_position, ball_radius, circle_center, circle_radius):
        ball_positions.append((int(edge_position_x), int(edge_position_y), ball_radius, ball_color))

    # Clear the screen
    screen.fill(black)

    # Update circle color (HSV to RGB)
    hue = (hue + 0.5) % 360  # Adjust the step value to control the speed of color change
    circle_color = hsv_to_rgb(hue, 1, 1)

    # Draw the circular obstacle
    pygame.draw.circle(screen, circle_color, circle_center, circle_radius, circle_thickness)

    # Draw the ball track with the same thickness and color as the ball's radius
    if len(ball_positions) > 1:
        for i in range(len(ball_positions) - 1):
            start_pos = (ball_positions[i][0], ball_positions[i][1])
            end_pos = (ball_positions[i + 1][0], ball_positions[i + 1][1])
            thickness = int(ball_positions[i][2])  # Use the ball's radius as the thickness
            color = ball_positions[i][3]  # Use the ball's color for the track
            # Draw the thin boundary
            pygame.draw.line(screen, black, start_pos, end_pos, thickness + 2)
            # Draw the colored track
            pygame.draw.line(screen, color, start_pos, end_pos, thickness)
            # Draw circles along the track path for smoother transition
            num_circles = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]) / 5)
            for j in range(num_circles):
                interp_pos_x = start_pos[0] + (end_pos[0] - start_pos[0]) * j / num_circles
                interp_pos_y = start_pos[1] + (end_pos[1] - start_pos[1]) * j / num_circles
                pygame.draw.circle(screen, black, (int(interp_pos_x), int(interp_pos_y)), (thickness // 2) + 1)
                pygame.draw.circle(screen, color, (int(interp_pos_x), int(interp_pos_y)), thickness // 2)

    # Draw the ball with a black boundary
    pygame.draw.circle(screen, black, ball_position, ball_radius + 2)  # Black boundary
    pygame.draw.circle(screen, ball_color, ball_position, ball_radius)  # Ball with changing color

    # Render the score
    score_text = font.render(f"Bounces: {bounces}", True, circle_color)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, circle_center[1] + circle_radius + 30))

    # Save the frame as an image
    frame_filename = os.path.join(frames_dir, f'frame_{frame_counter:04d}.png')
    pygame.image.save(screen, frame_filename)
    frame_counter += 1

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
