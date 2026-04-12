try:
    from tasks.easy import EasyTask
    from tasks.medium import MediumTask
    from tasks.hard import HardTask
except ImportError:
    from easy import EasyTask
    from medium import MediumTask
    from hard import HardTask

TASKS = {
    "easy": EasyTask,
    "medium": MediumTask,
    "hard": HardTask
}