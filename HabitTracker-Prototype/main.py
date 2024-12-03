# Import necessary tools
import matplotlib.pyplot as plt  # For making graphs
from datetime import datetime, timedelta  # For handling dates

# A dictionary to store your habits and their completion dates
habits = {}


# Make sure the habits file exists
def init_file():
    try:
        with open("habits.txt", "x"):  # 'x' creates the file if it doesn't exist
            pass
    except FileExistsError:
        pass  # If the file already exists, we do nothing


# Load habits and their data from the file
def load_habits():
    with open("habits.txt", "r") as file:
        for line in file:
            habit, dates = line.strip().split(" | ")
            habits[habit] = dates.split(", ") if dates else []  # Split dates into a list


# Save current habits and their data to the file
def save_habits():
    with open("habits.txt", "w") as file:
        for habit, dates in habits.items():
            file.write(f"{habit} | {', '.join(dates)}\n")


# Add a new habit to the tracker
def add_habit():
    habit = input("What habit would you like to track? ")
    if habit not in habits:
        habits[habit] = []  # Start with an empty list of dates
        save_habits()
        print(f'Great! You are now tracking "{habit}".')
    else:
        print(f'You are already tracking "{habit}".')


# Mark a habit as completed
def complete_habit(habit, date_str=None):
    if habit not in habits:
        print(f'Habit "{habit}" isn’t being tracked yet.')
        return

    if not date_str:  # Ask for a date if not provided
        date_str = input("Enter the date (YYYY-MM-DD, or leave blank for today): ")
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')  # Default to today's date

    try:
        datetime.strptime(date_str, '%Y-%m-%d')  # Check if the date is valid
    except ValueError:
        print("The date format is incorrect. Try YYYY-MM-DD.")
        return

    if date_str not in habits[habit]:  # Avoid duplicate entries
        habits[habit].append(date_str)
        save_habits()
        print(f'You completed "{habit}" on {date_str}. Well done!')
    else:
        print(f'You already marked "{habit}" as done on {date_str}.')


# Show all tracked habits and their progress
def view_habits():
    if not habits:
        print("You haven’t started tracking any habits yet.")
    else:
        print("\nHere are your habits:")
        for habit, dates in habits.items():
            print(f"- {habit}: {', '.join(dates) if dates else 'No progress yet'}")


# Create a simple progress graph
def plot_habit(habit_name):
    if habit_name not in habits:
        print(f'Habit "{habit_name}" isn’t being tracked.')
        return

    dates = [datetime.strptime(date, '%Y-%m-%d') for date in habits[habit_name]]
    if not dates:
        print(f'No progress data for "{habit_name}".')
        return

    # Prepare cumulative data for plotting
    dates.sort()
    start_date = dates[0]
    end_date = dates[-1]
    date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    cumulative = 0
    progress = []
    for date in date_range:
        if date in dates:
            cumulative += 1
        progress.append(cumulative)

    # Convert datetime objects to date strings for plotting
    date_labels = [date.strftime('%Y-%m-%d') for date in date_range]

    # Plot the graph
    plt.figure(figsize=(8, 4))
    plt.plot(date_labels, progress, label=habit_name)
    plt.xlabel('Date')
    plt.ylabel('Total Completions')
    plt.title(f'Progress for "{habit_name}"')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()


# Main menu for interacting with the habit tracker
def main_menu():
    init_file()
    load_habits()

    while True:
        print("\n--- Your Habit Tracker ---")
        print("1. Add a new habit")
        print("2. Mark a habit as done")
        print("3. View your habits")
        print("4. See progress on a habit")
        print("5. Exit")

        choice = input("What would you like to do? ")

        if choice == '1':
            add_habit()
        elif choice == '2':
            habit = input("Which habit did you complete? ")
            complete_habit(habit)
        elif choice == '3':
            view_habits()
        elif choice == '4':
            habit = input("Which habit’s progress do you want to see? ")
            plot_habit(habit)
        elif choice == '5':
            print("Goodbye! Keep building those habits!")
            break
        else:
            print("That’s not a valid option. Try again.")


# Start the program
main_menu()
