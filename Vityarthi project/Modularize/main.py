import datetime
from habit import Habit # type: ignore
from habit_tracker import HabitTracker # type: ignore

def main():
    tracker = HabitTracker()
    tracker.loadFromFile("habits.json")
    
    while True:
        print("\n=== Habit Tracker ===")
        print("1. Add New Habit")
        print("2. Log Today's Progress")
        print("3. Check Streaks")
        print("4. View Last Week Stats")
        print("5. Save & Exit")
        
        choice = input("\nWhat would you like to do? ")
        
        if choice == "1":
            habitName = input("Enter habit name: ")
            habitGoal = input("What's your goal? ")
            newHabit = Habit(habitName, habitGoal)
            tracker.addHabit(newHabit)
            print("Great! Habit added successfully.")
            
        elif choice == "2":
            habitName = input("Which habit? ")
            if habitName not in tracker.habits:
                print("Hmm, I don't see that habit. Maybe add it first?")
                continue
            
            didIt = input("Did you complete it today? (y/n): ")
            if didIt.lower() == "y":
                tracker.logHabit(habitName, datetime.date.today(), True)
                print("Awesome! Logged as done.")
            else:
                tracker.logHabit(habitName, datetime.date.today(), False)
                print("No worries, there's always tomorrow!")
            
        elif choice == "3":
            if len(tracker.habits) == 0:
                print("You haven't added any habits yet.")
            else:
                print("\nYour current streaks:")
                for habitName in tracker.habits:
                    streak = tracker.getStreak(habitName)
                    print(f"  {habitName}: {streak} days in a row")
                    
        elif choice == "4":
            if len(tracker.habits) == 0:
                print("No habits to show stats for.")
            else:
                print("\nLast 7 days completion:")
                for habitName in tracker.habits:
                    pct = tracker.getCompletionPercent(habitName, 7)
                    print(f"  {habitName}: {pct:.1f}% completed")
                    
        elif choice == "5":
            tracker.saveToFile("habits.json")
            print("All saved! See you next time.")
            break
            
        else:
            print("Sorry, that's not a valid option. Try again!")

if __name__ == "__main__":
    main()
