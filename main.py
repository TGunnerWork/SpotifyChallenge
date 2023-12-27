import subprocess

# Consolidates JSON files into Database
subprocess.run(['python', 'InitializeMMPL.py'])

# Creates and saves Collaborative Filter algorithm
subprocess.run(['python', 'CreateCollFilter.py'])

# Generate and save challenge submissions
subprocess.run(['python', 'RecommendTracks.py'])
