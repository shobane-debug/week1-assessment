from pathlib import Path
import sys
ROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from assessment import task1, file_tasks, task3
ROOT

task1()

file_tasks()

task3()

values = list(range(10_000))
%timeit [value * 2 for value in values]
