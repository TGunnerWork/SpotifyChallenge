import subprocess

# Consolidates JSON files into Database
print("Initializing Database")
subprocess.run(['python', 'InitializeMMPL.py'])

# Creates and saves Collaborative Filter algorithm
print("Creating Collaborative Filter")
subprocess.run(['python', 'CreateCollFilter.py'])

# Generate and save challenge submissions
print("Generating Recommendations")
subprocess.run(['python', 'RecommendTracks.py'])
