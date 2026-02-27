import tkinter as tk
from PIL import Image, ImageTk
import random
import os

# -----------------------------
# Root window
# -----------------------------
root = tk.Tk()
root.title("🌱 Virtual Plant Companion")
root.geometry("450x800")
root.configure(bg="#FDF6F0")
root.resizable(False, False)
screens = {}  # <- define this at the very top, before any use of screens
score = [0]
#Controls
mini_game_active = False
spawn_job = None

# -----------------------------
# Plant Stats
# -----------------------------
plant_stats = {
    "water": 5,
    "sunlight": 5,
    "happiness": 5,
    "growth_stage": "Seed",
    "money": 10
}

# -----------------------------
# Helper Functions
# -----------------------------
def check_growth():
    if plant_stats["water"] > 7 and plant_stats["sunlight"] > 7 and plant_stats["happiness"] > 5:
        plant_stats["growth_stage"] = "Flower"
    elif plant_stats["water"] < 3 or plant_stats["sunlight"] < 3:
        plant_stats["growth_stage"] = "Wilting"
    else:
        plant_stats["growth_stage"] = "Sprout"

def update_plant_image():
    if money_label.winfo_exists():
        money_label.config(text=f"💰 {plant_stats['money']}")
        stage = plant_stats["growth_stage"]
        img_path = os.path.join("images", f"{stage}.png")
        try:
            img = Image.open(img_path).resize((200,200))
            photo = ImageTk.PhotoImage(img)
            plant_label.config(image=photo, text="")
            plant_label.image = photo
        except:
            plant_label.config(text=stage, font=("Arial", 20))
        stats_label.config(text=f"💧{plant_stats['water']}  ☀{plant_stats['sunlight']}  🙂{plant_stats['happiness']}")
        money_label.config(text=f"💰 {plant_stats['money']}")
    else:
        print("Widget gone, skipping update.")


# In your clear_screen function:
def clear_screen():
    global decay_loop
    if decay_loop:
        main_screen.after_cancel(decay_loop) # This stops the background timer
    for w in main_widgets:
        w.destroy()
    main_widgets.clear()
# -----------------------------
# MAIN SCREEN
# -----------------------------
main_screen = tk.Frame(root, bg="#FDF6F0")
main_screen.pack(fill="both", expand=True)

# Store all main screen widgets to hide/show them easily
main_widgets = []

# Money bar
top_frame = tk.Frame(main_screen, bg="#FFD6E0", height=60)
top_frame.pack(fill="x", side= "top")
money_label = tk.Label(top_frame, text=f"💰 {plant_stats['money']}", font=("Helvetica", 18, "bold"), bg="#FFD6E0", fg="#5A3E36")
money_label.pack(side="left", pady=10)
main_widgets.extend([top_frame, money_label])
# Plant display
plant_frame = tk.Frame(main_screen, bg="#FDF6F0")
plant_frame.pack( side="top")
plant_label = tk.Label(plant_frame,bg="#FDF6F0",text="🌱 Plant", font=("Arial",20))
plant_label.pack(pady=20)

main_widgets.extend([plant_frame])
# Buttons frame
button_frame = tk.Frame(main_screen, bg="#FDF6F0")
button_frame.pack(pady=10)
main_widgets.append(button_frame)
# Stats label
stats_frame = tk.Frame(main_screen, bg="#FFFAE3")
stats_frame.pack(pady=5, fill="x", side = "top")
stats_label = tk.Label(stats_frame, text="", font=("Arial",12,"bold"), bg="#FFFAE3")
stats_label.pack()
main_widgets.extend([stats_frame, stats_label])
# Event label
event_label = tk.Label(main_screen, text="🌼 Welcome!", font=("Arial",12), bg="#FDF6F0")
event_label.pack(pady=5, side = "top")
main_widgets.append(event_label)

# --- Mini-game frame ---
mini_game_frame = tk.Frame(root, bg="#E8F5E9")
# Do NOT pack yet; pack when mini-game starts

back_btn = tk.Button(mini_game_frame, text="⬅ Back")
back_btn.pack(pady=10)
#-----------------------------------------------------------------

