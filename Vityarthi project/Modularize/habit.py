class Habit:
    def __init__(self, name, target):
        self.name = name
        self.target = target
    
    def __str__(self):
        return f"Habit: {self.name} - Goal: {self.target}"
