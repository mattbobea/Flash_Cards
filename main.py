import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
french_word = ""
english_word = ""
new_word_set = {}
# ---------------------------- data pull------------------------------- #
try:
    word_data = pandas.read_csv(r"words_to_learn.csv")
except FileNotFoundError:
    word_data = pandas.read_csv(r"words.csv")
word_data = word_data.to_dict(orient="records")

# ---------------------------- UI SETUP ------------------------------- #
# window
window = Tk()
window.title("Github.com/mattbobea")
window.config(width=200, height=200, padx=50, pady=40, bg=BACKGROUND_COLOR)
# card background
canvas = Canvas(width=800, height=525, highlightthickness=0)
card_front = PhotoImage(file="card_front.png")
card_back = PhotoImage(file="card_back.png")
card_front_image = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=2)
# Top text
# ---------------------------- Timer ------------------------------- #
clock = canvas.create_text(100, 50, text="00:00", font=("Arial", 34, "bold"))


def timer(count):
    if count >= 0:
        canvas.itemconfig(clock, text=f"00.0{count}")
        window.after(1000, timer, count - 1)
    else:
        flip()


timer(5)


# selects a random set
def generate_word():
    global word_data, english_word, french_word, new_word_set
    new_word_set = random.choice(word_data)
    french_word = new_word_set["French"]
    english_word = new_word_set["English"]
    canvas.itemconfig(word_text, text=french_word, fill="black")
    canvas.itemconfig(language_text, text="Chinese", fill="black")
    canvas.itemconfig(clock, text="moo")
    timer(5)


def check_mark():
    # removes learned word from being reselected
    word_data.remove(new_word_set)
    # 1) converts to DF.  2) saves to CSV
    data = pandas.DataFrame(word_data)
    data.to_csv("words_to_learn.csv", index=False)
    generate_word()


language_text = canvas.create_text(400, 150, text="Chinese", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 300, text=french_word, font=("Arial", 60, "bold"))
generate_word()


def flip():
    canvas.itemconfig(card_front_image, image=card_back)
    canvas.itemconfig(word_text, text=english_word, fill="white")
    canvas.itemconfig(language_text, text="English", fill="white")


# x button
wrong_image = PhotoImage(file="wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=generate_word)
wrong_button.grid(row=1, column=0)
# check button
right_image = PhotoImage(file="right.png")
right_button = Button(image=right_image, highlightthickness=0, command=check_mark)
right_button.grid(row=1, column=1)

window.mainloop()
