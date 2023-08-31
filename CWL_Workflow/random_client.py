import random
import sys

# Get the list of strings from sys.argv
workflow_output = sys.argv[1:]

# Select a random item
random_item = random.choice(workflow_output)

# Print the selected random item
print(random_item)