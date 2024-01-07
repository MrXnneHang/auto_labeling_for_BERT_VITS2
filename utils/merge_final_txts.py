import glob

# Get all the text files matching the pattern './tmp/final*.txt'
file_paths = glob.glob('./tmp/final*.txt')

# Open the file for writing the merged content
with open('./tmp/merged.txt', 'w',encoding="utf-8") as merged_file:
    for file_path in file_paths:
        # Write the file name as a separator
        merged_file.write(f'{file_path}\n-----------\n')
        # Open each file and write its contents to the merged file
        with open(file_path, 'r',encoding="utf-8") as file:
            lines = file.readlines()
            merged_file.write(''.join(lines))
            # Add a separator after the contents of each file
            merged_file.write('\n-----------\n')
