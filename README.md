# 🎯 Recoil Simulator

A customizable and interactive **first-person shooter (FPS) recoil simulator** built using Python and Pygame. This tool replicates the feel of weapon recoil found in games like Valorant, CS:GO, and other tactical shooters, with an emphasis on **3D simulation** and accurate spatial projection.

---

## 🕹️ Features

- 🔫 Simulate realistic recoil buildup based on hold time
- 🌐 **3D bullet simulation**: bullets are fired as rays in 3D space and intersect with a flat wall (target plane) ahead
- 🎯 Change the **target distance** to visualize bullet spread at different ranges
- 🎛️ Easy-to-edit weapon profiles (fire rate, max recoil angle, decay rate, etc.)
- 📈 Visual **recoil progress bar** showing buildup over time
- ⬆️ Dynamic recoil and tilt offset logic
- 🔄 Recoil decay (with protection against abuse from spam-clicking)
- 🔊 Integrated SFX when firing

---

## 🎬 Demo

[https://github.com/user-attachments/assets/98124daa-0090-4c35-8e1e-0ed0ad632cca](https://github.com/user-attachments/assets/e6549197-f457-453a-b793-4d4ddad9a931)

---

## 🧰 Requirements

- Python 3.8+
- `pygame`

Install dependencies:

```bash
pip install pygame
```

## 🌐 How the Simulation Works
Each bullet is simulated as a 3D direction vector inside a cone (representing inaccuracy/recoil).

The vector originates from the player's position and intersects with a plane (the target wall) located ```TARGET_DISTANCE``` units away.

The point of intersection determines where the bullet lands on the screen.

The higher the distance, the more spread you'll see from small changes in recoil angle, like in real games.
