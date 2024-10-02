# Bouncing Ball with Gravity Inside a Color-Changing Circle

This project is a Pygame simulation of a ball bouncing with gravity inside a large circle whose color changes over time. The ball grows in size with each bounce and leaves a colorful trail as it moves. The simulation also saves each frame as an image, allowing for the creation of animations or videos from the frames.

## Table of Contents

- [Features](#features)
- [Demo](#demo)

## Features

- **Realistic Physics**: Implements gravity and collision detection with the circular boundary.
- **Dynamic Visuals**:
  - The circle changes color smoothly using HSV to RGB conversion.
  - The ball changes to a random color upon each bounce.
  - The ball leaves a trail that matches its color and size.
- **Growth Mechanic**: The ball increases in size and speed with each bounce.
- **Frame Capture**: Saves each frame as an image in the `frames` directory for animation purposes.
- **Score Display**: Displays the number of bounces in real-time.

## Demo

![Bouncing Ball Simulation](frames/frame_0000.png)

*Note: For a full animation, you can compile the saved frames into a video using tools like FFmpeg.*
