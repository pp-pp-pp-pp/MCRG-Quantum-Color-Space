# MCRG Color Space

## Usage Instructions

1. Clone the repository
2. Install required dependencies: `pip install PyQt5 numpy`
3. Run the script
4. Input complex amplitudes for each quantum basis state (|00⟩, |01⟩, |10⟩, |11⟩)
5. Observe the resulting color visualization. Disclaimer: The UI is pretty terrible right now.
   
## Project Overview

This project introduces a novel color space, MCRG (Magenta, Cyan, Red, Green). It offers a unique approach to color representation and manipulation, opening new possibilities in digital color theory.

## Notable Features

1. Simple Number Inputs:
   - Example: MCRG(1, 1, 1, 1) = #FFFFFF (White)
2. Complex Number Inputs, Phase, and Amplitude Manipulation:
   - Example: MCRG(1, 1, 1+2j, 1) = #FF7F7F (Infrared/Salmon)
   The use of complex numbers allows for phase shifts in color representation. Complex number inputs affect both the phase and amplitude of the color components, mimicking quantum state behavior and allowing for highly nuanced color mixing.

3. Infinite Scaling:
   Inputs can be scaled infinitely without changing the output color.
   Example: MCRG(0, 10, 0, -10) = MCRG(0, 1, 0, -1) = #0000FF
   This property is unique to MCRG and offers new ways to think about color intensity.

4. Negative Inputs:
   MCRG allows for negative input values, a novel feature in color spaces. This enables color "subtraction" and interference effects similar to those in quantum systems.
   
   Pure blue (#0000FF) can be achieved with the following non-complex inputs:

- |00⟩ (M): 0
- |01⟩ (C): 1
- |10⟩ (R): 0
- |11⟩ (G): -1

5. Precise Inputs:
   - Example: MCRG(1.13768, 1.25938, 1.239587, 1.23892368579963287) = #e6ffea (very light lime)
## Quantum Mechanics Connection

While the MCRG space has interesting properties on its own, its inspiration from quantum mechanics opens up possibilities for visualizing quantum states and exploring the relationship between quantum phenomena and color perception.

## Future Directions

1. Exploration of higher-dimensional color spaces
2. Potential applications in visualizing quantum entanglement
3. Implications for digital color theory and representation
4. Possible insights into the relationship between quantum mechanics and human color perception
5. Investigation of color harmonies and contrasts unique to MCRG space
6. Development of new color mixing and blending algorithms
7. Exploration of MCRG in digital art and design applications

## MCRG Space

The MCRG color space is a novel departure from traditional color models. By bridging concepts from quantum mechanics with color theory, it offers new ways to think about and manipulate color. 
