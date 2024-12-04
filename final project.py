import json
from tkinter import *
from tkinter import simpledialog ,messagebox
from tkinter import ttk
from datetime import datetime
import webbrowser
from ai import Geminiai
def ai_ask():
    api_key = "AIzaSyDQqG1vQHVGs3vWJZ_GZ-PAwxN-TDMDeXU"
    assistant = Geminiai(api_key)
    q=simpledialog.askstring(title="ask ai",prompt="enter your question")
    ans = assistant.ask_question(q)
    messagebox.showinfo(title="AI says",message=ans)
def main_app():
    window.destroy()
    back_colour = "white"
    text_colour = "black"
    button_colour = "#1E90FF"
    button2_colour = "purple"

    def open_google_maps(location, landmark):
        q = f"{location} {landmark}"
        webbrowser.open(f"https://www.google.com/maps?q={q}")

    def save_reminder(event):
        try:
            with open("reminders.json", "r") as file:
                reminders = json.load(file)
        except FileNotFoundError:
            reminders = []
        if event in reminders:
            messagebox.showinfo("Reminder", "This event is already in your reminders!")
            return
        reminders.append(event)
        with open("reminders.json", "w") as file:
            json.dump(reminders, file, indent=4)
        messagebox.showinfo("Reminder", "Event added to your reminders!")

    def load_reminders():
        try:
            with open("reminders.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def delete_reminder(event):
        reminders = load_reminders()
        reminders = [r for r in reminders if r != event]
        with open("reminders.json", "w") as file:
            json.dump(reminders, file, indent=4)
        messagebox.showinfo("Reminder", "Event deleted from your reminders!")

    def show_reminders():
        reminders_window = Tk()
        reminders_window.title("My Events")
        reminders_window.geometry("500x500")
        reminders_window.config(bg=back_colour)
        reminders = load_reminders()
        Label(reminders_window, text="My Events", font=("Arial", 18, "bold"), bg=back_colour, fg=text_colour).pack(
            pady=10)
        if not reminders:
            Label(reminders_window, text="No reminders set.", font=("Arial", 12), bg=back_colour).pack(pady=20)
        else:
            for event in reminders:
                frame = Frame(reminders_window, bg=back_colour, relief="solid", padx=10, pady=5)
                frame.pack(pady=5, fill=X)
                Label(frame, text=f"Title: {event['title']}\nDate: {event['date']}\nLocation: {event['location']}\n"
                                  f"Landmark: {event.get('landmark', 'N/A')}",
                      font=("Arial", 12), bg=back_colour, fg="#333").pack(side=LEFT, padx=10)
                Button(frame, text="Delete", font=("Arial", 10), bg=button_colour, fg="white",
                       command=lambda e=event: [delete_reminder(e), reminders_window.destroy(), show_reminders()]).pack(
                    side=RIGHT, padx=5)
        reminders_window.mainloop()

    def add_event():
        add_event_window = Tk()
        add_event_window.title("Add Event")
        add_event_window.geometry("450x600")
        add_event_window.config(bg="white")
        Label(add_event_window, text="Add Event Details", font=("Arial", 18, "bold"), bg="white", fg="#333").place(x=40,
                                                                                                                   y=10)

        def save_event():
            t = title.get()
            d = date.get()
            l = location.get()
            lm = landmark.get()
            dec = description.get()
            pho = phone.get()
            p = price.get()
            if t == "" or t == "title" or d == "" or d == "date" or l == "" or l == "location" or lm == "" or lm == "landmark" \
                    or dec == "" or dec == "description" or pho == "" or pho == "phone" or p == "" or p == "price":
                messagebox.showerror(title="ERROR", message="One of the parameters is empty")
            else:
                q = messagebox.askyesno(title="Save", message="Do you want to save this information?")
                if q:
                    eventdata = {
                        "title": t,
                        "date": d,
                        "location": l,
                        "landmark": lm,
                        "price": p,
                        "phone": pho,
                        "description": dec
                    }
                    try:
                        with open("events.json", "r") as file:
                            data = json.load(file)
                    except FileNotFoundError:
                        data = []
                    data.append(eventdata)
                    with open("events.json", "w") as file:
                        json.dump(data, file, indent=4)
                    messagebox.showinfo(title="SAVED", message="Event details have been saved successfully!")

        def on_entry(e, entry, placeholder):
            if entry.get() == placeholder:
                entry.delete(0, "end")

        def on_exit(e, entry, placeholder):
            if entry.get() == "":
                entry.insert(0, placeholder)

        placeholders = [
            ("title", 60), ("date (DD/MM/YYYY)", 120), ("location", 180), ("landmark", 240),
            ("price", 300), ("description", 420), ("phone", 360)
        ]
        entries = {}
        for text, y in placeholders:
            entry = Entry(add_event_window, width=30, highlightthickness=0, bg="white", border=0, font=("Arial", 12))
            entry.place(x=40, y=y)
            entry.insert(0, text)
            entry.bind("<FocusIn>", lambda e, ent=entry, ph=text: on_entry(e, ent, ph))
            entry.bind("<FocusOut>", lambda e, ent=entry, ph=text: on_exit(e, ent, ph))
            entries[text] = entry
            Frame(add_event_window, width=300, height=2, bg="black").place(x=40, y=y + 30)

        title, date, location, landmark, price, description, phone = entries.values()
        Button(add_event_window, text="Save Event", width=25, bg=button2_colour, fg="white",
               font=("Arial", 12, "bold"), command=save_event).place(x=40, y=520)
        add_event_window.mainloop()

    def load_events():
        try:
            with open("events.json", "r") as file:
                data = json.load(file)
            today = datetime.now().date()
            data = [
                event for event in data
                if datetime.strptime(event["date"], "%d/%m/%Y").date() >= today
            ]
            data.sort(key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"))
            return data
        except FileNotFoundError:
            return []
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return []

    def display_events(events, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        for event in events:
            frame_event = Frame(frame, bg=back_colour, relief="solid", padx=10, pady=5)
            frame_event.pack(pady=5, fill=X)
            # Display event details including landmark
            Label(frame_event, text=f"Title: {event['title']}\nDate: {event['date']}\nLocation: {event['location']}\n"
                                    f"Landmark: {event.get('landmark', 'N/A')}",
                  font=("Arial", 12), bg=back_colour, fg=text_colour).pack(side=LEFT, padx=10)
            Button(frame_event, text="Set Reminder", font=("Arial", 10), bg=back_colour, fg=text_colour,
                   command=lambda e=event: save_reminder(e)).pack(side=RIGHT, padx=5)
            Button(frame_event, text="Details", font=("Arial", 10), bg=button_colour, fg="white",
                   command=lambda e=event: messagebox.showinfo("Event Details",
                                                               f"Title: {e['title']}\nDate: {e['date']}\nLocation: {e['location']}\n"
                                                               f"Landmark: {e.get('landmark', 'N/A')}\nPrice: {e['price']}\n"
                                                               f"Phone: {e['phone']}\nDescription: {e['description']}")).pack(
                side=RIGHT, padx=5)
            Button(frame_event, text="locate", font=("Arial", 10), bg="red", fg="white",
                   command=lambda e=event: open_google_maps(e["location"], e["landmark"])).pack(side=RIGHT, padx=5)

    def animate_label_slide(label, text, index=0):
        """Animate the label by sliding in the text one character at a time."""
        if index <= len(text):
            label.config(text=text[:index])
            label.after(100, animate_label_slide, label, text, index + 1)  # Add one character every 100ms

    def home_page():
        app = Tk()
        app.title("Event Finder App")
        app.geometry("900x600")
        app.config(bg=back_colour)

        # Modern, clean title with sliding text animation
        app_name = Label(app, text="", font=("Helvetica", 28, "bold"), bg=back_colour, fg=text_colour)
        app_name.pack(pady=10)

        # Start sliding animation for the title
        animate_label_slide(app_name, "EVENT FINDER")

        # Sidebar setup
        sidebar = Frame(app, bg=back_colour, width=250)
        sidebar.pack(side=LEFT, fill=Y)

        # city_label = Label(sidebar, text="Select City", font=("Helvetica", 14), bg="#2D3748", fg="white")
        # city_label.pack(pady=10)

        cities = ["All cities", "New Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
        city_var = StringVar()
        city_dropdown = ttk.Combobox(app, textvariable=city_var, values=cities, font=("Helvetica", 12))
        city_dropdown.set("All cities")
        city_dropdown.place(y=70, x=20)

        search_btn = Button(app, text="Search Events", font=("Helvetica", 8), bg=back_colour, fg="black",
                            command=lambda: display_events(
                                [event for event in load_events() if
                                 city_var.get() == "All cities" or event["location"] == city_var.get()],
                                content_frame))
        search_btn.place(y=70, x=230)

        add_event_btn = Button(app, text="Add Event", font=("Helvetica", 8), bg=button_colour, fg="white",
                               command=add_event)
        add_event_btn.place(x=725, y=70)

        reminders_btn = Button(app, text="My Events", font=("Helvetica", 8), bg=button2_colour, fg="white",
                               command=show_reminders)
        reminders_btn.place(y=70, x=800)
        aiask=Button(app,text="AI",width=5,font=("Helvetica", 8), bg="red", fg="white",command=ai_ask)
        aiask.place(x=800,y=550)

        content_frame = Frame(app, bg=back_colour, height=450, width=450)
        content_frame.place(x=20 + 50 + 100 + 20, y=110)

        display_events(load_events(), content_frame)
        app.mainloop()

    home_page()


bgcolour="white"
window=Tk()
window.title("sig in/sign up")
window.geometry("925x500+300+200")
window.config(bg=bgcolour)
img=PhotoImage(file="compressed_1733225882750.png")
Label(window,image=img,bg=bgcolour).place(x=10+30,y=50)
frame=Frame(window,width=350,height=390,bg="white")
frame.place(x=480,y=50)
heading=Label(frame,text="Sign up",fg="#57a1f8",bg=bgcolour,font=("Microsoft Yahei UI Light",23,"bold"))
heading.place(x=100,y=5)
def app():
    window.destroy()
    app=Tk()
    app.title("welcome")
    app.geometry("925x500+300+200")
    app.config(bg=bgcolour)
    Label(app,text="WELCOME",fg="#57a1f8",bg=bgcolour,font=("Microsoft Yahei UI Light",23,"bold")).place(x=20,y=100)
    app.mainloop()
def sign_in():
    username=user.get()
    password=password1.get()
    if username=="" or username=="username":
        messagebox.showerror(title="Error",message="Enter your username")
        return
    if password=="" or password=="password":
        messagebox.showerror(title="Error",message="Enter your password")
        return
    try:
        with open("data.json","r") as file:
            users=json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error",message="username not found\nSign in and try again")
    for u in users:
        if u["username"]==username:
            if u["password"]==password:
                messagebox.showinfo(title="successful",message=f"welcome back {username}")
                a=main_app()
                return a
                #actual project from here
            else:
                messagebox.showerror(title="error",message="incorrect password\ntry again")
                return

    messagebox.showerror(title="Error", message="username not found\nSign in and try again")
def sign_up():
    username=user.get()
    password=password1.get()
    conform_password=cpassword.get()
    if password==conform_password and username!="username":
        userdata={"username":username,"password":password}
        try:
            with open("data.json","r") as file:
                data=json.load(file)
        except FileNotFoundError:
            data=[]
        data.append(userdata)
        with open("data.json","w") as file:
            json.dump(data,file,indent=4)
        messagebox.showinfo(title="WELCOME",message="Sign up successful")
        login_o()
    elif password!=conform_password:
        messagebox.showerror(title="Error",message="The passwords do not match")
    elif username=="username":
        messagebox.showerror(title="Error",message="username can't be empty")
def login_o():
    heading.config(text="Welcome back")
    cpassword.destroy()
    login_b.destroy()
    text1.destroy()
    f1.destroy()
    cig=Button(frame,text="Sign In",bg="white",width=40,command=sign_in)
    cig.place(x=25,y=257)
def on_entry(e):
    if user.get()=="username":
        user.delete(0,"end")
def on_exit(e):
    if user.get()=="":
        user.insert(0,"username")
user=Entry(frame,width=70,highlightthickness=0,bg=bgcolour,border=0)
user.place(x=30,y=80)
f=Frame(frame,width=420,height=2,bg="black")
f.place(x=25,y=107)
user.insert(0, "username")
user.bind("<FocusIn>",on_entry)
user.bind("<FocusOut>",on_exit)

def on_entry(e):
    if password1.get()=="password":
        password1.delete(0,"end")
def on_exit(e):
    if password1.get()=="":
        password1.insert(0,"password")
password1=Entry(frame,width=70,highlightthickness=0,bg=bgcolour,border=0)
password1.place(x=30,y=80+50)
f=Frame(frame,width=420,height=2,bg="black")
f.place(x=25,y=107+50)
password1.insert(0, "password")
password1.bind("<FocusIn>",on_entry)
password1.bind("<FocusOut>",on_exit)


def on_entry(e):
    if cpassword.get()=="conform password":
        cpassword.delete(0,"end")
def on_exit(e):
    if cpassword.get()=="":
        cpassword.insert(0,"conform password")
cpassword=Entry(frame,width=70,highlightthickness=0,bg=bgcolour,border=0)
cpassword.place(x=30,y=80+50+50)
f1=Frame(frame,width=420,height=2,bg="black")
f1.place(x=25,y=107+50+50)
cpassword.insert(0, "conform password")
cpassword.bind("<FocusIn>",on_entry)
cpassword.bind("<FocusOut>",on_exit)

login=Button(frame,text="Sign Up",bg="white",width=40,command=sign_up)
login.place(x=25,y=257)
#--------------------------------------------
text1=Label(frame,text="Already have an account?",bg=bgcolour)
text1.place(x=25,y=257+20+20)
#-----------------------
login_b=Button(frame,text="login",bg=bgcolour,fg="#57a1f8",border=0,highlightthickness=0,command=login_o)
login_b.place(x=100+50+20,y=257+20+20)
window.mainloop()
