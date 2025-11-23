import datetime
import json

class Habit:
    def __init__(self, name, target):
        self.name = name
        self.target = target
    
    def __str__(self):
        return f"Habit: {self.name} - Goal: {self.target}"

class HabitTracker:
    def __init__(self):
        self.habits = {}
        self.logs = {}
    
    def addHabit(self, habit):
        self.habits[habit.name] = habit
        if habit.name not in self.logs:
            self.logs[habit.name] = {}
    
    def logHabit(self, name, date, done):
        if name in self.logs:
            self.logs[name][date.isoformat()] = done
    
    def getStreak(self, name):
        today = datetime.date.today()
        streak = 0
        logs = self.logs.get(name, {})
        currentDay = today
        while logs.get(currentDay.isoformat(), False):
            streak += 1
            currentDay -= datetime.timedelta(days=1)
        return streak
    
    def getCompletionPercent(self, name, numDays):
        today = datetime.date.today()
        logs = self.logs.get(name, {})
        done = 0
        for i in range(numDays):
            checkDay = today - datetime.timedelta(days=i)
            if logs.get(checkDay.isoformat(), False):
                done += 1
        if numDays > 0:
            return (done / numDays) * 100
        else:
            return 0
    
    def saveToFile(self, filename):
        habitData = {}
        for name, habit in self.habits.items():
            habitData[name] = habit.target
        
        saveData = {"habits": habitData, "logs": self.logs}
        
        f = open(filename, "w")
        json.dump(saveData, f)
        f.close()
    
    def loadFromFile(self, filename):
        try:
            f = open(filename, "r")
            data = json.load(f)
            f.close()
            
            for name, target in data["habits"].items():
                self.habits[name] = Habit(name, target)
            self.logs = data["logs"]
        except:
            pass

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