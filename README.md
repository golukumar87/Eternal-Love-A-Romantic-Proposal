# 💘 Romantic Proposal – Python Turtle Animation

An interactive, cinematic **marriage proposal animation** built entirely with Python's Turtle graphics. Walk across a moonlit park, kneel down, and pop the question — with customizable characters, dialogue styles, weather effects, speech synthesis, fireworks, and a "Love Meter" mini-game!

![Language](https://img.shields.io/badge/Language-Python-blue) ![Module](https://img.shields.io/badge/Module-Turtle-green) ![Platform](https://img.shields.io/badge/Platform-Windows-brightgreen) ![Status](https://img.shields.io/badge/Status-Fully%20Interactive-orange)

---

## 🎯 Objective

The main objective of this project is to create a **fully interactive, animated romantic proposal experience** using Python's Turtle graphics library. It tells a complete story:

> A man (default: **Raj**) walks across a scenic sunset-to-night park toward his love (default: **Neha**), gets down on one knee with a ring, and asks **"Will you marry me?"** — with the outcome depending on the viewer's keyboard choices (❤️ **Yes** / 💔 **No**).

The project demonstrates advanced Turtle programming concepts:

- **Multi-layer rendering** using multiple turtle objects (background, characters, hearts, text).
- **State machine design** for scene transitions (startup → walking → proposing → accepted/rejected).
- **Particle systems** for fireworks, rain, snow, petals, sparks, and dust.
- **Procedural character animation** (walking, kneeling, kissing, blinking, swaying).
- **Interactive keyboard input** — a full custom typing interface for names and settings.
- **Mathematical animation** — sine waves for motion, color interpolation, gradients, and physics.

---

## ✨ Features

### 🎨 Fully Customizable Start Screen
- **Step 1 – Names:** Type your name and your partner's name (defaults to **Raj** & **Neha** if left blank).
- **Step 2 – Settings:** Choose from 4 customizable options using arrow keys:
  | Setting | Options |
  |---------|---------|
  | 👒 Proposer Look | Fedora Hat, Top Hat, No Hat (Stylish Hair) |
  | 👗 Partner Look | Gown + Long Hair, Gown + Elegant Bun, Dress + Long Hair, Dress + Elegant Bun |
  | 💬 Dialogue Style | Direct (Ring Focus), Poetic (Love Scrolls), Musical (Song Notes) |
  | 🌦️ Weather Setting | Rainy Drizzle, Cherry Blossom Wind, Winter Snowfall |

### 🌆 Cinematic Scene
- **Sunset-to-night gradient** sky that smoothly transitions as the man walks.
- **Glowing moon** with craters and 3D sphere shading.
- **Ocean** with shimmering moonlight reflection and animated waves.
- **Street lamp** with light rays, glowing bulb, haze aura, and floating dust motes.
- **Cherry blossom tree**, wooden fence, park bench, flowers, and ground hills.
- **Twinkling stars**, shooting meteors, flapping birds, swaying vines, and fireflies.

### 🧍 Realistic Character Animation
- **Blinking eyes** on all characters (deterministic per position).
- **Walking man** with swinging arms/legs, torso tilt, bounce, and footstep dust.
- **Kneeling pose** with a **gold ring and cyan diamond**.
- **Kiss pose** with hugging arms and a pulsing heart at the lips.
- **Woman** with flowing hair, gown folds, and multiple poses (stand, surprised, accepted, kiss).
- **6 spectators** who chat, sway, and **clap** when she says yes!

### 💖 Interactive Proposal
- Typewriter subtitles with blinking cursor and 3D shadow text.
- Speech bubbles with vector tails.
- Press **[Y]** to Accept → 💍 Kiss, fireworks, cheering, floating hearts, celebration!
- Press **[N]** to Reject → 💔 Heartbreak: cracking heart, lightning storm, rain, tears, and a sad walk away.

### 🎮 Love Meter Mini-Game (during the walk)
- **Falling hearts** spawn on the left side of the screen.
- Use **⬆ / ⬇ arrow keys** to move the man and **catch the hearts**.
- Each heart caught adds **10%** to the Love Meter (up to 100%).
- **MAX LOVE (100%)** triggers golden text, extra fireworks, and sparkles!

### 🔊 Windows Speech & Sound Integration
- **Text-to-Speech** via Windows SAPI (`System.Speech`) — the proposal is **spoken aloud**!
  - "Will you marry me?" (male voice)
  - "She said yes!" (female voice)
  - "Achha chalta hoon, duao mein yaad rakhna" (male voice, on rejection)
- Background sound hooks for applause / sad song (disabled by default).

---

## 🧠 How It Works

### The State Machine

The entire animation is driven by a single `while True` loop with a `state` variable:

| State | Description |
|-------|-------------|
| `startup` | Custom name entry + settings selection (keyboard driven) |
| `walking` | Man walks from left to the girl; Love Meter mini-game active |
| `proposing` | Man kneels, ring sparkles, dialogue bubble, **[Y]/[N]** prompt |
| `accepted` | Kiss scene, fireworks, applause, floating hearts, congratulations |
| `rejected` | Cracking heart, lightning, rain, tears, sad goodbye walk |

### Multi-Layer Rendering

Five dedicated turtles keep the animation fast and organized:

| Turtle | Responsibility |
|--------|----------------|
| `bg_turtle` | Static background (sky, moon, sea, lamp, hill, tree, bench, fence) |
| `star_turtle` | Stars, petals, fireflies, meteors, birds, grass, vines, rain, waves |
| `char_turtle` | Characters (man, woman, spectators) and cast shadows |
| `heart_turtle` | Hearts, ring sparkle, fireworks, lightning, clouds, tears, dust |
| `text_turtle` | All text overlays (titles, subtitles, instructions) |

### Key Functions

| Function | Purpose |
|----------|---------|
| `get_ground_y(x)` | Returns ground height using a sine-based hill curve |
| `interpolate_color(c1, c2, f)` | Blends two hex colors for gradients |
| `draw_heart_shape(...)` | Draws filled hearts for decoration |
| `draw_profile_head(...)` | Draws a face profile silhouette with blinking eyes |
| `draw_man_full(...)` / `draw_woman_full(...)` | Rim-light outline + solid silhouette pass for characters |
| `update_fireworks(...)` | Full firework system: rockets, explosions, particles, gravity |
| `update_lightning(...)` | Random zig-zag bolts + full-screen flash on rejection |
| `update_love_meter_game(...)` | Falling-heart catch mini-game + progress HUD |
| `speak_text(text, gender)` | Windows TTS voice synthesis (background thread) |
| `draw_typewriter_subtitle(...)` | Typewriter-style cinematic subtitles |

---

## 🛠️ Requirements

| Requirement | Details |
|-------------|---------|
| **Python** | 3.x (any recent version) |
| **Turtle** | Standard library — no installation needed |
| **Winsound** | Standard library on Windows (for sound hooks) |
| **OS** | Windows recommended (TTS uses PowerShell/System.Speech) |
| **Screen** | 800×600 minimum resolution |

---

## 🚀 How to Run

### From the Command Line

```bash
cd Propose
python propose.py
```

Or, from the project root:

```bash
python "Propose/propose.py"
```

### From VS Code

1. Open `Propose/propose.py` in VS Code.
2. Ensure the **Python extension** is installed.
3. Press **`Ctrl + F5`** (or ▶️ Run) to start.
4. The **Turtle window** opens with the startup card — begin typing names!

---

## 🎮 Controls & How to Play

### Startup Screen — Step 1 (Names)
| Key | Action |
|-----|--------|
| `A–Z`, `0–9`, `-`, `Space` | Type characters |
| `Tab` | Switch between name fields |
| `Backspace` | Delete last character |
| `Enter` | Confirm names (defaults: **Raj** & **Neha**) |

### Startup Screen — Step 2 (Settings)
| Key | Action |
|-----|--------|
| `Up / Down` | Navigate between the 4 settings |
| `Left / Right` | Cycle through options for the selected setting |
| `Enter` | Start the animation! |

### Walking Phase (Love Meter Mini-Game)
| Key | Action |
|-----|--------|
| `Up / Down` | Move the man up/down to **catch falling hearts** 💖 |

### Proposing Phase
| Key | Action |
|-----|--------|
| `Y` / `y` | 💍 **Accept** — marry them! |
| `N` / `n` | 💔 **Reject** — break their heart... |

---

## 🎛️ Customization Ideas

Here are easy edits to make the animation your own:

| Change | Location | Effect |
|--------|----------|--------|
| Default names | `man_name = "Raj"`, `woman_name = "Neha"` | Change fallback names |
| Walk speed | `man_x += 4.5` | Faster/slower approach |
| Love meter gain | `love_meter + 10` | More/less per caught heart |
| Ring color | `"#ffd700"` (gold) | Change ring color |
| Diamond color | `"#00e5ff"` (cyan) | Change gem color |
| Firework colors | `FIREWORK_COLORS` list | Add/change explosion colors |
| Screen size | `screen.setup(800, 600)` | Larger/smaller canvas |
| Frame rate | `time.sleep(0.033)` | Smoothness vs. speed |

---

## 🗂️ File Structure

```
Propose/
├── propose.py    # Main script – full interactive proposal animation
├── README.md     # This documentation file
└── sad_song.wav  # (Optional) sad song file for rejection scene
```

---

## 📸 Expected Experience

1. A sleek glassmorphic **startup card** appears with the title **"💞 ROMANTIC PROPOSAL 💞"**.
2. You type **your name** and **your partner's name**.
3. You pick **hats, dresses, dialogue style, and weather**.
4. The scene fades from a **sunset pink** sky to a **starry night** as the man walks toward his love, catching hearts along the way.
5. He **kneels**, a glowing ring sparkles, and the question appears.
6. Press **Y** → fireworks, cheers, a kiss, and "She said YES!" — or press **N** → a lightning storm, cracking heart, and a tearful farewell.

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'turtle'` | Reinstall Python from [python.org](https://python.org) and enable **"Add Python to PATH"**. |
| No voice / TTS error | Requires Windows with **System.Speech** enabled. The animation runs fine without it. |
| Window closes instantly | Run from a terminal (`python propose.py`) instead of double-clicking. |
| Turtle not responding to keys | Click on the Turtle window first so it has **keyboard focus**. |
| Slow animation | Reduce `time.sleep(0.033)` or set `screen.tracer(0)` updates more efficiently. |
| Missing `sad_song.wav` | Safe — the sad song is disabled by default; the animation still works. |

---

## 📄 License

Part of the **RAJ Project** collection — free to use, modify, and share for learning and personal projects.

---

## 🙏 Acknowledgments

- Built with Python's built-in **Turtle** graphics library.
- Voice synthesis via Windows **System.Speech (SAPI)**.
- Inspired by classic romantic animation projects and recursive/procedural art.

