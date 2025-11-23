import datetime
import json
from habit import Habit

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
        
        with open(filename, "w") as f:
            json.dump(saveData, f)
    
    def loadFromFile(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            
            for name, target in data["habits"].items():
                self.habits[name] = Habit(name, target)
            self.logs = data["logs"]
        except:
            pass
