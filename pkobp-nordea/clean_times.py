# We open the source file and get its lines
with open('available_dates.csv', 'r') as inp:
    lines = inp.readlines()

# We open the target file in write-mode
with open('available_dates_clean.csv', 'w') as out:
    # We go line by line writing in the target file
    # if the original line does not include the
    # strings 'py-board' or 'coffee'
    for line in lines:
        if not 'B r a k' in line:
            out.write(line)