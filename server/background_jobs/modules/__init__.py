import sys, os
directory = os.path.abspath(__file__).split("background_jobs")
parent_module  = directory[0] + "background_jobs"
sys.path.append(directory[0] + "background_jobs")