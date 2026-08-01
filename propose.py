import turtle
import math
import random
import time
import threading
import subprocess
import os


screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.title("A Romantic Proposal - Python Turtle Animation")
screen.bgcolor("#fc5c7d")  

screen.tracer(0)

state = "startup"
startup_step = 1  
typing_field = 0  
man_name = ""
woman_name = ""

settings_field = 0 
man_look = 0        
woman_look = 0      
dialogue_style = 0  
weather_style = 0   

man_y_offset = 0    
love_meter = 0     
game_hearts = []   
heart_sparks = []   

firework_rockets = []
firework_particles = []
lightning_active = False
lightning_timer = 0

flowers_x = [-320, -260, -150, -80, 150, 280]

bg_turtle = turtle.Turtle()    
star_turtle = turtle.Turtle()    
char_turtle = turtle.Turtle() 
heart_turtle = turtle.Turtle()   
text_turtle = turtle.Turtle()    

for t in [bg_turtle, star_turtle, char_turtle, heart_turtle, text_turtle]:
    t.hideturtle()
    t.speed(0)
    t.penup()


try:
    import winsound
except ImportError:
    winsound = None

REJECT_SONG_WAV = "sad_song.wav"

def play_sad_song():
    """Disabled background sad song/melody."""
    return

def play_applause():
    """Disabled crowd clapping sound effects."""
    return

def speak_text(text, gender="female"):
    """Speaks text out loud natively on Windows using SAPI with a gender preference."""
    def run_speech():
        try:
            gender_val = "Female" if gender.lower() == "female" else "Male"
            safe_text = text.replace("'", "''")
            cmd = (
                f"powershell -Command \"Add-Type -AssemblyName System.Speech; "
                f"$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                f"$synth.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::{gender_val}); "
                f"$synth.Speak('{safe_text}');\""
            )
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
            
    threading.Thread(target=run_speech, daemon=True).start()


def get_ground_y(x):
    """Calculates ground y coordinate based on the hill's mathematical curve."""
    return -135 + 12 * math.sin(x * 0.005) - 4 * math.cos(x * 0.003)

def rotate_point(px, py, cx, cy, angle_deg):
    """Rotates a point (px, py) around center (cx, cy) by angle_deg degrees."""
    rad = math.radians(angle_deg)
    dx = px - cx
    dy = py - cy
    rx = cx + dx * math.cos(rad) - dy * math.sin(rad)
    ry = cy + dx * math.sin(rad) + dy * math.cos(rad)
    return rx, ry

def interpolate_color(color1, color2, factor):
    """Interpolates between two hex colors."""
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

def draw_circle(t, x, y, r, color):
    """Draws a filled circle centered at (x, y)."""
    t.penup()
    t.goto(x, y - r)
    t.pendown()
    t.fillcolor(color)
    t.pencolor(color)
    t.begin_fill()
    t.circle(r)
    t.end_fill()