def create_button(text, color, command):
    return tk.Button(button_frame, text=text, font=("Helvetica",12,"bold"),
                     bg=color, fg="white", activebackground=color, relief="raised", bd=3, padx=15, pady=8,
                     command=command)

COST_WATER, COST_SUN, COST_MOOD = 2, 2, 1

def water_plant():
    if plant_stats["money"] >= COST_WATER:
        plant_stats["money"] -= COST_WATER
        plant_stats["water"] += 2
        check_growth()
        update_plant_image()
    else:
        event_label.config(text="💰 Not enough money to water!")

def give_sunlight():
    if plant_stats["money"] >= COST_SUN:
        plant_stats["money"] -= COST_SUN
        plant_stats["sunlight"] += 2
        check_growth()
        update_plant_image()
    else:
        event_label.config(text="💰 Not enough money for sunlight!")

def improve_mood():
    if plant_stats["money"] >= COST_MOOD:
        plant_stats["money"] -= COST_MOOD
        plant_stats["happiness"] += 2
        check_growth()
        update_plant_image()
    else:
        event_label.config(text="💰 Not enough money to improve mood!")

water_btn = create_button("💧 Water","#A0E7E5",water_plant)
sun_btn = create_button("🌞 Sun","#FFAEBC",give_sunlight)
mood_btn = create_button("😊 Mood","#B4F8C8",improve_mood)
water_btn.grid(row=0,column=0,padx=5,pady=5)
sun_btn.grid(row=0,column=1,padx=5,pady=5)
mood_btn.grid(row=1,column=0,columnspan=2,pady=5)
main_widgets.extend([water_btn, sun_btn, mood_btn])

# Shop buttons
fertilizer_btn = create_button("🌸 Fertilizer (10💰)","#CDB4DB",lambda:buy_item("fertilizer"))
pest_btn = create_button("🧪 Pesticide (8💰)","#FFB6B9",lambda:buy_item("pesticide"))
fertilizer_btn.grid_remove()
pest_btn.grid_remove()
shop_open=False

def toggle_shop():
    global shop_open
    if not shop_open:
        fertilizer_btn.grid()
        pest_btn.grid()
        shop_open=True
    else:
        fertilizer_btn.grid_remove()
        pest_btn.grid_remove()
        shop_open=False

shop_btn = tk.Button(main_screen, text="🛒 Shop", font=("Helvetica",14,"bold"),
                     bg="#FFDAC1", fg="#5A3E36", relief="raised", command=toggle_shop)
shop_btn.pack(pady=15)
main_widgets.append(shop_btn)
main_widgets.extend([fertilizer_btn, pest_btn])

def buy_item(item):
    if item=="fertilizer" and plant_stats["money"]>=10:
        plant_stats["money"]-=10
        plant_stats["water"]+=3; plant_stats["sunlight"]+=3; plant_stats["happiness"]+=3
        event_label.config(text="🌟 Fertilizer applied!")
    elif item=="pesticide" and plant_stats["money"]>=8:
        plant_stats["money"]-=8
        event_label.config(text="🐛 Bugs removed!")
    else:
        event_label.config(text="💰 Not enough money!")
    update_plant_image()

# -----------------------------
# MINI-GAME SCREEN
# -----------------------------
mini_game_screen = tk.Frame(root, bg="#E8F5E9")
mini_game_screen.place(relwidth=1, relheight=1)  # fullscreen over main screen
screens["mini_game"] = mini_game_screen
mini_game_screen.lower()  # hide initially

mini_score_label = tk.Label(mini_game_screen,text="",font=("Arial",18),bg="#E8F5E9")
mini_score_label.pack(pady=10)

game_grid = tk.Frame(mini_game_screen, bg="#E8F5E9")
game_grid.pack(expand=True, fill = "both")
for i in range(3):
    game_grid.rowconfigure(i, weight=1)
    game_grid.columnconfigure(i, weight=1)

back_btn = tk.Button(mini_game_screen,text="⬅ Back",font=("Helvetica",14,"bold"),
                     bg="#FFDAC1", fg="#5A3E36", relief="raised")
back_btn.pack(pady=10)
back_btn.pack_forget()  # hide back button initially

# Mini-game logic
mini_game_active = False
spawn_job = None

def start_mini_game():
    global mini_game_active, spawn_job
    score[0] = 0
    if mini_game_active:
        return  # Prevent double-starting
    
    mini_game_active = True

    # 1. HIDE the main UI instead of destroying it
    # This keeps the widgets "alive" so background loops don't crash
    main_screen.pack_forget()

    # 2. SHOW the mini-game UI
    mini_game_screen.pack(fill="both", expand=True)
    mini_game_screen.lift()
    back_btn.pack(pady=10)    
    # 3. Reset the game state
    mini_score_label.config(text="Score: 0")
    for widget in game_grid.winfo_children():
        widget.destroy() # Clear old plants from previous games
    spawn_plant()
    mini_game_screen.after(10000, end_mini_game)

def spawn_plant():
    global spawn_job
    for widget in game_grid.winfo_children(): widget.destroy()

    if not mini_game_active: return

    row, col = random.randint(0, 2), random.randint(0, 2)
    plant_btn = tk.Button(game_grid, text="🌿", font=("Arial", 30),
                            command=lambda: click_plant(plant_btn))
    plant_btn.grid(row=row, column=col, padx=20, pady=20,)

        # Move the plant automatically if not clicked in 1 second
    spawn_job = mini_game_screen.after(3000, spawn_plant) 
    print(row, col)

def click_plant(plant_btn):
    # 1. Update Stats
    score[0] += 1
    plant_stats["money"] += 1
    
    # 2. Update UI
    if money_label.winfo_exists():
        money_label.config(text=f"💰 {plant_stats['money']}")
    mini_score_label.config(text=f"Score: {score[0]}")

    # 3. Cancel the "missed plant" timer so it doesn't spawn two plants
    if spawn_job:
        mini_game_screen.after_cancel(spawn_job)

    # 4. Remove the current plant and SPAWN A NEW ONE
    plant_btn.destroy()
    spawn_plant() # <--- This creates the "looping" effect
    
    # Set a timer to end the game automatically after 10 seconds
def end_mini_game():
    global mini_game_active, spawn_job
    mini_game_active = False

    if spawn_job:
        root.after_cancel(spawn_job)
        spawn_job = None 
    mini_game_screen.pack_forget()     # Hide the game
    main_screen.pack(fill="both", expand=True)  # Show the plant
    
    update_plant_image()
    event_label.config(text="Welcome back to your garden!")
back_btn.config(command=lambda: mini_game_screen.after_cancel(spawn_job) if spawn_job else None or
                mini_game_screen.after(1, lambda: show_main_from_mini_game()))

def show_main_from_mini_game():
    global mini_game_active, spawn_job
    mini_game_active=False
    if spawn_job:
        mini_game_screen.after_cancel(spawn_job)
        spawn_job=None
    for w in main_widgets:
        if hasattr(w,"pack_info") and w.pack_info():
            w.pack()
        else:
            try: w.grid()
            except: pass
    back_btn.pack_forget()
    mini_game_screen.lower()

# Mini-game button on main screen
mini_game_btn = tk.Button(top_frame,text="🎯 Mini-Game",font=("Helvetica",10,"bold"),
                          bg="#B9FBC0", fg="#2C6E49", relief="raised",
                          command=start_mini_game)
mini_game_btn.pack(side="left", padx=10,pady=5)
main_widgets.append(mini_game_btn)
#DECAY
def decay_stats():
    plant_stats["water"] = max(0, plant_stats["water"] - 1)
    plant_stats["sunlight"] = max(0, plant_stats["sunlight"] - 1)
    plant_stats["happiness"] = max(0, plant_stats["happiness"] - 1)
    check_growth()
    update_plant_image()
    root.after(15000, decay_stats)
decay_loop = main_screen.after(5000, decay_stats)
back_btn.config(command=end_mini_game)
mini_game_btn.config(command=start_mini_game)
# -----------------------------
# START
# -----------------------------
update_plant_image()
decay_stats()
root.mainloop()
# Update the back button to trigger the cleanup function