def draw_rect(t, x, y, w, h, color):
    """Draws a filled rectangle starting from bottom-left (x, y)."""
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor(color)
    t.pencolor(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(w)
        t.left(90)
        t.forward(h)
        t.left(90)
    t.end_fill()

def draw_heart_shape(t, x, y, size, color, heading=90):
    """Draws a filled heart at (x, y) with tip at the bottom, pointing in the heading direction."""
    t.penup()
    t.goto(x, y)
    t.setheading(heading)
    t.fillcolor(color)
    t.pencolor(color)
    t.begin_fill()
    t.left(40)
    t.forward(size)
    t.circle(size / 2, 200)
    t.left(140)
    t.circle(size / 2, 200)
    t.forward(size)
    t.end_fill()

def draw_heart_left(t, x, y, size, color, heading=90):
    """Draws only the left half of a heart, ending at the cleft."""
    t.penup()
    t.goto(x, y)
    t.setheading(heading)
    t.fillcolor(color)
    t.pencolor(color)
    t.begin_fill()
    t.left(40)
    t.forward(size)
    t.circle(size / 2, 200)
    t.goto(x, y)
    t.end_fill()

def draw_heart_right(t, x, y, size, color, heading=90):
    """Draws only the right half of a heart, starting from the cleft."""
    t.penup()
    t.goto(x, y)
    t.setheading(heading)
    t.fillcolor(color)
    t.pencolor(color)
    t.begin_fill()
    t.left(40)
    t.forward(size)
    t.circle(size / 2, 200)
    t.pendown()
    t.left(140)
    t.circle(size / 2, 200)
    t.forward(size)
    t.goto(x, y)
    t.end_fill()

def draw_blossoms(t, x, y, count=12):
    """Draws a cluster of cherry blossoms around (x, y)."""
    for _ in range(count):
        bx = x + random.randint(-25, 25)
        by = y + random.randint(-18, 18)
        r = random.randint(4, 9)
        color = random.choice(["#ffb7d5", "#ff6ba3", "#ff4081", "#ff80ab"])
        draw_circle(t, bx, by, r, color)

def draw_rounded_rect(t, x, y, w, h, r, fill_color, border_color, border_width=2):
    """Draws a beautiful rounded rectangle."""
    t.penup()
    t.goto(x + r, y)
    t.setheading(0)
    t.pendown()
    t.fillcolor(fill_color)
    t.pencolor(border_color)
    t.width(border_width)
    t.begin_fill()
    for _ in range(2):
        t.forward(w - 2 * r)
        t.circle(r, 90)
        t.forward(h - 2 * r)
        t.circle(r, 90)
    t.end_fill()
    t.penup()

def key_typed(char):
    global man_name, woman_name, typing_field
    if startup_step == 1:
        if typing_field == 0:
            if len(man_name) < 14:
                man_name += char
        else:
            if len(woman_name) < 14:
                woman_name += char

def backspace_typed():
    global man_name, woman_name, typing_field
    if startup_step == 1:
        if typing_field == 0:
            man_name = man_name[:-1]
        else:
            woman_name = woman_name[:-1]

def tab_pressed():
    global typing_field
    if startup_step == 1:
        typing_field = 1 - typing_field

def enter_pressed():
    global state, startup_step, man_name, woman_name, typing_field
    if startup_step == 1:
        if typing_field == 0:
            if not man_name.strip():
                man_name = "Raj"
            typing_field = 1
        else:
            if not woman_name.strip():
                woman_name = "Neha"
            startup_step = 2
            unregister_typing_keys()
            register_settings_keys()
    elif startup_step == 2:
        unregister_settings_keys()
        state = "walking"
        bind_proposal_keys()
        bind_game_keys()

def settings_up():
    global settings_field
    if startup_step == 2:
        settings_field = (settings_field - 1) % 4

def settings_down():
    global settings_field
    if startup_step == 2:
        settings_field = (settings_field + 1) % 4

def settings_left():
    global man_look, woman_look, dialogue_style, weather_style
    if startup_step == 2:
        if settings_field == 0:
            man_look = (man_look - 1) % 3
        elif settings_field == 1:
            woman_look = (woman_look - 1) % 4
        elif settings_field == 2:
            dialogue_style = (dialogue_style - 1) % 3
        elif settings_field == 3:
            weather_style = (weather_style - 1) % 3

def settings_right():
    global man_look, woman_look, dialogue_style, weather_style
    if startup_step == 2:
        if settings_field == 0:
            man_look = (man_look + 1) % 3
        elif settings_field == 1:
            woman_look = (woman_look + 1) % 4
        elif settings_field == 2:
            dialogue_style = (dialogue_style + 1) % 3
        elif settings_field == 3:
            weather_style = (weather_style + 1) % 3

def register_typing_keys():
    for char in "abcdefghijklmnopqrstuvwxyz":
        def make_handler(c=char):
            return lambda: key_typed(c)
        screen.onkey(make_handler(), char)
        def make_handler_upper(c=char.upper()):
            return lambda: key_typed(c)
        screen.onkey(make_handler_upper(), char.upper())
    for char in "0123456789":
        def make_handler_digit(c=char):
            return lambda: key_typed(c)
        screen.onkey(make_handler_digit(), char)
    screen.onkey(lambda: key_typed(" "), "space")
    screen.onkey(lambda: key_typed("-"), "minus")
    screen.onkey(backspace_typed, "BackSpace")
    screen.onkey(enter_pressed, "Return")
    screen.onkey(tab_pressed, "Tab")
    screen.listen()

def unregister_typing_keys():
    for char in "abcdefghijklmnopqrstuvwxyz":
        screen.onkey(None, char)
        screen.onkey(None, char.upper())
    for char in "0123456789":
        screen.onkey(None, char)
    screen.onkey(None, "space")
    screen.onkey(None, "minus")
    screen.onkey(None, "BackSpace")
    screen.onkey(None, "Return")
    screen.onkey(None, "Tab")

def register_settings_keys():
    screen.onkey(settings_up, "Up")
    screen.onkey(settings_down, "Down")
    screen.onkey(settings_left, "Left")
    screen.onkey(settings_right, "Right")
    screen.onkey(enter_pressed, "Return")
    screen.listen()

def unregister_settings_keys():
    screen.onkey(None, "Up")
    screen.onkey(None, "Down")
    screen.onkey(None, "Left")
    screen.onkey(None, "Right")
    screen.onkey(None, "Return")

def bind_proposal_keys():
    screen.onkey(choose_yes, "y")
    screen.onkey(choose_yes, "Y")
    screen.onkey(choose_no, "n")
    screen.onkey(choose_no, "N")
    screen.listen()

def move_man_up():
    global man_y_offset
    if state == "walking":
        man_y_offset = min(35, man_y_offset + 5)

def move_man_down():
    global man_y_offset
    if state == "walking":
        man_y_offset = max(-35, man_y_offset - 5)

def bind_game_keys():
    screen.onkey(move_man_up, "Up")
    screen.onkey(move_man_down, "Down")
    screen.listen()

def draw_startup_screen():
    text_turtle.clear()
    
    draw_rounded_rect(text_turtle, -230, -160, 460, 320, 15, "#0b0718", "#ff2a6d", 3)
    
  
    text_turtle.penup()
    text_turtle.goto(0, 105)
    text_turtle.pencolor("#ff71ce")
    text_turtle.write("💞 ROMANTIC PROPOSAL 💞", align="center", font=("Georgia", 20, "bold"))
    
    if startup_step == 1:
        text_turtle.goto(0, 80)
        text_turtle.pencolor("#ffffff")
        text_turtle.write("Step 1: Customize your characters' names", align="center", font=("Georgia", 11, "italic"))
        
        text_turtle.goto(-190, 35)
        text_turtle.pencolor("#a5f3fc" if typing_field == 0 else "#94a3b8")
        text_turtle.write("Your Name (Proposer):", align="left", font=("Georgia", 11, "bold"))
        
        color_box_1 = "#00d9ff" if typing_field == 0 else "#334155"
        draw_rounded_rect(text_turtle, -190, -5, 380, 32, 6, "#150e26", color_box_1, 2)
        
        text_turtle.penup()
        text_turtle.goto(-175, 4)
        text_turtle.pencolor("#ffffff")
        cursor_1 = " |" if typing_field == 0 and (frame // 10) % 2 == 0 else ""
        text_turtle.write(man_name + cursor_1, align="left", font=("Consolas", 12, "bold"))
        
        text_turtle.goto(-190, -45)
        text_turtle.pencolor("#a5f3fc" if typing_field == 1 else "#94a3b8")
        text_turtle.write("Partner's Name (Woman):", align="left", font=("Georgia", 11, "bold"))
        
        color_box_2 = "#00d9ff" if typing_field == 1 else "#334155"
        draw_rounded_rect(text_turtle, -190, -85, 380, 32, 6, "#150e26", color_box_2, 2)
        
        text_turtle.penup()
        text_turtle.goto(-175, -76)
        text_turtle.pencolor("#ffffff")
        cursor_2 = " |" if typing_field == 1 and (frame // 10) % 2 == 0 else ""
        text_turtle.write(woman_name + cursor_2, align="left", font=("Consolas", 12, "bold"))
        
        text_turtle.goto(0, -115)
        text_turtle.pencolor("#94a3b8")
        text_turtle.write("Press [TAB] to switch fields", align="center", font=("Georgia", 9, "bold"))
        
        text_turtle.goto(0, -138)
        text_turtle.pencolor("#ffb7d5")
        text_turtle.write("Press [ENTER] to proceed to settings", align="center", font=("Georgia", 11, "bold"))
        
        text_turtle.goto(0, -154)
        text_turtle.pencolor("#64748b")
        text_turtle.write("(Defaults to Raj & Neha if blank)", align="center", font=("Georgia", 8, "italic"))
        
    elif startup_step == 2:
        text_turtle.goto(0, 80)
        text_turtle.pencolor("#ffffff")
        text_turtle.write("Step 2: Choose styles & weather", align="center", font=("Georgia", 11, "italic"))
        
        man_options = ["Fedora Hat", "Top Hat", "No Hat (Stylish Hair)"]
        woman_options = ["Gown + Long Hair", "Gown + Elegant Bun", "Dress + Long Hair", "Dress + Elegant Bun"]
        dialogue_options = ["Direct (Ring Focus)", "Poetic (Love Scrolls)", "Musical (Song Notes)"]
        weather_options = ["Rainy Drizzle", "Blossom Wind", "Winter Snowfall"]
        
        settings = [
            ("Proposer Look:", man_options[man_look]),
            ("Partner Look:", woman_options[woman_look]),
            ("Dialogue Style:", dialogue_options[dialogue_style]),
            ("Weather Setting:", weather_options[weather_style])
        ]
        
        start_y = 35
        for i, (label, val) in enumerate(settings):
            is_active = (settings_field == i)
            curr_y = start_y - i * 36
            
            
            text_turtle.penup()
            text_turtle.goto(-190, curr_y)
            text_turtle.pencolor("#a5f3fc" if is_active else "#94a3b8")
            text_turtle.write(label, align="left", font=("Georgia", 10, "bold"))
            
            box_border = "#00d9ff" if is_active else "#334155"
            draw_rounded_rect(text_turtle, -30, curr_y - 8, 220, 24, 4, "#150e26", box_border, 1.5)
            
            text_turtle.penup()
            text_turtle.goto(80, curr_y - 6)
            text_turtle.pencolor("#ffffff" if is_active else "#64748b")
            arrow_l = "< " if is_active else ""
            arrow_r = " >" if is_active else ""
            text_turtle.write(arrow_l + val + arrow_r, align="center", font=("Georgia", 9, "bold"))
            
        text_turtle.goto(0, -115)
        text_turtle.pencolor("#94a3b8")
        text_turtle.write("Press [UP/DOWN] to navigate | [LEFT/RIGHT] to change", align="center", font=("Georgia", 8, "bold"))
        
        text_turtle.goto(0, -138)
        text_turtle.pencolor("#ffd700")
        text_turtle.write("Press [ENTER] to start the animation!", align="center", font=("Georgia", 11, "bold"))
    


def draw_waves(t_wave, frame):
    """Draws moving wave ripples on the sea behind the hill and obstacles."""
    wave_layers = [
        {"y_base": -85, "amp": 2.0, "freq": 0.04, "speed": 0.08, "color": "#1f6b75", "width": 1.5},
        {"y_base": -105, "amp": 2.5, "freq": 0.03, "speed": -0.06, "color": "#1c5d68", "width": 2.0},
        {"y_base": -125, "amp": 3.0, "freq": 0.02, "speed": 0.04, "color": "#154952", "width": 2.5}
    ]
    t_wave.penup()
    for layer in wave_layers:
        t_wave.pencolor(layer["color"])
        t_wave.width(layer["width"])
        drawing = False
        for x in range(-400, 401, 10):
            phase = frame * layer["speed"]
            y = layer["y_base"] + layer["amp"] * math.sin(x * layer["freq"] + phase)
            is_above_ground = y > get_ground_y(x)
            is_blocked = (-385 <= x <= -255) or (-165 <= x <= -115) or (205 <= x <= 245)
            if is_above_ground and not is_blocked:
                if not drawing:
                    t_wave.penup()
                    t_wave.goto(x, y)
                    t_wave.pendown()
                    drawing = True
                else:
                    t_wave.goto(x, y)
            else:
                if drawing:
                    t_wave.penup()
                    drawing = False
        t_wave.penup()

rain_ripples = []

def update_rain(frame, state):
    """Updates raindrops and draws rain and ripple splashes."""
    if state in ["startup", "accepted"]:
        max_drops = 0
    elif state == "rejected":
        max_drops = 80
    else:
        max_drops = 25  
        
    spawn_chance = 0.5 if state == "rejected" else 0.2
    
    if len(raindrops) < max_drops and random.random() < spawn_chance:
        raindrops.append({
            "x": random.randint(-400, 400),
            "y": 300,
            "speed": random.uniform(14, 22) if state == "rejected" else random.uniform(8, 14),
            "length": random.uniform(15, 25) if state == "rejected" else random.uniform(8, 15)
        })
        
    for r in raindrops[:]:
        wind = -4.0 if state == "rejected" else -1.5
        r["x"] += wind
        r["y"] -= r["speed"]
        
        y_floor = get_ground_y(r["x"])
        is_in_sea = (r["y"] <= -75) and (-75 > y_floor)
        
        if r["y"] <= y_floor or is_in_sea:
            impact_y = y_floor if r["y"] <= y_floor else -75
            is_blocked = (-385 <= r["x"] <= -255) or (-165 <= r["x"] <= -115) or (205 <= r["x"] <= 245)
            if not is_blocked:
                rain_ripples.append({
                    "x": r["x"],
                    "y": impact_y,
                    "radius": 1.0,
                    "max_radius": random.uniform(8, 15) if state == "rejected" else random.uniform(5, 10),
                    "life": 8
                })
            raindrops.remove(r)
        elif r["y"] < -300 or r["x"] < -400:
            raindrops.remove(r)
            
    for rp in rain_ripples[:]:
        rp["radius"] += (rp["max_radius"] - rp["radius"]) * 0.3
        rp["life"] -= 1
        if rp["life"] <= 0:
            rain_ripples.remove(rp)
        else:
            alpha = rp["life"] / 8.0
            ripple_color = interpolate_color("#05020c", "#a5f3fc", alpha)
            star_turtle.penup()
            star_turtle.pencolor(ripple_color)
            star_turtle.width(1)
            
            cx, cy = rp["x"], rp["y"]
            r = rp["radius"]
            star_turtle.goto(cx + r, cy)
            star_turtle.pendown()
            for angle in range(0, 361, 45):
                rad = math.radians(angle)
                ex = cx + r * math.cos(rad)
                ey = cy + (r * 0.25) * math.sin(rad)
                star_turtle.goto(ex, ey)
            star_turtle.penup()
            
   
    if state not in ["startup", "accepted"] and len(raindrops) > 0:
        star_turtle.penup()
        star_turtle.pencolor("#00d9ff" if state == "rejected" else "#a5f3fc")
        star_turtle.width(2 if state == "rejected" else 1)
        for r in raindrops:
            wind = -4.0 if state == "rejected" else -1.5
            star_turtle.penup()
            star_turtle.goto(r["x"], r["y"])
            star_turtle.pendown()
            star_turtle.goto(r["x"] + wind * 0.8, r["y"] - r["length"])
        star_turtle.penup()

def update_love_meter_game(t, frame):
    """Updates falling hearts, collision checks, particle sparks, and renders the Love Meter HUD."""
    global love_meter, game_hearts, heart_sparks
    
    if state != "walking":
        game_hearts.clear()
        heart_sparks.clear()
        return

    if frame % 45 == 0 and len(game_hearts) < 4:
        game_hearts.append({
            "x": random.randint(-360, -90),
            "y": 300,
            "speed": random.uniform(3, 5),
            "size": random.randint(8, 12)
        })

    t.width(2)
    for h in game_hearts[:]:
        h["y"] -= h["speed"]
        
        man_center_y = get_ground_y(man_x) + man_y_offset + 35
        dist = math.hypot(h["x"] - man_x, h["y"] - man_center_y)
        if dist < 32:
            # Catch heart!
            love_meter = min(100, love_meter + 10)
            for _ in range(8):
                heart_sparks.append({
                    "x": h["x"],
                    "y": h["y"],
                    "vx": random.uniform(-3, 3),
                    "vy": random.uniform(-1, 4),
                    "color": random.choice(["#ff2a6d", "#ff71ce", "#ffd700"]),
                    "life": random.randint(10, 20)
                })
            game_hearts.remove(h)
            continue
            
        y_floor = get_ground_y(h["x"])
        if h["y"] < y_floor - 20:
            game_hearts.remove(h)
            continue
            
        t.penup()
        t.goto(h["x"], h["y"])
        t.pendown()
        t.fillcolor("#ff2a6d")
        t.pencolor("#ffffff")
        t.begin_fill()
        t.setheading(45)
        t.forward(h["size"])
        t.circle(h["size"]/2, 180)
        t.right(90)
        t.circle(h["size"]/2, 180)
        t.forward(h["size"])
        t.end_fill()

    for s in heart_sparks[:]:
        s["x"] += s["vx"]
        s["y"] += s["vy"]
        s["vy"] -= 0.15  # gravity
        s["life"] -= 1
        if s["life"] <= 0:
            heart_sparks.remove(s)
            continue
        t.penup()
        t.goto(s["x"], s["y"])
        t.dot(random.randint(4, 7), s["color"])

    hud_x, hud_y = -370, 240
    draw_rounded_rect(t, hud_x, hud_y, 180, 28, 6, "#0b0718", "#ff2a6d", 2)
    if love_meter > 0:
        bar_w = int((love_meter / 100.0) * 172)
        draw_rounded_rect(t, hud_x + 4, hud_y + 4, bar_w, 20, 4, "#ff2a6d", "#ff2a6d", 0)
        
    t.penup()
    t.goto(hud_x + 90, hud_y + 6)
    t.pencolor("#ffffff")
    meter_text = f"💖 LOVE METER: {love_meter}%"
    if love_meter == 100:
        meter_text = "💖 MAX LOVE! 💖"
        t.pencolor("#ffd700")
    t.write(meter_text, align="center", font=("Georgia", 9, "bold"))

def draw_typewriter_subtitle(t, text, active_frame_start, x, y, font, color, speed=3):
    """Draws romantic typewriter subtitle text with blinking block cursor."""
    elapsed = frame - active_frame_start
    char_count = min(len(text), elapsed // speed)
    typed_text = text[:char_count]
    
    if char_count < len(text):
        typed_text += "█"
    else:
        if (frame // 10) % 2 == 0:
            typed_text += "_"
            
    write_shadow_text(t, typed_text, x, y, font, color)

def write_shadow_text(t, text, x, y, font, color, shadow_color="#020105"):
    """Writes text with a neat 3D shadow effect."""
    t.penup()
    t.goto(x + 2, y - 2)
    t.pencolor(shadow_color)
    t.write(text, align="center", font=font)
    t.goto(x, y)
    t.pencolor(color)
    t.write(text, align="center", font=font)

def draw_speech_bubble(t, x, y, w, h, text, tail_x, tail_y):
    """Draws a beautiful vector dialogue bubble pointing at tail_x, tail_y."""
    t.width(2)
    t.pencolor("#05020a")
    t.fillcolor("#ffffff")
    
    t.penup()
    t.goto(tail_x, tail_y)
    t.pendown()
    t.begin_fill()
    t.goto(x - 8, y - h/2 + 2)
    t.goto(x + 8, y - h/2 + 2)
    t.goto(tail_x, tail_y)
    t.end_fill()
    
    r = 8
    t.penup()
    t.goto(x - w/2 + r, y - h/2)
    t.pendown()
    t.begin_fill()
    t.goto(x + w/2 - r, y - h/2)
    t.circle(r, 90)
    t.goto(x + w/2, y + h/2 - r)
    t.circle(r, 90)
    t.goto(x - w/2 + r, y + h/2)
    t.circle(r, 90)
    t.goto(x - w/2, y - h/2 + r)
    t.circle(r, 90)
    t.end_fill()
    
    t.penup()
    t.goto(x, y - 7)
    t.pencolor("#05020a")
    t.write(text, align="center", font=("Georgia", 10, "bold"))


def draw_profile_head(t, cx, cy, r, color, dir_x=1, frame=0, blink_offset=0):
    """Draws detailed face profile, and draws blinking white eye highlight."""
    scale = r / 12.0
    points = [
        (-5, -12), (-9, -8), (-12, -3), (-12, 3), (-9, 8), (-5, 11), (0, 12),
        (8, 9), (7, 2), (14, -2), (7, -5), (10, -9), (9, -14), (4, -12)
    ]
    t.penup()
    t.goto(cx + points[0][0] * dir_x * scale, cy + points[0][1] * scale)
    t.pendown()
    t.fillcolor(color)
    t.pencolor(color)
    t.begin_fill()
    for pt in points[1:]:
        t.goto(cx + pt[0] * dir_x * scale, cy + pt[1] * scale)
    t.goto(cx + points[0][0] * dir_x * scale, cy + points[0][1] * scale)
    t.end_fill()
    
    
    if color == "#05020a": 
        is_blinking = (frame + blink_offset) % 140 < 4
        if not is_blinking:
            eye_x = cx + 5 * dir_x * scale
            eye_y = cy + 2 * scale
            draw_circle(t, eye_x, eye_y, 1.2, "#ffffff")

def draw_cast_shadow(t, x, width=12):
    """Draws a conforming dark purple ground shadow stretching away from the lamppost."""
    y_base = get_ground_y(x)
    dx = x - 210
    shadow_len = dx * 0.35 
    t.penup()
    t.goto(x, y_base)
    t.pendown()
    t.pencolor("#0c0714")  
    
    steps = 8
    for i in range(steps + 1):
        factor = i / float(steps)
        curr_x = x + shadow_len * factor
        curr_y = get_ground_y(curr_x) - 1.5
        t.width(width * (1.0 - factor * 0.5))
        t.goto(curr_x, curr_y)
    t.penup()


def draw_static_background():
    bg_turtle.clear()
    
    for y in range(300, -300, -30):
        factor = (300 - y) / 600
        color = interpolate_color("#05020c", "#1f0f37", factor)
        draw_rect(bg_turtle, -400, y - 30, 800, 30, color)
        
    moon_x, moon_y = 200, 100
    draw_circle(bg_turtle, moon_x, moon_y, 115, "#1b112c")
    draw_circle(bg_turtle, moon_x, moon_y, 95, "#2f2043") 
    draw_circle(bg_turtle, moon_x, moon_y, 75, "#523c58") 
    draw_circle(bg_turtle, moon_x, moon_y, 55, "#fffde6")   
    
    # Lunar craters
    draw_circle(bg_turtle, moon_x - 18, moon_y + 15, 10, "#ebdcb9")
    draw_circle(bg_turtle, moon_x + 22, moon_y - 12, 8, "#ebdcb9")
    draw_circle(bg_turtle, moon_x - 8, moon_y - 25, 6, "#ebdcb9")
    draw_circle(bg_turtle, moon_x + 10, moon_y + 20, 5, "#ebdcb9")
    
    bg_turtle.width(1)
    bg_turtle.penup()
    bg_turtle.goto(moon_x - 55, moon_y)
    bg_turtle.pendown()
    bg_turtle.fillcolor("#e8dfc0")
    bg_turtle.pencolor("#e8dfc0")
    bg_turtle.begin_fill()
    bg_turtle.setheading(270)
    bg_turtle.circle(55, 180)  
    bg_turtle.setheading(125)
    bg_turtle.circle(68, 110)  
    bg_turtle.end_fill()
    
    sea_horizon = -75
    for y in range(sea_horizon, -300, -10):
        factor = (sea_horizon - y) / 225.0
        color = interpolate_color("#144d53", "#080c16", factor)
        draw_rect(bg_turtle, -400, y - 10, 800, 10, color)
    for y in range(sea_horizon, -300, -6):
        factor = (sea_horizon - y) / 225.0
        ref_w = 40 + factor * 80
        ref_color = interpolate_color("#ffd700", "#080c16", factor)
        bg_turtle.penup()
        bg_turtle.goto(200 - ref_w/2, y)
        bg_turtle.pendown()
        bg_turtle.pencolor(ref_color)
        bg_turtle.width(2)
        bg_turtle.goto(200 + ref_w/2, y)

    
    bg_turtle.pencolor("#47383a") 
    bg_turtle.width(1.5)
    for target_x in range(30, 310, 8):
        bg_turtle.penup()
        bg_turtle.goto(210, 68)
        bg_turtle.pendown()
        bg_turtle.goto(target_x, get_ground_y(target_x))

    
    bg_turtle.width(6)
    bg_turtle.pencolor("#05020a")
    bg_turtle.penup()
    bg_turtle.goto(240, get_ground_y(240))
    bg_turtle.pendown()
    bg_turtle.goto(240, 90)
    bg_turtle.goto(210, 90)
    bg_turtle.goto(210, 80)
    
  
    bg_turtle.width(1)
    bg_turtle.penup()
    bg_turtle.goto(200, 80)
    bg_turtle.pendown()
    bg_turtle.fillcolor("#05020a")
    bg_turtle.begin_fill()
    bg_turtle.goto(220, 80)
    bg_turtle.goto(215, 86)
    bg_turtle.goto(205, 86)
    bg_turtle.goto(200, 80)
    bg_turtle.end_fill()
    
  
    bg_turtle.penup()
    bg_turtle.goto(202, 80)
    bg_turtle.fillcolor("#ffd700")
    bg_turtle.pencolor("#ffd700")
    bg_turtle.begin_fill()
    bg_turtle.goto(218, 80)
    bg_turtle.goto(214, 68)
    bg_turtle.goto(206, 68)
    bg_turtle.goto(202, 80)
    bg_turtle.end_fill()
    
   
    bg_color = "#0b0718"
    draw_circle(bg_turtle, 210, 68, 80, interpolate_color(bg_color, "#ffd700", 0.08))
    draw_circle(bg_turtle, 210, 68, 50, interpolate_color(bg_color, "#ffd700", 0.16))
    draw_circle(bg_turtle, 210, 68, 30, interpolate_color(bg_color, "#ffd700", 0.32))
    
   
    bg_turtle.penup()
    bg_turtle.goto(-400, -300)
    bg_turtle.pendown()
    bg_turtle.fillcolor("#05020a")  
    bg_turtle.pencolor("#05020a")
    bg_turtle.begin_fill()
    for sx in range(-400, 401, 10):
        bg_turtle.goto(sx, get_ground_y(sx))
    bg_turtle.goto(400, -300)
    bg_turtle.end_fill()
    
    bx = -160
    by = get_ground_y(bx) + 20
    bg_turtle.width(4)
    bg_turtle.pencolor("#05020a")
  
    bg_turtle.penup()
    bg_turtle.goto(bx, by)
    bg_turtle.pendown()
    bg_turtle.goto(bx + 40, by)
  
    bg_turtle.penup()
    bg_turtle.goto(bx, by + 12)
    bg_turtle.pendown()
    bg_turtle.goto(bx + 40, by + 12)
  
    bg_turtle.width(3)
    bg_turtle.penup()
    bg_turtle.goto(bx + 5, by)
    bg_turtle.pendown()
    bg_turtle.goto(bx + 5, get_ground_y(bx + 5))
    bg_turtle.penup()
    bg_turtle.goto(bx + 35, by)
    bg_turtle.pendown()
    bg_turtle.goto(bx + 35, get_ground_y(bx + 35))
    bg_turtle.penup()
    bg_turtle.goto(bx + 2, by)
    bg_turtle.pendown()
    bg_turtle.goto(bx + 5, by + 15)
    bg_turtle.penup()
    bg_turtle.goto(bx + 38, by)
    bg_turtle.pendown()
    bg_turtle.goto(bx + 35, by + 15)
    
    bg_turtle.width(4)
    for fx in range(-380, -260, 25):
        fgy = get_ground_y(fx)
        bg_turtle.penup()
        bg_turtle.goto(fx, fgy)
        bg_turtle.pendown()
        bg_turtle.goto(fx, fgy + 35)
        bg_turtle.width(1)
        bg_turtle.begin_fill()
        bg_turtle.goto(fx - 4, fgy + 35)
        bg_turtle.goto(fx, fgy + 40)
        bg_turtle.goto(fx + 4, fgy + 35)
        bg_turtle.goto(fx - 4, fgy + 35)
        bg_turtle.end_fill()
        bg_turtle.width(4)
  
    bg_turtle.penup()
    bg_turtle.goto(-390, get_ground_y(-390) + 12)
    bg_turtle.pendown()
    bg_turtle.goto(-270, get_ground_y(-270) + 12)
    bg_turtle.penup()
    bg_turtle.goto(-390, get_ground_y(-390) + 27)
    bg_turtle.pendown()
    bg_turtle.goto(-270, get_ground_y(-270) + 27)
    
    bg_turtle.penup()
    bg_turtle.goto(-400, -50)
    bg_turtle.pendown()
    bg_turtle.width(18)
    bg_turtle.pencolor("#05020a")
    
    main_branch = [(-400, -50), (-360, 50), (-300, 130), (-220, 180), (-120, 210), (0, 220), (100, 220)]
    for pt in main_branch:
        bg_turtle.goto(pt)
        
    bg_turtle.penup()
    bg_turtle.goto(-300, 130)
    bg_turtle.pendown()
    bg_turtle.width(8)
    sub1 = [(-300, 130), (-200, 110), (-100, 90), (0, 80)]
    for pt in sub1:
        bg_turtle.goto(pt)
        
    bg_turtle.penup()
    bg_turtle.goto(-360, 50)
    bg_turtle.pendown()
    bg_turtle.width(10)
    sub2 = [(-360, 50), (-280, 20), (-180, 5)]
    for pt in sub2:
        bg_turtle.goto(pt)

    # 7. Blossoms
    draw_blossoms(bg_turtle, 100, 220, 10)
    draw_blossoms(bg_turtle, 0, 220, 12)
    draw_blossoms(bg_turtle, -120, 210, 12)
    draw_blossoms(bg_turtle, 0, 80, 12)
    draw_blossoms(bg_turtle, -100, 90, 8)
    draw_blossoms(bg_turtle, -180, 5, 10)

    # 8. Ground flowers
    for fx in flowers_x:
        fy = get_ground_y(fx)
        bg_turtle.width(2)
        bg_turtle.pencolor("#214c24")
        bg_turtle.penup()
        bg_turtle.goto(fx, fy)
        bg_turtle.pendown()
        bg_turtle.goto(fx, fy + 7)
        bg_turtle.penup()
        bg_turtle.goto(fx, fy + 7)
        bg_turtle.pendown()
        bg_turtle.dot(5, random.choice(["#ff2a6d", "#ffde59", "#05d9e8"]))

draw_static_background()


stars = []
for _ in range(45):
    sx = random.randint(-380, 380)
    sy = random.randint(-80, 280)
    dist_to_moon = math.sqrt((sx - 200)**2 + (sy - 100)**2)
    if dist_to_moon > 75:
        stars.append({"x": sx, "y": sy, "r": random.randint(1, 3), "phase": random.uniform(0, 2 * math.pi)})

petals = []
for _ in range(12):
    petals.append({
        "x": random.randint(-380, 50),
        "y": random.randint(50, 220),
        "speed_y": random.uniform(1.0, 2.5),
        "speed_x": random.uniform(0.5, 1.8),
        "phase": random.uniform(0, 2 * math.pi),
        "r": random.randint(3, 6)
    })

fireflies = []
for _ in range(12):
    fireflies.append({
        "x": random.randint(-350, 350),
        "y": random.randint(-90, 180),
        "speed_x": random.uniform(0.4, 1.2),
        "speed_y": random.uniform(0.3, 1.0),
        "phase_x": random.uniform(0, 2 * math.pi),
        "phase_y": random.uniform(0, 2 * math.pi)
    })

hanging_hearts = [
    {"anchor": (-200, 110), "length": 60, "size": 8, "color": "#ff2a6d", "phase": 0.0},
    {"anchor": (-100, 90), "length": 50, "size": 6, "color": "#ff71ce", "phase": 1.5},
    {"anchor": (-120, 210), "length": 85, "size": 9, "color": "#ff2a6d", "phase": 0.7},
    {"anchor": (0, 80), "length": 45, "size": 7, "color": "#ff71ce", "phase": 2.2}
]

tree_vines = [
    {"anchor": (-300, 130), "length": 35, "phase": 0.0, "size": 5},
    {"anchor": (-250, 150), "length": 45, "phase": 1.2, "size": 6},
    {"anchor": (-200, 110), "length": 30, "phase": 0.6, "size": 4},
    {"anchor": (-150, 90), "length": 40, "phase": 2.1, "size": 5},
    {"anchor": (-100, 90), "length": 35, "phase": 1.7, "size": 4},
    {"anchor": (-80, 150), "length": 50, "phase": 0.3, "size": 6},
    {"anchor": (-50, 120), "length": 30, "phase": 2.5, "size": 4},
    {"anchor": (20, 100), "length": 40, "phase": 0.9, "size": 5}
]

step_dust = []

dust_motes = []
for _ in range(15):
    dust_motes.append({
        "x": random.randint(30, 310),
        "y": random.randint(-130, 60),
        "speed_y": random.uniform(0.3, 0.7),
        "speed_x": random.uniform(-0.15, 0.15),
        "phase": random.uniform(0, 2 * math.pi),
        "size": random.uniform(1.2, 2.4)
    })


def draw_dynamic_background(t_sky):
    """Draws background gradient and static elements, interpolating sunset to night."""
    bg_turtle.clear()
    
    top_color = interpolate_color("#fc5c7d", "#05020c", t_sky)
    bottom_color = interpolate_color("#6a82fb", "#1f0f37", t_sky)
    
    for y in range(300, -300, -30):
        factor = (300 - y) / 600
        color = interpolate_color(top_color, bottom_color, factor)
        draw_rect(bg_turtle, -400, y - 30, 800, 30, color)
        
    moon_x, moon_y = 200, 100
    if t_sky > 0.1:
        draw_circle(bg_turtle, moon_x, moon_y, 115, interpolate_color("#fc5c7d", "#1b112c", t_sky))
        draw_circle(bg_turtle, moon_x, moon_y, 95, interpolate_color("#6a82fb", "#2f2043", t_sky))
        draw_circle(bg_turtle, moon_x, moon_y, 75, interpolate_color("#ffb7d5", "#523c58", t_sky))
    draw_circle(bg_turtle, moon_x, moon_y, 55, interpolate_color("#ffde59", "#fffde6", t_sky))
    
    draw_circle(bg_turtle, moon_x - 18, moon_y + 15, 10, "#ebdcb9")
    draw_circle(bg_turtle, moon_x + 22, moon_y - 12, 8, "#ebdcb9")
    draw_circle(bg_turtle, moon_x - 8, moon_y - 25, 6, "#ebdcb9")
    draw_circle(bg_turtle, moon_x + 10, moon_y + 20, 5, "#ebdcb9")
    
    bg_turtle.width(1)
    bg_turtle.penup()
    bg_turtle.goto(moon_x - 55, moon_y)
    bg_turtle.pendown()
    bg_turtle.fillcolor("#e8dfc0")
    bg_turtle.pencolor("#e8dfc0")
    bg_turtle.begin_fill()
    bg_turtle.setheading(270)
    bg_turtle.circle(55, 180)
    bg_turtle.setheading(125)
    bg_turtle.circle(68, 110)
    bg_turtle.end_fill()
    
    sea_horizon = -75
    if t_sky > 0.15:
        factor_sea = (t_sky - 0.15) / 0.85
        sea_top_sunset = "#a24857"
        sea_bottom_sunset = "#3b4d8c"
        sea_top_night = "#144d53"
        sea_bottom_night = "#080c16"
        
        top_sea = interpolate_color(sea_top_sunset, sea_top_night, factor_sea)
        bottom_sea = interpolate_color(sea_bottom_sunset, sea_bottom_night, factor_sea)
        
        for y in range(sea_horizon, -300, -10):
            f_y = (sea_horizon - y) / 225.0
            color = interpolate_color(top_sea, bottom_sea, f_y)
            draw_rect(bg_turtle, -400, y - 10, 800, 10, color)
            
        for y in range(sea_horizon, -300, -8):
            f_y = (sea_horizon - y) / 225.0
            ref_w = (40 + f_y * 80) * t_sky
            ref_color = interpolate_color("#ffd700", bottom_sea, f_y)
            bg_turtle.penup()
            bg_turtle.goto(200 - ref_w/2, y)
            bg_turtle.pendown()
            bg_turtle.pencolor(ref_color)
            bg_turtle.width(2)
            bg_turtle.goto(200 + ref_w/2, y)

    if t_sky > 0.3:
        bg_turtle.pencolor(interpolate_color("#1f0f37", "#47383a", (t_sky - 0.3) / 0.7))
        bg_turtle.width(1.5)
        for target_x in range(30, 310, 8):
            bg_turtle.penup()
            bg_turtle.goto(210, 68)
            bg_turtle.pendown()
            bg_turtle.goto(target_x, get_ground_y(target_x))
            
    bg_turtle.width(6)
    bg_turtle.pencolor("#05020a")
    bg_turtle.penup()
    bg_turtle.goto(240, get_ground_y(240))
    bg_turtle.pendown()
    bg_turtle.goto(240, 90)
    bg_turtle.goto(210, 90)
    bg_turtle.goto(210, 80)
    
    bg_turtle.width(1)
    bg_turtle.penup()
    bg_turtle.goto(200, 80)
    bg_turtle.pendown()
    bg_turtle.fillcolor("#05020a")
    bg_turtle.begin_fill()
    bg_turtle.goto(220, 80)
    bg_turtle.goto(215, 86)
    bg_turtle.goto(205, 86)
    bg_turtle.goto(200, 80)
    bg_turtle.end_fill()
    
    bg_turtle.penup()
    bg_turtle.goto(202, 80)
    bulb_color = interpolate_color("#ffeb99", "#ffd700", t_sky)
    bg_turtle.fillcolor(bulb_color)
    bg_turtle.pencolor(bulb_color)
    bg_turtle.begin_fill()
    bg_turtle.goto(218, 80)
    bg_turtle.goto(214, 68)
    bg_turtle.goto(206, 68)
    bg_turtle.goto(202, 80)
    bg_turtle.end_fill()
    
    # Haze Aura Glow bloom overlay
    if t_sky > 0.3:
        bg_c = interpolate_color("#fc5c7d", "#05020c", t_sky)
        draw_circle(bg_turtle, 210, 68, 80, interpolate_color(bg_c, "#ffd700", 0.08 * t_sky))
        draw_circle(bg_turtle, 210, 68, 50, interpolate_color(bg_c, "#ffd700", 0.16 * t_sky))
        draw_circle(bg_turtle, 210, 68, 30, interpolate_color(bg_c, "#ffd700", 0.32 * t_sky))
    
    bg_turtle.penup()
    bg_turtle.goto(-400, -300)
    bg_turtle.pendown()
    bg_turtle.fillcolor("#05020a")
    bg_turtle.pencolor("#05020a")
    bg_turtle.begin_fill()
    for sx in range(-400, 401, 10):
        bg_turtle.goto(sx, get_ground_y(sx))
    bg_turtle.goto(400, -300)
    bg_turtle.end_fill()
    
    bx = -160
    by = get_ground_y(bx) + 20
    bg_turtle.width(4)
    bg_turtle.pencolor("#05020a")
    bg_turtle.penup()
    bg_turtle.goto(bx, by)
    bg_turtle.pendown()
    bg_turtle.goto(bx + 40, by)
    bg_turtle.penup()
    bg_turtle.goto(bx, by + 12)
    bg_turtle.pendown()
    bg_turtle.goto(bx + 40, by + 12)
    bg_turtle.width(3)
    bg_turtle.penup()
    bg_turtle.goto(bx + 5, by)
    bg_turtle.pendown()
    bg_turtle.goto(bx + 5, get_ground_y(bx + 5))
    bg_turtle.penup()
    bg_turtle.goto(bx + 35, by)
    bg_turtle.pendown()
    bg_turtle.goto(bx + 35, get_ground_y(bx + 35))
    bg_turtle.penup()
    bg_turtle.goto(bx + 2, by)
    bg_turtle.pendown()
    bg_turtle.goto(bx + 5, by + 15)
    bg_turtle.penup()
    bg_turtle.goto(bx + 38, by)
    bg_turtle.pendown()
    bg_turtle.goto(bx + 35, by + 15)
    
    bg_turtle.width(4)
    for fx in range(-380, -260, 25):
        fgy = get_ground_y(fx)
        bg_turtle.penup()
        bg_turtle.goto(fx, fgy)
        bg_turtle.pendown()
        bg_turtle.goto(fx, fgy + 35)
        bg_turtle.width(1)
        bg_turtle.begin_fill()
        bg_turtle.goto(fx - 4, fgy + 35)
        bg_turtle.goto(fx, fgy + 40)
        bg_turtle.goto(fx + 4, fgy + 35)
        bg_turtle.goto(fx - 4, fgy + 35)
        bg_turtle.end_fill()
        bg_turtle.width(4)
    bg_turtle.penup()
    bg_turtle.goto(-390, get_ground_y(-390) + 12)
    bg_turtle.pendown()
    bg_turtle.goto(-270, get_ground_y(-270) + 12)
    bg_turtle.penup()
    bg_turtle.goto(-390, get_ground_y(-390) + 27)
    bg_turtle.pendown()
    bg_turtle.goto(-270, get_ground_y(-270) + 27)
    
    bg_turtle.penup()
    bg_turtle.goto(-400, -50)
    bg_turtle.pendown()
    bg_turtle.width(18)
    bg_turtle.pencolor("#05020a")
    main_branch = [(-400, -50), (-360, 50), (-300, 130), (-220, 180), (-120, 210), (0, 220), (100, 220)]
    for pt in main_branch:
        bg_turtle.goto(pt)
    bg_turtle.penup()
    bg_turtle.goto(-300, 130)
    bg_turtle.pendown()
    bg_turtle.width(8)
    sub1 = [(-300, 130), (-200, 110), (-100, 90), (0, 80)]
    for pt in sub1:
        bg_turtle.goto(pt)
    bg_turtle.penup()
    bg_turtle.goto(-360, 50)
    bg_turtle.pendown()
    bg_turtle.width(10)
    sub2 = [(-360, 50), (-280, 20), (-180, 5)]
    for pt in sub2:
        bg_turtle.goto(pt)

    draw_blossoms(bg_turtle, 100, 220, 10)
    draw_blossoms(bg_turtle, 0, 220, 12)
    draw_blossoms(bg_turtle, -120, 210, 12)
    draw_blossoms(bg_turtle, 0, 80, 12)
    draw_blossoms(bg_turtle, -100, 90, 8)
    draw_blossoms(bg_turtle, -180, 5, 10)

    for fx in flowers_x:
        fy = get_ground_y(fx)
        bg_turtle.width(2)
        bg_turtle.pencolor("#214c24")
        bg_turtle.penup()
        bg_turtle.goto(fx, fy)
        bg_turtle.pendown()
        bg_turtle.goto(fx, fy + 7)
        bg_turtle.penup()
        bg_turtle.goto(fx, fy + 7)
        bg_turtle.pendown()
        bg_turtle.dot(5, random.choice(["#ff2a6d", "#ffde59", "#05d9e8"]))


def draw_man_hat_or_hair(t, x, y_head, dir_x, pen_w, draw_color):
    t.width(1)
    t.pencolor(draw_color)
    t.fillcolor(draw_color)
    if man_look == 0:
        
        t.penup()
        t.goto(x - 16 * dir_x, y_head + 11)
        t.pendown()
        t.begin_fill()
        t.goto(x + 16 * dir_x, y_head + 11)
        t.goto(x + 14 * dir_x, y_head + 14)
        t.goto(x + 9 * dir_x, y_head + 14)
        t.goto(x + 7 * dir_x, y_head + 25)
        t.goto(x - 7 * dir_x, y_head + 25)
        t.goto(x - 9 * dir_x, y_head + 14)
        t.goto(x - 14 * dir_x, y_head + 14)
        t.goto(x - 16 * dir_x, y_head + 11)
        t.end_fill()
    elif man_look == 1:
       
        t.penup()
        t.goto(x - 15 * dir_x, y_head + 11)
        t.pendown()
        t.begin_fill()
        t.goto(x + 15 * dir_x, y_head + 11)
        t.goto(x + 13 * dir_x, y_head + 14)
        t.goto(x + 8 * dir_x, y_head + 14)
        t.goto(x + 8 * dir_x, y_head + 38)
        t.goto(x - 8 * dir_x, y_head + 38)
        t.goto(x - 8 * dir_x, y_head + 14)
        t.goto(x - 13 * dir_x, y_head + 14)
        t.goto(x - 15 * dir_x, y_head + 11)
        t.end_fill()
    else:
       
        t.penup()
        t.goto(x - 8 * dir_x, y_head + 9)
        t.pendown()
        t.begin_fill()
        t.goto(x - 11 * dir_x, y_head + 15)
        t.goto(x - 6 * dir_x, y_head + 14)
        t.goto(x - 7 * dir_x, y_head + 22)
        t.goto(x - 2 * dir_x, y_head + 17)
        t.goto(x - 1 * dir_x, y_head + 25)
        t.goto(x + 3 * dir_x, y_head + 18)
        t.goto(x + 5 * dir_x, y_head + 23)
        t.goto(x + 7 * dir_x, y_head + 15)
        t.goto(x + 9 * dir_x, y_head + 8)
        t.goto(x - 8 * dir_x, y_head + 9)
        t.end_fill()
    t.width(pen_w)

def draw_man(t, x, frame, pose="walk", dir_x=1, outline_mode=False):
    """Draws details of the man. Supports walk, kneel, kiss, tilts, folds and outlines."""
    y_base = get_ground_y(x)
    if pose == "walk" and state == "walking":
        y_base += man_y_offset
    
    if outline_mode:
        draw_color = "#ffecb3"  
        pen_w = 8.5
    else:
        draw_color = "#05020a" 
        pen_w = 5.0
        
    t.width(pen_w)
    t.pencolor(draw_color)
    t.fillcolor(draw_color)
    
    blink_offset = abs(int(x)) % 150
    
    if pose == "walk":
        bounce = 2.5 * abs(math.sin(frame * 0.4))
        y_head = y_base + 75 + bounce
        neck_x, neck_y = x, y_head - 12
        
        # 1. Profile Head with blink
        draw_profile_head(t, x, y_head, 12, draw_color, dir_x, frame, blink_offset)
        
        # 2. Hat or Hair
        draw_man_hat_or_hair(t, x, y_head, dir_x, pen_w, draw_color)
        
        # 3. Torso Tilt
        tilt = 4.5 * math.sin(frame * 0.5) * dir_x
        sh_l_x, sh_l_y = rotate_point(x - 11, y_head - 15, neck_x, neck_y, tilt)
        sh_r_x, sh_r_y = rotate_point(x + 11, y_head - 15, neck_x, neck_y, tilt)
        wa_l_x, wa_l_y = rotate_point(x - 7, y_head - 48, neck_x, neck_y, tilt)
        wa_r_x, wa_r_y = rotate_point(x + 7, y_head - 48, neck_x, neck_y, tilt)
        wa_c_x, wa_c_y = rotate_point(x, y_head - 44, neck_x, neck_y, tilt)
        
        # Torso Open Jacket
        t.width(1)
        t.penup()
        t.goto(sh_l_x, sh_l_y)
        t.pendown()
        t.begin_fill()
        t.goto(sh_r_x, sh_r_y)
        t.goto(wa_r_x, wa_r_y)
        t.goto(wa_c_x, wa_c_y)
        t.goto(wa_l_x, wa_l_y)
        t.goto(sh_l_x, sh_l_y)
        t.end_fill()
        
        # 4. Arms
        t.width(pen_w + 1)
        sin_phase = math.sin(frame * 0.25)
        t.penup()
        t.goto(sh_l_x, sh_l_y)
        t.pendown()
        t.goto(sh_l_x - 14 * sin_phase * dir_x, sh_l_y - 20)
        
        t.penup()
        t.goto(sh_r_x, sh_r_y)
        t.pendown()
        t.goto(sh_r_x + 14 * sin_phase * dir_x, sh_r_y - 20)
        
        # Draw clothing details (lapel line) in shadow-grey
        if not outline_mode:
            t.pencolor("#1c182a")
            t.width(1.5)
            t.penup()
            t.goto(neck_x, neck_y)
            t.pendown()
            t.goto(wa_c_x, wa_c_y)
            t.pencolor(draw_color)
            t.width(pen_w)
            
            # Spawn step dust on footstrike
            if abs(sin_phase) > 0.95 and frame % 4 == 0:
                for _ in range(3):
                    step_dust.append({
                        "x": x + random.uniform(-10, 10),
                        "y": y_base,
                        "vx": random.uniform(-1.5, 1.5),
                        "vy": random.uniform(1.0, 3.0),
                        "life": random.randint(8, 12)
                    })
        
        # 5. Legs
        t.width(pen_w + 2)
        t.penup()
        t.goto(wa_l_x, wa_l_y)
        t.pendown()
        lx = x + 16 * sin_phase * dir_x
        t.goto(lx, y_base)
        t.width(pen_w)
        t.goto(lx + 8 * dir_x, y_base)
        
        t.width(pen_w + 2)
        t.penup()
        t.goto(wa_r_x, wa_r_y)
        t.pendown()
        rx = x - 16 * sin_phase * dir_x
        t.goto(rx, y_base)
        t.width(pen_w)
        t.goto(rx + 8 * dir_x, y_base)
        
    elif pose == "kneel":
        y_head = y_base + 50
        draw_profile_head(t, x, y_head, 12, draw_color, dir_x, frame, blink_offset)
        # 2. Hat or Hair
        draw_man_hat_or_hair(t, x, y_head, dir_x, pen_w, draw_color)
        
        # Torso Coat
        t.width(1)
        t.penup()
        t.goto(x - 13, y_head - 18)
        t.pendown()
        t.begin_fill()
        t.goto(x + 11, y_head - 15)
        t.goto(x - 2, y_base + 15)
        t.goto(x - 14, y_base + 15)
        t.goto(x - 13, y_head - 18)
        t.end_fill()
        
        # Arms
        t.width(pen_w + 1)
        t.penup()
        t.goto(x + 10, y_head - 15)
        t.pendown()
        t.goto(x + 24, y_head - 20)
        
        t.penup()
        t.goto(x - 12, y_head - 18)
        t.pendown()
        t.goto(x - 15, y_head - 35)
        
        # Suit crease lines
        if not outline_mode:
            t.pencolor("#1c182a")
            t.width(1.5)
            t.penup()
            t.goto(x - 2, y_head - 15)
            t.pendown()
            t.goto(x - 8, y_base + 15)
            t.pencolor(draw_color)
            t.width(pen_w)
        
        # Legs
        t.width(pen_w + 2)
        t.penup()
        t.goto(x - 2, y_base + 15)
        t.pendown()
        t.goto(x + 12, y_base + 15)
        t.goto(x + 12, y_base)
        t.width(pen_w)
        t.goto(x + 20, y_base)
        
        t.width(pen_w + 2)
        t.penup()
        t.goto(x - 14, y_base + 15)
        t.pendown()
        t.goto(x - 22, y_base)
        t.width(pen_w)
        t.goto(x - 30, y_base)
        
        # Gold Ring & Diamond
        if not outline_mode:
            rx, ry = x + 24, y_head - 20
            t.penup()
            t.goto(rx, ry - 3.5)
            t.pendown()
            t.pencolor("#ffd700")  # Gold
            t.width(2)
            t.circle(3.5)
            
            t.penup()
            t.goto(rx - 2, ry + 3.5)
            t.pendown()
            t.fillcolor("#00e5ff")  # Cyan
            t.pencolor("#00e5ff")
            t.begin_fill()
            t.goto(rx + 2, ry + 3.5)
            t.goto(rx, ry + 7)
            t.goto(rx - 2, ry + 3.5)
            t.end_fill()

    elif pose == "kiss":
        y_head = y_base + 73
        draw_profile_head(t, x + 4, y_head, 12, draw_color, 1, frame, blink_offset)
        
        # 2. Hat or Hair
        draw_man_hat_or_hair(t, x + 4, y_head, 1, pen_w, draw_color)
        
        # Torso leaning right
        t.width(1)
        t.penup()
        t.goto(x - 11, y_head - 15)
        t.pendown()
        t.begin_fill()
        t.goto(x + 15, y_head - 13)
        t.goto(x + 9, y_base + 12)
        t.goto(x - 7, y_base + 10)
        t.goto(x - 11, y_head - 15)
        t.end_fill()
        
        # Hugging arm
        t.width(pen_w + 1)
        t.penup()
        t.goto(x + 9, y_head - 15)
        t.pendown()
        t.goto(x + 23, y_head - 22)
        
        # Other arm resting
        t.penup()
        t.goto(x - 9, y_head - 16)
        t.pendown()
        t.goto(x - 12, y_head - 36)
        
        # Tuxedo lapel line details
        if not outline_mode:
            t.pencolor("#1c182a")
            t.width(1.5)
            t.penup()
            t.goto(x + 2, y_head - 14)
            t.pendown()
            t.goto(x + 4, y_base + 11)
            t.pencolor(draw_color)
            t.width(pen_w)
            
        # Legs
        t.width(pen_w + 2)
        t.penup()
        t.goto(x - 5, y_base + 12)
        t.pendown()
        t.goto(x - 2, y_base)
        t.width(pen_w)
        t.goto(x + 6, y_base)
        
        t.width(pen_w + 2)
        t.penup()
        t.goto(x + 5, y_base + 12)
        t.pendown()
        t.goto(x + 8, y_base)
        t.width(pen_w)
        t.goto(x + 16, y_base)

def draw_woman(t, x, frame, pose="stand", outline_mode=False):
    """Draws detailed woman silhouette. Supports long flowing hair, gown folds, blinking and outline."""
    y_base = get_ground_y(x)
    
    if outline_mode:
        draw_color = "#ffecb3"
        pen_w = 8.5
    else:
        draw_color = "#05020a"
        pen_w = 5.0
        
    t.width(pen_w)
    t.pencolor(draw_color)
    t.fillcolor(draw_color)
    
    y_head = y_base + 75
    blink_offset = abs(int(x)) % 150
    
    if pose != "kiss":
        if woman_look in [0, 2]:
            t.width(1)
            t.penup()
            t.goto(x - 2, y_head + 11)
            t.pendown()
            t.begin_fill()
            t.goto(x + 8, y_head + 10)
            t.goto(x + 14, y_head + 2)
            t.goto(x + 16, y_head - 8)
            t.goto(x + 16, y_head - 18)
            t.goto(x + 12, y_head - 30)
            t.goto(x + 5, y_head - 34)
            t.goto(x + 2, y_head - 25)
            t.goto(x + 2, y_head - 11)
            t.goto(x - 2, y_head + 11)
            t.end_fill()
        else:
            t.width(1)
            t.penup()
            t.goto(x + 9, y_head + 5)
            t.pendown()
            t.begin_fill()
            t.circle(6)
            t.end_fill()
            
            t.penup()
            t.goto(x - 2, y_head + 11)
            t.pendown()
            t.begin_fill()
            t.goto(x + 7, y_head + 10)
            t.goto(x + 10, y_head + 2)
            t.goto(x + 10, y_head - 6)
            t.goto(x + 4, y_head - 8)
            t.goto(x + 2, y_head - 8)
            t.goto(x + 2, y_head - 11)
            t.goto(x - 2, y_head + 11)
            t.end_fill()
            
        draw_profile_head(t, x, y_head, 11, draw_color, -1, frame, blink_offset)
        
        t.width(1)
        t.penup()
        t.goto(x - 8, y_head - 18)
        t.pendown()
        t.begin_fill()
        t.goto(x + 8, y_head - 18)
        t.goto(x + 6, y_head - 32)
        t.goto(x - 6, y_head - 32)
        t.goto(x - 8, y_head - 18)
        t.end_fill()
        
        if woman_look in [0, 1]:
            t.penup()
            t.goto(x - 6, y_head - 32)
            t.pendown()
            t.begin_fill()
            t.goto(x + 6, y_head - 32)
            t.goto(x + 22, y_base)
            t.goto(x + 10, y_base - 2)
            t.goto(x, y_base - 3)
            t.goto(x - 10, y_base - 2)
            t.goto(x - 22, y_base)
            t.goto(x - 6, y_head - 32)
            t.end_fill()
            
            if not outline_mode:
                t.pencolor("#1c182a")
                t.width(1.5)
                t.penup()
                t.goto(x - 3, y_head - 32)
                t.pendown()
                t.goto(x - 10, y_base - 1)
                t.penup()
                t.goto(x + 3, y_head - 32)
                t.pendown()
                t.goto(x + 10, y_base - 1)
                t.pencolor(draw_color)
                t.width(pen_w)
        else:
            t.penup()
            t.goto(x - 6, y_head - 32)
            t.pendown()
            t.begin_fill()
            t.goto(x + 6, y_head - 32)
            t.goto(x + 14, y_base + 22)
            t.goto(x - 14, y_base + 22)
            t.goto(x - 6, y_head - 32)
            t.end_fill()
            
            t.width(pen_w - 0.5)
            t.penup()
            t.goto(x - 3, y_base + 22)
            t.pendown()
            t.goto(x - 3, y_base)
            t.penup()
            t.goto(x + 3, y_base + 22)
            t.pendown()
            t.goto(x + 3, y_base)
            t.width(pen_w)
            
            if not outline_mode:
                t.pencolor("#1c182a")
                t.width(1.5)
                t.penup()
                t.goto(x - 2, y_head - 32)
                t.pendown()
                t.goto(x - 6, y_base + 23)
                t.penup()
                t.goto(x + 2, y_head - 32)
                t.pendown()
                t.goto(x + 6, y_base + 23)
                t.pencolor(draw_color)
                t.width(pen_w)
            
        # 5. Arms
        t.width(pen_w)
        if pose == "stand":
            t.penup()
            t.goto(x - 8, y_head - 18)
            t.pendown()
            t.goto(x - 13, y_head - 38)
            t.goto(x - 13, y_head - 48)
            
            t.penup()
            t.goto(x + 8, y_head - 18)
            t.pendown()
            t.goto(x + 13, y_head - 38)
        elif pose == "surprised":
            t.penup()
            t.goto(x - 8, y_head - 18)
            t.pendown()
            t.goto(x - 12, y_head - 16)
            t.goto(x - 8, y_head - 3)
            
            t.penup()
            t.goto(x + 8, y_head - 18)
            t.pendown()
            t.goto(x - 2, y_head - 1)
        elif pose == "accepted":
            t.penup()
            t.goto(x - 8, y_head - 18)
            t.pendown()
            t.goto(x - 24, y_head - 23)
            
            t.penup()
            t.goto(x - 8, y_head - 18)
            t.pendown()
            t.goto(x - 22, y_head - 28)
            
    else:  
        y_head = y_base + 73
        
        if woman_look in [0, 2]:
            t.width(1)
            t.penup()
            t.goto(x - 6, y_head + 11)
            t.pendown()
            t.begin_fill()
            t.goto(x + 4, y_head + 10)
            t.goto(x + 10, y_head + 2)
            t.goto(x + 12, y_head - 8)
            t.goto(x + 12, y_head - 18)
            t.goto(x + 8, y_head - 30)
            t.goto(x + 1, y_head - 34)
            t.goto(x - 2, y_head - 25)
            t.goto(x - 2, y_head - 11)
            t.goto(x - 6, y_head + 11)
            t.end_fill()
        else:
            # Elegant Hair Bun (leaning left)
            t.width(1)
            t.penup()
            t.goto(x + 5, y_head + 5)
            t.pendown()
            t.begin_fill()
            t.circle(6)
            t.end_fill()
            
            t.penup()
            t.goto(x - 6, y_head + 11)
            t.pendown()
            t.begin_fill()
            t.goto(x + 3, y_head + 10)
            t.goto(x + 6, y_head + 2)
            t.goto(x + 6, y_head - 6)
            t.goto(x + 2, y_head - 8)
            t.goto(x, y_head - 8)
            t.goto(x, y_head - 11)
            t.goto(x - 6, y_head + 11)
            t.end_fill()
            
        draw_profile_head(t, x - 4, y_head, 11, draw_color, -1, frame, blink_offset)
        
        t.width(1)
        t.penup()
        t.goto(x - 15, y_head - 18)
        t.pendown()
        t.begin_fill()
        t.goto(x + 11, y_head - 18)
        t.goto(x + 7, y_head - 32)
        t.goto(x - 9, y_head - 32)
        t.goto(x - 15, y_head - 18)
        t.end_fill()
        
        if woman_look in [0, 1]:
            t.penup()
            t.goto(x - 9, y_head - 32)
            t.pendown()
            t.begin_fill()
            t.goto(x + 7, y_head - 32)
            t.goto(x + 20, y_base)
            t.goto(x + 8, y_base - 2)
            t.goto(x - 2, y_base - 3)
            t.goto(x - 12, y_base - 2)
            t.goto(x - 25, y_base)
            t.goto(x - 9, y_head - 32)
            t.end_fill()
            
            if not outline_mode:
                t.pencolor("#1c182a")
                t.width(1.5)
                t.penup()
                t.goto(x - 5, y_head - 32)
                t.pendown()
                t.goto(x - 12, y_base - 1)
                t.pencolor(draw_color)
                t.width(pen_w)
        else:
            t.penup()
            t.goto(x - 9, y_head - 32)
            t.pendown()
            t.begin_fill()
            t.goto(x + 7, y_head - 32)
            t.goto(x + 13, y_base + 22)
            t.goto(x - 17, y_base + 22)
            t.goto(x - 9, y_head - 32)
            t.end_fill()
            
            t.width(pen_w - 0.5)
            t.penup()
            t.goto(x - 6, y_base + 22)
            t.pendown()
            t.goto(x - 6, y_base)
            t.penup()
            t.goto(x, y_base + 22)
            t.pendown()
            t.goto(x, y_base)
            t.width(pen_w)
            
            if not outline_mode:
                t.pencolor("#1c182a")
                t.width(1.5)
                t.penup()
                t.goto(x - 5, y_head - 32)
                t.pendown()
                t.goto(x - 10, y_base + 23)
                t.pencolor(draw_color)
                t.width(pen_w)
            
        # Hugging arm
        t.width(pen_w)
        t.penup()
        t.goto(x - 11, y_head - 18)
        t.pendown()
        t.goto(x - 23, y_head - 24)
        
        # Other arm resting
        t.penup()
        t.goto(x + 8, y_head - 18)
        t.pendown()
        t.goto(x + 12, y_head - 38)

def draw_spectator(t, x, frame, is_clapping=False, is_talking=False, type="man", dir_x=1, outline_mode=False):
    """Draws a side spectator. Supports clapping hands, chatting gestures and outline highlight."""
    y_base = get_ground_y(x)
    
    if outline_mode:
        draw_color = "#ffecb3"
        pen_w = 8.0
    else:
        draw_color = "#05020a"
        pen_w = 5.0
        
    t.width(pen_w)
    t.pencolor(draw_color)
    t.fillcolor(draw_color)
    
    # Dynamic crowd sway/bobbing
    bob = 1.2 * math.sin(frame * 0.08 + x * 0.05)
    sway = 1.0 * math.cos(frame * 0.06 + x * 0.05)
    y_head = y_base + 75 + bob
    x_head = x + sway
    
    # Deterministic blink offset
    blink_offset = abs(int(x)) % 150
    draw_profile_head(t, x_head, y_head, 10, draw_color, dir_x, frame, blink_offset)
    
    # Torso
    t.width(1)
    t.penup()
    t.goto(x_head - 8 * dir_x, y_head - 12)
    t.pendown()
    t.begin_fill()
    t.goto(x_head + 8 * dir_x, y_head - 12)
    t.goto(x + 6 * dir_x, y_base + 37)
    t.goto(x - 6 * dir_x, y_base + 37)
    t.goto(x_head - 8 * dir_x, y_head - 12)
    t.end_fill()
    
    # Lower Body
    if type == "woman":
        t.penup()
        t.goto(x - 5 * dir_x, y_base + 37)
        t.pendown()
        t.begin_fill()
        t.goto(x + 5 * dir_x, y_base + 37)
        t.goto(x + 11 * dir_x, y_base)
        t.goto(x - 11 * dir_x, y_base)
        t.goto(x - 5 * dir_x, y_base + 37)
        t.end_fill()
    else:
        t.width(pen_w + 1)
        t.penup()
        t.goto(x - 3 * dir_x, y_base + 37)
        t.pendown()
        t.goto(x - 3 * dir_x, y_base)
        t.width(pen_w - 1)
        t.goto(x - 3 * dir_x + 5 * dir_x, y_base)
        
        t.width(pen_w + 1)
        t.penup()
        t.goto(x + 3 * dir_x, y_base + 37)
        t.pendown()
        t.goto(x + 3 * dir_x, y_base)
        t.width(pen_w - 1)
        t.goto(x + 3 * dir_x + 5 * dir_x, y_base)
        
    t.width(pen_w - 0.5)
    if is_clapping:
        x_clap = x_head + 4 * dir_x + 3.5 * math.sin(frame * 1.5)
        t.penup()
        t.goto(x_head - 5 * dir_x, y_head - 14)
        t.pendown()
        t.goto(x_clap, y_head - 20)
        
        t.penup()
        t.goto(x_head + 5 * dir_x, y_head - 14)
        t.pendown()
        t.goto(x_clap, y_head - 20)
    elif is_talking:
        t.penup()
        t.goto(x_head - 7 * dir_x, y_head - 14)
        t.pendown()
        t.goto(x - 8 * dir_x, y_base + 43)
        
        t.penup()
        t.goto(x_head + 5 * dir_x, y_head - 14)
        t.pendown()
        t.goto(x_head + 12 * dir_x, y_head - 24 + 4 * math.sin(frame * 0.25))
    else:
        t.penup()
        t.goto(x_head - 7 * dir_x, y_head - 14)
        t.pendown()
        t.goto(x - 8 * dir_x, y_base + 43)
        
        t.penup()
        t.goto(x_head + 7 * dir_x, y_head - 14)
        t.pendown()
        t.goto(x + 8 * dir_x, y_base + 43)


def draw_man_full(t, x, frame, pose="walk", dir_x=1):
    draw_man(t, x, frame, pose, dir_x, outline_mode=True)
    draw_man(t, x, frame, pose, dir_x, outline_mode=False)

def draw_woman_full(t, x, frame, pose="stand"):
    draw_woman(t, x, frame, pose, outline_mode=True)
    draw_woman(t, x, frame, pose, outline_mode=False)

def draw_spectator_full(t, x, frame, is_clapping=False, is_talking=False, type="man", dir_x=1):
    draw_spectator(t, x, frame, is_clapping, is_talking, type, dir_x, outline_mode=True)
    draw_spectator(t, x, frame, is_clapping, is_talking, type, dir_x, outline_mode=False)


floating_hearts = []


firework_rockets = []
firework_particles = []

FIREWORK_COLORS = ["#ff0040", "#ff6600", "#ffd700", "#00ff88", "#00d9ff", "#ff00ff", "#ff71ce"]

def spawn_firework_rocket():
    """Spawns a new firework rocket from a random ground position."""
    if len(firework_rockets) < 6:
        firework_rockets.append({
            "x": random.randint(-350, 350),
            "y": get_ground_y(random.randint(-350, 350)),
            "target_y": random.randint(50, 250),
            "speed": random.uniform(4, 8),
            "trail": [],
            "exploded": False,
            "color": random.choice(FIREWORK_COLORS),
            "type": random.choice(["peony", "chrysanthemum", "willow"])
        })

def update_fireworks(t_layer, frame):
    """Updates and draws all firework rockets, explosions, and particles."""
    if frame % 30 == 0 and random.random() < 0.4:
        spawn_firework_rocket()
    
    for rocket in firework_rockets[:]:
        if not rocket["exploded"]:
            # Move rocket up
            rocket["y"] += rocket["speed"]
            
            rocket["trail"].append((rocket["x"], rocket["y"]))
            if len(rocket["trail"]) > 12:
                rocket["trail"].pop(0)
            
            if rocket["y"] >= rocket["target_y"]:
                rocket["exploded"] = True
                num_particles = 40 + random.randint(0, 30)
                for _ in range(num_particles):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 8)
                    firework_particles.append({
                        "x": rocket["x"],
                        "y": rocket["y"],
                        "vx": math.cos(angle) * speed,
                        "vy": math.sin(angle) * speed,
                        "color": rocket["color"] if random.random() < 0.7 else random.choice(["#ffffff", "#ffd700"]),
                        "size": random.uniform(2, 5),
                        "life": random.randint(30, 80),
                        "max_life": 80,
                        "type": rocket["type"],
                        "trail": []
                    })
                firework_rockets.remove(rocket)
                continue
            
            for i, (tx, ty) in enumerate(rocket["trail"]):
                alpha = i / len(rocket["trail"])
                t_layer.penup()
                t_layer.goto(tx, ty)
                t_layer.dot(3 * alpha, interpolate_color("#ffd700", rocket["color"], alpha))
            
            # Draw rocket head
            t_layer.penup()
            t_layer.goto(rocket["x"], rocket["y"])
            t_layer.dot(4, "#ffffff")
        else:
            firework_rockets.remove(rocket)
    
    for p in firework_particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] -= 0.08  # Gravity
        p["vx"] *= 0.98  # Air resistance
        p["life"] -= 1
        
        if "trail" not in p:
            p["trail"] = []
        p["trail"].append((p["x"], p["y"]))
        if len(p["trail"]) > 5:
            p["trail"].pop(0)
        
        if p["life"] <= 0 or p["y"] < get_ground_y(p["x"]):
            firework_particles.remove(p)
            continue
        
        # Draw particle with glow
        alpha = p["life"] / p["max_life"]
        size = p["size"] * alpha
        
        # Trail dots
        for i, (tx, ty) in enumerate(p["trail"]):
            t_layer.penup()
            t_layer.goto(tx, ty)
            t_layer.dot(size * 0.5 * (i/len(p["trail"])), interpolate_color(p["color"], "#05020c", 1 - alpha))
        
        # Main particle
        t_layer.penup()
        t_layer.goto(p["x"], p["y"])
        t_layer.dot(size * 2, p["color"])
        
        # Extra glow
        t_layer.dot(size * 3, interpolate_color(p["color"], "#ffffff", 0.2))


lightning_active = False
lightning_timer = 0
lightning_flash_alpha = 0
lightning_bolts = []

def trigger_lightning():
    """Triggers a lightning strike with random bolt pattern."""
    global lightning_active, lightning_flash_alpha, lightning_bolts
    lightning_active = True
    lightning_flash_alpha = 1.0
    
    # Generate zig-zag bolt
    bolt = []
    start_x = random.randint(-200, 200)
    start_y = 200
    bx, by = start_x, start_y
    
    bolt.append((bx, by))
    while by > get_ground_y(bx):
        bx += random.randint(-30, 30)
        by -= random.randint(15, 40)
        # Branching
        if random.random() < 0.3:
            branch_x = bx + random.randint(-20, 20)
            branch_y = by - random.randint(10, 25)
            bolt.append(("branch", bx, by, branch_x, branch_y))
        bolt.append((bx, by))
    
    lightning_bolts = bolt

def update_lightning(t_layer, t_bg, frame):
    """Updates and draws lightning effects."""
    global lightning_flash_alpha, lightning_active
    
    if not lightning_active and random.random() < 0.008:
        trigger_lightning()
        lightning_timer = frame
    
    if lightning_active:
        if lightning_flash_alpha > 0:
            flash_color = interpolate_color("#05020c", "#ffffff", lightning_flash_alpha)
            t_bg.penup()
            t_bg.goto(-400, 300)
            t_bg.pendown()
            t_bg.fillcolor(flash_color)
            t_bg.pencolor(flash_color)
            t_bg.begin_fill()
            t_bg.goto(400, 300)
            t_bg.goto(400, -300)
            t_bg.goto(-400, -300)
            t_bg.goto(-400, 300)
            t_bg.end_fill()
            
            lightning_flash_alpha -= 0.06
            if lightning_flash_alpha <= 0:
                lightning_flash_alpha = 0
                lightning_active = False
        
        # 2. Draw lightning bolt
        t_layer.penup()
        t_layer.width(3)
        t_layer.pencolor("#e0f7ff")
        
        for i in range(len(lightning_bolts)):
            if isinstance(lightning_bolts[i], tuple) and lightning_bolts[i][0] == "branch":
                _, x1, y1, x2, y2 = lightning_bolts[i]
                t_layer.penup()
                t_layer.goto(x1, y1)
                t_layer.pendown()
                t_layer.goto(x2, y2)
            else:
                if i < len(lightning_bolts) - 1:
                    if not (isinstance(lightning_bolts[i+1], tuple) and lightning_bolts[i+1][0] == "branch"):
                        t_layer.penup()
                        t_layer.goto(lightning_bolts[i])
                        t_layer.pendown()
                        t_layer.goto(lightning_bolts[i+1])
        
        t_layer.width(1)
        t_layer.pencolor("#ffffff")
        
        # Inner bright core
        t_layer.width(1.5)
        for i in range(len(lightning_bolts)):
            if isinstance(lightning_bolts[i], tuple) and lightning_bolts[i][0] == "branch":
                continue
            if i < len(lightning_bolts) - 1:
                if not (isinstance(lightning_bolts[i+1], tuple) and lightning_bolts[i+1][0] == "branch"):
                    t_layer.penup()
                    t_layer.goto(lightning_bolts[i])
                    t_layer.pendown()
                    t_layer.goto(lightning_bolts[i+1])


dialogue_music_notes = []
dialogue_poetic_texts = []

def spawn_dialogue_effect(style, frame):
    """Spawns visual effects based on selected dialogue style."""
    if style == 1:  # Musical - spawn music notes
        if frame % 8 == 0 and len(dialogue_music_notes) < 15:
            dialogue_music_notes.append({
                "x": random.randint(-80, -20),
                "y": random.randint(-80, 60),
                "vx": random.uniform(0.5, 2),
                "vy": random.uniform(0.5, 2),
                "note": random.choice(["🎵", "🎶", "♪", "♫"]),
                "life": random.randint(40, 80),
                "max_life": 80,
                "size": random.randint(14, 24)
            })
    elif style == 0:  # Poetic - spawn shayari text
        if frame % 60 == 0 and len(dialogue_poetic_texts) < 4:
            shayaris = [
                "💕 Tumse milna... likhai hai kismat ki...",
                "✨ Chaand bhi hai gawah... aaj ki raat ka...",
                "🌹 Dil ki har dhadkan... tumhare naam hai...",
                "💫 Meri duniya ho tum... har baat mein...",
                "🌟 Sitare bhi jhukte hain... is pyaar ke aage..."
            ]
            dialogue_poetic_texts.append({
                "x": random.randint(-200, 200),
                "y": random.randint(50, 180),
                "text": random.choice(shayaris),
                "life": random.randint(120, 200),
                "max_life": 200,
                "alpha": 0
            })

def update_dialogue_effects(t_layer, frame, style):
    """Updates and draws dialogue style effects."""
    spawn_dialogue_effect(style, frame)
    
    # Musical notes
    for n in dialogue_music_notes[:]:
        n["x"] += n["vx"]
        n["y"] += n["vy"]
        n["vy"] += 0.1
        n["life"] -= 1
        if n["life"] <= 0:
            dialogue_music_notes.remove(n)
            continue
        alpha = n["life"] / n["max_life"]
        t_layer.penup()
        t_layer.goto(n["x"], n["y"])
        t_layer.pencolor(interpolate_color("#ff71ce", "#05020c", 1 - alpha))
        t_layer.write(n["note"], align="center", font=("Arial", n["size"], "bold"))
    
    # Poetic texts
    for p in dialogue_poetic_texts[:]:
        p["life"] -= 1
        if p["life"] > 0:
            p["alpha"] = min(1.0, p["alpha"] + 0.02)
        else:
            p["alpha"] = max(0, p["alpha"] - 0.02)
            if p["alpha"] <= 0:
                dialogue_poetic_texts.remove(p)
                continue
        t_layer.penup()
        t_layer.goto(p["x"], p["y"])
        t_layer.pencolor(interpolate_color("#ffd700", "#ff71ce", 0.5))
        t_layer.write(p["text"], align="center", font=("Georgia", int(10 * p["alpha"]), "bold"))


cherry_petals = []
def init_cherry_petals():
    """Initializes cherry blossom petals for weather style 1."""
    for _ in range(30):
        cherry_petals.append({
            "x": random.randint(-400, 400),
            "y": random.randint(-100, 280),
            "vx": random.uniform(2, 5),
            "vy": random.uniform(-0.5, -2),
            "size": random.randint(3, 7),
            "rotation": random.uniform(0, 360),
            "rot_speed": random.uniform(-5, 5),
            "color": random.choice(["#ffb7d5", "#ff6ba3", "#ff4081", "#ff80ab", "#ffd1dc"])
        })

def update_cherry_blossom(t_layer, frame):
    """Updates and draws cherry blossom wind effect."""
    if len(cherry_petals) < 30 and random.random() < 0.3:
        cherry_petals.append({
            "x": random.randint(350, 400),
            "y": random.randint(50, 280),
            "vx": random.uniform(3, 7),
            "vy": random.uniform(-1.5, -3),
            "size": random.randint(3, 7),
            "rotation": random.uniform(0, 360),
            "rot_speed": random.uniform(-5, 5),
            "color": random.choice(["#ffb7d5", "#ff6ba3", "#ff4081", "#ff80ab", "#ffd1dc"])
        })
    
    for p in cherry_petals[:]:
        p["x"] += p["vx"] + 2 * math.sin(frame * 0.03 + p["rotation"] * 0.01)
        p["y"] += p["vy"]
        p["rotation"] += p["rot_speed"]
        
        if p["x"] > 420 or p["y"] < get_ground_y(p["x"]) - 50:
            p["x"] = random.randint(350, 400)
            p["y"] = random.randint(50, 280)
        
        # Draw petal (small rotated ellipse approximation)
        t_layer.penup()
        t_layer.goto(p["x"], p["y"])
        rad = math.radians(p["rotation"])
        for angle in range(0, 360, 45):
            ex = p["x"] + p["size"] * math.cos(rad) * math.cos(math.radians(angle)) - p["size"] * 0.5 * math.sin(rad) * math.sin(math.radians(angle))
            ey = p["y"] + p["size"] * math.sin(rad) * math.cos(math.radians(angle)) + p["size"] * 0.5 * math.cos(rad) * math.sin(math.radians(angle))
            if angle == 0:
                t_layer.pendown()
                t_layer.fillcolor(p["color"])
                t_layer.pencolor(p["color"])
                t_layer.begin_fill()
            t_layer.goto(ex, ey)
        t_layer.end_fill()
        t_layer.penup()


snowflakes = []
def init_snowflakes():
    """Initializes snowflakes for weather style 2."""
    for _ in range(40):
        snowflakes.append({
            "x": random.randint(-400, 400),
            "y": random.randint(-100, 300),
            "speed": random.uniform(1, 3),
            "drift": random.uniform(-0.5, 0.5),
            "size": random.uniform(2, 5),
            "phase": random.uniform(0, 2 * math.pi),
            "sway": random.uniform(0.3, 1.0)
        })

def update_snowfall(t_layer, frame):
    """Updates and draws winter snowfall effect."""
    if len(snowflakes) < 60 and random.random() < 0.2:
        snowflakes.append({
            "x": random.randint(-400, 400),
            "y": 300,
            "speed": random.uniform(1, 3),
            "drift": random.uniform(-0.5, 0.5),
            "size": random.uniform(2, 5),
            "phase": random.uniform(0, 2 * math.pi),
            "sway": random.uniform(0.3, 1.0)
        })
    
    for s in snowflakes[:]:
        s["y"] -= s["speed"]
        s["x"] += s["drift"] + s["sway"] * math.sin(frame * 0.03 + s["phase"])
        
        if s["y"] < get_ground_y(s["x"]) - 10 or s["x"] < -400 or s["x"] > 400:
            snowflakes.remove(s)
            continue
        
        alpha = min(1.0, (300 - s["y"]) / 200)  # Fade in near top
        t_layer.penup()
        t_layer.goto(s["x"], s["y"])
        t_layer.pencolor("#ffffff")
        t_layer.fillcolor("#ffffff")
        t_layer.begin_fill()
        
        rad = s["size"]
        t_layer.setheading(0)
        for i in range(6):
            t_layer.goto(s["x"] + rad * math.cos(math.radians(i * 60)), s["y"] + rad * math.sin(math.radians(i * 60)))
            t_layer.goto(s["x"], s["y"])
        t_layer.end_fill()
        
        # Soft glow
        t_layer.dot(s["size"] * 2, "#e8f0fe")
def spawn_floating_heart():
    floating_hearts.append({
        "x": random.randint(-40, 90),
        "y": -120,
        "speed_y": random.uniform(2.0, 4.5),
        "speed_x": random.uniform(-0.8, 0.8),
        "size": random.randint(4, 9),
        "color": random.choice(["#ff2a6d", "#ff71ce", "#05d9e8", "#ff007f"]),
        "phase": random.uniform(0, 2 * math.pi)
    })

raindrops = []

active_meteor = None
active_bird = None
teardrops = []

# =========================================================================
# Interactive Keyboard Choice Events
# =========================================================================
def choose_yes():
    global state, accept_frame
    if state == "proposing":
        state = "accepted"
        accept_frame = frame
        speak_text(f"{woman_name} said yes!", gender="female")
        # Play clapping beeps asynchronously
        threading.Thread(target=play_applause, daemon=True).start()
        screen.onkey(None, "y")
        screen.onkey(None, "Y")
        screen.onkey(None, "n")
        screen.onkey(None, "N")

def choose_no():
    global state, reject_frame
    if state == "proposing":
        state = "rejected"
        reject_frame = frame
        speak_text("Achha chalta hoon, duao mein yaad rakhna.", gender="male")
       
        threading.Thread(target=play_sad_song, daemon=True).start()
        screen.onkey(None, "y")
        screen.onkey(None, "Y")
        screen.onkey(None, "n")
        screen.onkey(None, "N")


man_x = -380
state = "startup"     
propose_frame = 0
accept_frame = 0
reject_frame = 0

register_typing_keys()

try:
    while True:
        star_turtle.clear()
        char_turtle.clear()
        heart_turtle.clear()
        text_turtle.clear()
        
        if state == "startup":
            draw_startup_screen()
            screen.update()
            time.sleep(0.033)
            frame += 1
            continue
        
        for star in stars:
            twinkle_r = star["r"] * (0.4 + 0.6 * abs(math.sin(frame * 0.06 + star["phase"])))
            star_turtle.penup()
            star_turtle.goto(star["x"], star["y"])
            star_turtle.dot(twinkle_r * 2, "#fffdd0")
            
        draw_waves(star_turtle, frame)
            
        if active_meteor is None and random.random() < 0.015:
            active_meteor = {
                "x": random.randint(-380, 100),
                "y": random.randint(80, 240),
                "dx": random.uniform(9.0, 14.0),
                "dy": random.uniform(-4.5, -7.5),
                "life": random.randint(9, 14)
            }
        
        if active_meteor is not None:
            mx, my = active_meteor["x"], active_meteor["y"]
            mdx, mdy = active_meteor["dx"], active_meteor["dy"]
            star_turtle.width(1.5)
            star_turtle.pencolor("white")
            star_turtle.penup()
            star_turtle.goto(mx, my)
            star_turtle.pendown()
            star_turtle.goto(mx - 3 * mdx, my - 3 * mdy)
            
            # Update
            active_meteor["x"] += mdx
            active_meteor["y"] += mdy
            active_meteor["life"] -= 1
            if active_meteor["life"] <= 0:
                active_meteor = None
            
        if active_bird is None and random.random() < 0.008:
            active_bird = {
                "x": -420,
                "y": random.randint(80, 200),
                "speed": random.uniform(2.5, 4.0),
                "wing_phase": 0.0
            }
            
        if active_bird is not None:
            bx, by = active_bird["x"], active_bird["y"]
            w_amp = 8 * math.sin(active_bird["wing_phase"])
            
            star_turtle.width(2.5)
            star_turtle.pencolor("#05020a")
            star_turtle.penup()
            star_turtle.goto(bx - 10, by + w_amp)
            star_turtle.pendown()
            star_turtle.goto(bx, by - 2)
            star_turtle.goto(bx + 10, by + w_amp)
            
            # Update
            active_bird["x"] += active_bird["speed"]
            active_bird["wing_phase"] += 0.4
            if active_bird["x"] > 420:
                active_bird = None

        for vine in tree_vines:
            angle = 6 * math.sin(frame * 0.045 + vine["phase"])
            rad = math.radians(angle)
            ax, ay = vine["anchor"]
            L = vine["length"]
            ex = ax + L * math.sin(rad)
            ey = ay - L * math.cos(rad)
            
            star_turtle.width(1.2)
            star_turtle.pencolor("#1d381c")  
            star_turtle.penup()
            star_turtle.goto(ax, ay)
            star_turtle.pendown()
            star_turtle.goto(ex, ey)
            
            star_turtle.penup()
            star_turtle.goto(ex, ey)
            star_turtle.dot(vine["size"], "#2e5a2c")
            star_turtle.goto(ax + L*0.5*math.sin(rad), ay - L*0.5*math.cos(rad))
            star_turtle.dot(vine["size"] - 1, "#2e5a2c")

        if state != "rejected":
            for p in petals:
                p["y"] -= p["speed_y"]
                p["x"] += p["speed_x"] + 0.4 * math.sin(frame * 0.04 + p["phase"])
                if p["y"] < get_ground_y(p["x"]) or p["x"] > 400:
                    p["y"] = random.randint(120, 220)
                    p["x"] = random.randint(-380, -50)
                
                star_turtle.penup()
                star_turtle.goto(p["x"], p["y"])
                star_turtle.dot(p["r"] * 2, "#ffb7d5")

        for ff in fireflies:
            dx = 210 - ff["x"]
            dy = 68 - ff["y"]
            dist = math.sqrt(dx*dx + dy*dy)
            
            fx = (dx / (dist + 1)) * 0.045
            fy = (dy / (dist + 1)) * 0.045
            
            if "vx" not in ff:
                ff["vx"] = 0
                ff["vy"] = 0
                
            ff["vx"] = ff["vx"] * 0.96 + fx + random.uniform(-0.15, 0.15)
            ff["vy"] = ff["vy"] * 0.96 + fy + random.uniform(-0.15, 0.15)
            
            ff["x"] += ff["vx"]
            ff["y"] += ff["vy"]
            
            glow_r = 1.8 + 1.2 * math.sin(frame * 0.12 + ff["phase_x"])
            if glow_r > 0:
                star_turtle.penup()
                star_turtle.goto(ff["x"], ff["y"])
                star_turtle.dot(glow_r * 2, "#d4ff3b")
            
        for mote in dust_motes:
            mote["y"] -= mote["speed_y"]
            mote["x"] += mote["speed_x"] + 0.1 * math.sin(frame * 0.04 + mote["phase"])
            
            if mote["y"] < get_ground_y(mote["x"]) or mote["y"] > 70 or mote["x"] < 30 or mote["x"] > 310:
                mote["y"] = random.randint(50, 68)
                mote["x"] = random.randint(180, 240)
            
            sz = mote["size"] * (0.5 + 0.5 * abs(math.sin(frame * 0.1 + mote["phase"])))
            star_turtle.penup()
            star_turtle.goto(mote["x"], mote["y"])
            star_turtle.dot(sz * 2, "#fff3a8")

        for hh in hanging_hearts:
            angle = 8 * math.sin(frame * 0.045 + hh["phase"])
            rad = math.radians(angle)
            ax, ay = hh["anchor"]
            L = hh["length"]
            ex = ax + L * math.sin(rad)
            ey = ay - L * math.cos(rad)
            
            
            star_turtle.width(1.5)
            star_turtle.pencolor("#301a42")
            star_turtle.penup()
            star_turtle.goto(ax, ay)
            star_turtle.pendown()
            star_turtle.goto(ex, ey)
            
            
            draw_heart_shape(star_turtle, ex, ey, hh["size"], hh["color"], heading=270 + angle)

        star_turtle.width(1.5)
        star_turtle.pencolor("#05020a")
        for gx in range(-390, 390, 15):
            gy = get_ground_y(gx)
            sway = 7 * math.sin(frame * 0.05 + gx * 0.015)
            sway_rad = math.radians(sway)
            
            star_turtle.penup()
            star_turtle.goto(gx, gy)
            star_turtle.pendown()
            star_turtle.goto(gx - 3 + 8 * math.sin(sway_rad), gy + 8 * math.cos(sway_rad))
            
            star_turtle.penup()
            star_turtle.goto(gx, gy)
            star_turtle.pendown()
            star_turtle.goto(gx + 2 + 10 * math.sin(sway_rad), gy + 10 * math.cos(sway_rad))
            
        if weather_style == 1:
            update_cherry_blossom(star_turtle, frame)
        elif weather_style == 2:
            update_snowfall(star_turtle, frame)
        else:
            update_rain(frame, state)

        update_love_meter_game(heart_turtle, frame)

        is_accepted = (state == "accepted")
        t_accept = frame - accept_frame if is_accepted else 0
        
        draw_cast_shadow(char_turtle, -310)
        draw_cast_shadow(char_turtle, -270)
        draw_cast_shadow(char_turtle, -230)
        draw_cast_shadow(char_turtle, 220)
        draw_cast_shadow(char_turtle, 260)
        draw_cast_shadow(char_turtle, 300)
        
        if state == "walking":
            draw_cast_shadow(char_turtle, man_x)
            draw_cast_shadow(char_turtle, 100)
        elif state == "proposing":
            draw_cast_shadow(char_turtle, -50)
            draw_cast_shadow(char_turtle, 100)
        elif state == "accepted":
            if t_accept < 35:
                man_walk_x = -50 + (t_accept / 35.0) * 65.0
                woman_walk_x = 100 - (t_accept / 35.0) * 60.0
                draw_cast_shadow(char_turtle, man_walk_x)
                draw_cast_shadow(char_turtle, woman_walk_x)
            else:
                draw_cast_shadow(char_turtle, 15)
                draw_cast_shadow(char_turtle, 40)
        elif state == "rejected":
            sad_x = -50 - (t_reject - 25) * 3.0 if (frame - reject_frame) > 25 else -50
            draw_cast_shadow(char_turtle, sad_x)
            draw_cast_shadow(char_turtle, 100)

        chat_left = (not is_accepted) and (state != "rejected")
        chat_right = (not is_accepted) and (state != "rejected")
        
        dir1 = 1
        dir2 = -1 if chat_left else 1
        dir3 = 1
        dir4 = -1
        dir5 = 1 if chat_right else -1
        dir6 = -1
        
        draw_spectator_full(char_turtle, -310, frame, is_clapping=is_accepted, is_talking=chat_left, type="man", dir_x=dir1)
        draw_spectator_full(char_turtle, -270, frame, is_clapping=is_accepted, is_talking=chat_left, type="woman", dir_x=dir2)
        draw_spectator_full(char_turtle, -230, frame, is_clapping=is_accepted, is_talking=False, type="man", dir_x=dir3)
        
        draw_spectator_full(char_turtle, 220, frame, is_clapping=is_accepted, is_talking=False, type="woman", dir_x=dir4)
        draw_spectator_full(char_turtle, 260, frame, is_clapping=is_accepted, is_talking=chat_right, type="man", dir_x=dir5)
        draw_spectator_full(char_turtle, 300, frame, is_clapping=is_accepted, is_talking=chat_right, type="woman", dir_x=dir6)

        if state == "walking":
            t_sky = min(1.0, max(0.0, (man_x - -380) / 330.0))
            man_x += 4.5
            draw_man_full(char_turtle, man_x, frame, pose="walk", dir_x=1)
            draw_woman_full(char_turtle, 100, frame, pose="stand")
            
           
            if frame % 6 == 0:
                draw_dynamic_background(t_sky)
            
            if man_x >= -50:
                man_x = -50
                state = "proposing"
                propose_frame = frame
                speak_text("Will you marry me?", gender="male")
                draw_dynamic_background(1.0)  # Locked to full night sky
                
        elif state == "proposing":
            draw_man_full(char_turtle, -50, frame, pose="kneel", dir_x=1)
            draw_woman_full(char_turtle, 100, frame, pose="surprised")
            
           
            rx, ry = -26, get_ground_y(-50) + 50 - 20
            
            if dialogue_style == 0:
                ray_len = 5 + 3.5 * math.sin(frame * 0.35)
                heart_turtle.pencolor("#ffd700")
                heart_turtle.width(3)
                heart_turtle.penup()
                heart_turtle.goto(rx, ry + 4 - ray_len)
                heart_turtle.pendown()
                heart_turtle.goto(rx, ry + 4 + ray_len)
                heart_turtle.penup()
                heart_turtle.goto(rx - ray_len, ry + 4)
                heart_turtle.pendown()
                heart_turtle.goto(rx + ray_len, ry + 4)
                draw_circle(heart_turtle, rx, ry + 4, 6 + 2 * math.sin(frame * 0.3), "#00e5ff")
                draw_circle(heart_turtle, rx, ry + 4, 4, "#ffffff")
            elif dialogue_style == 1:
                update_dialogue_effects(heart_turtle, frame, 0)
            else:
                update_dialogue_effects(heart_turtle, frame, 1)
            
            # Speech bubble
            draw_speech_bubble(heart_turtle, -65, get_ground_y(-50)+50+40, w=140, h=30, text="Will you marry me?", tail_x=-50, tail_y=get_ground_y(-50)+50+12)
            
          
            prop_text = f"{man_name}: Will you marry me?"
            draw_typewriter_subtitle(text_turtle, prop_text, propose_frame, 25, -205, ("Georgia", 24, "bold"), "#ffffff", speed=3)

            if frame - propose_frame > len(prop_text) * 3:
                if (frame // 8) % 2 == 0:
                    write_shadow_text(text_turtle, "[Y] Accept   /   [N] Reject", 25, -245, ("Georgia", 14, "bold"), "#ff71ce")
                else:
                    write_shadow_text(text_turtle, "[Y] Accept   /   [N] Reject", 25, -245, ("Georgia", 14, "bold"), "#ffffff")
                
        elif state == "accepted":
            t_accept = frame - accept_frame
            
            if t_accept < 35:
                man_walk_x = -50 + (t_accept / 35.0) * 65.0   
                woman_walk_x = 100 - (t_accept / 35.0) * 60.0  
                draw_man_full(char_turtle, man_walk_x, frame, pose="walk", dir_x=1)
                draw_woman_full(char_turtle, woman_walk_x, frame, pose="stand")
                
                draw_speech_bubble(heart_turtle, woman_walk_x - 5, get_ground_y(woman_walk_x)+75+40, w=70, h=30, text="YES! ❤️", tail_x=woman_walk_x, tail_y=get_ground_y(woman_walk_x)+75+11)
            else:
                man_walk_x = 15
                woman_walk_x = 40
                draw_man_full(char_turtle, man_walk_x, frame, pose="kiss", dir_x=1)
                draw_woman_full(char_turtle, woman_walk_x, frame, pose="kiss")
                
                draw_speech_bubble(heart_turtle, 27, get_ground_y(27)+73+40, w=110, h=30, text="I love you! ❤️", tail_x=27, tail_y=get_ground_y(27)+73+10)
                
                kiss_h_pulse = 6 + 2 * math.sin(frame * 0.3)
                draw_heart_shape(heart_turtle, 27, get_ground_y(27) + 73, kiss_h_pulse, "#ff007f", heading=90)
            
            heart_pulse = 1.0 + 0.12 * math.sin(t_accept * 0.15)
            draw_heart_shape(heart_turtle, 25, -5, int(22 * heart_pulse), "#ff2a6d", heading=90)
            draw_heart_shape(heart_turtle, 25, -5, int(25 * heart_pulse), "#ff71ce", heading=90)
            draw_heart_shape(heart_turtle, 25, -5, int(22 * heart_pulse), "#ff2a6d", heading=90)
            
            for sx in [-310, -270, -230, 220, 260, 300]:
                s_dir = 1 if sx < 0 else -1
                x_clap = sx + 4 * s_dir + 3.5 * math.sin(frame * 1.5)
                draw_circle(heart_turtle, x_clap, get_ground_y(sx) + 75 - 20, 2.2, "#ffd700")
            
            update_fireworks(heart_turtle, frame)
            
            love_tier = "low"
            if love_meter >= 71:
                love_tier = "max"
                if frame % 10 == 0:
                    spawn_firework_rocket()
                star_turtle.penup()
                star_turtle.goto(25, -50)
                star_turtle.pencolor("#ffd700")
                star_turtle.write("💖 MAX LOVE! 💖", align="center", font=("Georgia", 16, "bold"))
            elif love_meter >= 31:
                love_tier = "medium"
                if frame % 3 == 0:
                    spawn_floating_heart()
            
            draw_typewriter_subtitle(text_turtle, f"{woman_name} said YES! ❤️", accept_frame, 25, -205, ("Georgia", 26, "bold"), "#ffde59", speed=3)
            if t_accept > 75:
                draw_typewriter_subtitle(text_turtle, f"Congratulations {man_name} & {woman_name}! 🎉", accept_frame + 75, 25, -245, ("Georgia", 14, "italic"), "#ffb7d5", speed=3)
            
            if frame % 4 == 0:
                spawn_floating_heart()
                
            for fh in floating_hearts[:]:
                fh["y"] += fh["speed_y"]
                fh["x"] += fh["speed_x"] + 1.2 * math.sin(frame * 0.05 + fh["phase"])
                if fh["y"] > 250:
                    floating_hearts.remove(fh)
                else:
                    draw_heart_shape(heart_turtle, fh["x"], fh["y"], fh["size"], fh["color"], heading=90)
                    
        elif state == "rejected":
            t_reject = frame - reject_frame
            draw_woman_full(char_turtle, 100, frame, pose="stand")
            
            # 1. Heart Crack Animation
            crack_offset = min(120, t_reject * 3.5)
            y_drop = t_reject * 2.5
            rot_crack = t_reject * 0.9
            heart_color = interpolate_color("#ff2a6d", "#546e7a", min(1.0, t_reject / 25.0))
            
            draw_heart_left(heart_turtle, 25 - crack_offset, -5 - y_drop, 22, heart_color, heading=90 + rot_crack)
            draw_heart_right(heart_turtle, 25 + crack_offset, -5 - y_drop, 22, heart_color, heading=90 - rot_crack)
            
            update_lightning(heart_turtle, bg_turtle, frame)
            
            if t_reject < 25:
                draw_speech_bubble(heart_turtle, -65, get_ground_y(-50)+50+40, w=110, h=30, text="Oh no... 💔", tail_x=-50, tail_y=get_ground_y(-50)+50+12)
            
           
            cloud_scale = min(1.0, t_reject / 20.0)
            cloud_color = "#37474f"
            r1, r2, r3 = int(24 * cloud_scale), int(32 * cloud_scale), int(24 * cloud_scale)
            if r2 > 0:
                draw_circle(heart_turtle, 0, 140, r1, cloud_color)
                draw_circle(heart_turtle, 25, 145, r2, cloud_color)
                draw_circle(heart_turtle, 50, 140, r3, cloud_color)
                
          
           
           
            sad_x = -50
            if t_reject > 25:
                sad_x = -50 - (t_reject - 25) * 3.0
                draw_man_full(char_turtle, sad_x, frame, pose="walk", dir_x=-1)
                
                y_head_walk = get_ground_y(sad_x) + 75 + 2.5 * abs(math.sin(frame * 0.4))
                if frame % 6 == 0:
                    teardrops.append({
                        "x": sad_x - 10,
                        "y": y_head_walk - 8,
                        "vx": -1.5,
                        "vy": -2.5
                    })
            else:
                draw_man_full(char_turtle, -50, frame, pose="kneel", dir_x=1)
                
            for td in teardrops[:]:
                td["y"] += td["vy"]
                td["x"] += td["vx"]
                if td["y"] < get_ground_y(td["x"]):
                    teardrops.remove(td)
                else:
                    draw_circle(heart_turtle, td["x"], td["y"], 2.2, "#00e5ff")
            
         
            if t_reject < 90:
                sad_cap = "Achha chalta hoon duao mein yaad rakhna..."
                sub_cap = f"{man_name} was friendzoned... 💔"
                phase_start = reject_frame
            elif t_reject < 180:
                sad_cap = "Mere zikr ka zubaan pe swaad rakhna..."
                sub_cap = f"Sending prayers for {man_name}..."
                phase_start = reject_frame + 90
            else:
                sad_cap = "Channa mereya mereya... O beliya..."
                sub_cap = "Better luck next time in code!"
                phase_start = reject_frame + 180
                
            draw_typewriter_subtitle(text_turtle, sad_cap, phase_start, 25, -205, ("Georgia", 18, "bold"), "#ffb7d5", speed=2)
            elapsed_phase = frame - phase_start
            if elapsed_phase > 45:
                draw_typewriter_subtitle(text_turtle, sub_cap, phase_start + 45, 25, -245, ("Georgia", 14, "italic"), "#90a4ae", speed=2)
            
        
        for d in step_dust[:]:
            d["x"] += d["vx"]
            d["y"] += d["vy"]
            d["vy"] -= 0.15 
            d["life"] -= 1
            if d["life"] <= 0:
                step_dust.remove(d)
            else:
                draw_circle(heart_turtle, d["x"], d["y"], 1.8, "#6d5c6f")
        
        screen.update()
        time.sleep(0.033)
        frame += 1

except (turtle.Terminator, Exception) as e:
    pass
