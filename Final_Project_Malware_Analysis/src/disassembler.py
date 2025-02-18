#!/usr/bin/env python
import py_compile
import filecmp
import uncompyle6
import dis
import sys
import os
import marshal
import difflib

#disassemble .pyc file.
def disassemble_file_pyc(filename, mode):
    #user guide/help
    if mode == 'h' or mode == 'Help':
        show_help()
     
    #disassemble bytecode from a Python compiled file (.pyc)   
    elif mode == 'd' or mode == 'Disassemble':
        with open(filename, 'rb') as f:
         f.seek(16)
         dis.disassemble(marshal.load(f))  
    #reads the entire file into memory including the header
    elif mode == 'r' or mode == 'Read':
        with open(filename, 'rb') as f:
          magic = f.read(4) # read the magic number
          moddate = f.read(4) # read the modification timestamp
          code = f.read() # read the bytecode
        try:
          dis.dis(code)
        except IndexError:
          print("An error occurred while disassembling bytecode. Please check if the file is a valid Python bytecode file.")

    #displays a human-readable interpretation of the bytecode instructions
    elif mode == 'D' or mode == 'Display':
        with open(filename, "rb") as f:
           f.seek(16)
           dis.show_code(marshal.load(f))  
           
    #bytecode instructions that the Python interpreter would execute when running the program
    elif mode == 'i' or mode == 'instructions':   
        with open(filename, 'rb') as f:
            f.seek(16)
            code = marshal.load(f)
            instructions = dis.get_instructions(code)
            for instr in instructions:
                print(instr)    

    #find the offsets which are starts of lines in the source code              
    elif mode == 'f' or mode == 'Find':
        with open(filename, "rb") as f:
            code_str = f.read()
        code_obj = marshal.loads(code_str[16:])  # skip first 16 bytes (magic number and timestamp)
        print(dis.findlinestarts(code_obj))
                             
    else:
        print("\nInvalid mode: -[OPTION] ")
        show_help()
        

# compile .py file and name it as compiled.py.file.pyc and check the mode
def compile_file(file_py, file_pyc, mode):
    if mode == 'd' or mode == 'Disassemble':
       py_compile.compile(file_py, 'compiled.py.file.pyc')
       value = 'Disassemble'
       compare_pyc_files('compiled.py.file.pyc', file_pyc, value)
    elif mode == 'h' or mode == 'Help':
       show_help()
    elif mode == 'D' or mode == 'Display':
       py_compile.compile(file_py, 'compiled.py.file.pyc')
       value = 'Display'
       compare_pyc_files('compiled.py.file.pyc', file_pyc, value)
    elif mode == 'R' or mode == 'Read':
       py_compile.compile(file_py, 'compiled.py.file.pyc')
       value = 'Read'
       compare_pyc_files('compiled.py.file.pyc', file_pyc, value)
    elif mode == 'I' or mode == 'Instructions':
       py_compile.compile(file_py, 'compiled.py.file.pyc')
       value = 'Instructions'
       compare_pyc_files('compiled.py.file.pyc', file_pyc, value)
    else:
        print("\nInvalid mode: -[OPTION] ")
        show_help()

#compare both .pyc files
def compare_pyc_files(compiled_file, file_pyc, value):
     #if they are the same!
    if filecmp.cmp(compiled_file, file_pyc):
        print("\nThe two files are exactly the same...!")
        sys.exit(1)
    else:# if they are different

        print("\nThe two files are not matching!\n")
         #disassemble bytecode from a Python compiled file (.pyc) 
        if (value == 'Disassemble'):
          with open(compiled_file, "rb") as f, open(file_pyc, "rb") as ff, open("dis_compiled_file.txt", "w") as f_out,  open("dis_other_file.txt", "w") as f_outt:
             f.seek(16)
             code_obj = marshal.load(f)
             dis.disassemble(code_obj, file=f_out)
             dis.disassemble(code_obj, file=f_outt)
             ff.seek(16)
             try:
                 code_obj2 = marshal.load(ff)
             except ValueError as e:
                 print("Error while reading file_pyc:", e)
                 return
             dis.disassemble(code_obj2, file=f_outt)

        #displays a human-readable interpretation of the bytecode instructions and compare
        if (value == 'Display'):
          with open(compiled_file, "rb") as f, open(file_pyc, "rb") as ff, open("dis_compiled_file.txt", "w") as f_out,  open("dis_other_file.txt", "w") as f_outt:
             f.seek(16)
             code_obj = marshal.load(f)
             dis.show_code(code_obj, file=f_out)
             ff.seek(16)
             try:
                 code_obj2 = marshal.load(ff)
             except ValueError as e:
                 print("Error while reading file_pyc:", e)
                 return
             dis.show_code(code_obj2, file=f_outt)   
             
        #reads the entire file into memory including the header and compare        
        if (value == 'Read'):
          with open(compiled_file, "rb") as f, open(file_pyc, "rb") as ff, open("dis_compiled_file.txt", "w") as f_out, open("dis_other_file.txt", "w") as f_outt:
            magic = f.read(4) # read the magic number
            moddate = f.read(4) # read the modification timestamp
            code = f.read() # read the bytecode
            try:
              dis.dis(code, file=f_out)
            except IndexError:
              print("An error occurred while disassembling bytecode. Please check if the file is a valid Python bytecode file.")
              sys.exit(2)
            magic = ff.read(4) # read the magic number
            moddate = ff.read(4) # read the modification timestamp
            code = ff.read() # read the bytecode
            try:
              dis.dis(code, file=f_outt)
            except IndexError:
              print("An error occurred while disassembling bytecode. Please check if the file is a valid Python bytecode file.")
              sys.exit(3)
              
       #bytecode instructions that the Python interpreter would execute when running the program and compare                   
        if value == 'Instructions':
          with open(compiled_file, 'rb') as f1, open('dis_compiled_file.txt', 'w') as f2, open(file_pyc, 'rb') as f3, open('dis_other_file.txt', 'w') as f4:
        # disassemble compiled_file and write to dis_compiled_file.txt
           f1.seek(16)
           code = marshal.load(f1)
           instructions = dis.get_instructions(code)
           for instr in instructions:
             f2.write(f"{instr}\n")
           f3.seek(16)
           code = marshal.load(f3)
           instructions = dis.get_instructions(code)
           for instr in instructions:
             f4.write(f"{instr}\n")
       
    #comparing the diffrances  
    compare_files('dis_compiled_file.txt', 'dis_other_file.txt')

#print the diffrances between the two files .pyc
def compare_files(dis_compiled_file, dis_other_file):
    # Read the content of the files
    with open(dis_compiled_file, 'r') as f1, open(dis_other_file, 'r') as f2:
        file1_content = f1.readlines()
        file2_content = f2.readlines()
    
    # Compare the files and print the results

    # Find the common lines in the files
    common_lines = set(file1_content).intersection(file2_content)
    if common_lines:
        print("Common lines: ..................\n")
        for line in common_lines:
            print(line, end="")
        print("\n")
    
    # Find the different lines in the files
    diff = difflib.ndiff(file1_content, file2_content)
    print("Different lines: ....................\n")
    for line_num, line in enumerate(diff, 1):
        if line.startswith('-'):
            print("@- Line {}: {}".format(line_num, line[2:]), end="")
        elif line.startswith('+'):
            print("#+ Line {}: {}".format(line_num, line[2:]), end="")
    print()

        
#usage and help information about the disassembler tool        
def show_help():
    print()
    print(" Format: $./disassembler --[option] [filename].py [filename].pyc")
    print(" Options: \n")
    print("\t--h/--Help\t\tShow help message\n")
    print("\t--d/--Disassemble\tCompare: Disassemble bytecode")
    print("\t--R/--Read\t\tCompare: The entire file into memory.")
    print("\t--D/--Display\t\tCompare: A human-readable interpretation of the bytecode instructions.")
    print("\t--I/--Instructions\tCompare: Bytecode instructions that the Python interpreter would execute when running the program \n")
    print(" Format: $./disassembler --[option] [filename].pyc")
    print(" Options: \n")
    print("\t--d,  --Disassemble\tDisassemble bytecode from a Python.")
    print("\t--r,  --Read\t\tReads the entire file into memory.")
    print("\t--D,  --Display\t\tDisplays a human-readable interpretation of the bytecode instructions.")
    print("\t--i,  --Instructions\tBytecode instructions that the Python interpreter would execute when running the program.")
    print("\t--f,  --Find\t\tFind the offsets which are starts of lines in the source code.")
    sys.exit(4)

# Check the version of the Python
def chech_file_version(file1):
 file_path = file1
# Get the version of the Python 
 python_version = sys.version_info
# Check if the file is a .py file
 if file_path.endswith(".py"):
     with open(file_path, "r") as f:
         first_line = f.readline()
         # Check if the first line contains any elements after splitting by whitespace
         if len(first_line.split()) == 0:
             print(f"\nError: File {file_path} is empty or does not contain any whitespace-separated elements.")
             exit(1)
         version_info = first_line.split()[-1]
         version = version_info.strip("v")
 # Check if the version information matches the Python version
 if version != f"{python_version.major}.{python_version.minor}":
     print(f"\nError: File version {version} does not match Python version {python_version.major}.{python_version.minor}")
     exit(1)

    
if __name__ == '__main__':
    #Check if no arguments are provided or the name of the program is incorrect
    if len(sys.argv) == 1  and sys.argv[0] == "./disassembler.py":
       show_help()
       sys.exit(5)
       
    #Get the mode argument and check if the correct number of arguments is provided
    mode = sys.argv[1][:2]
    if len(sys.argv) >= 5 or mode != "--" or len(sys.argv) <= 2 :
       if sys.argv[1] == '--h' or sys.argv[1] == '--Help':
         show_help()
       print(f"\nError: Check the required format with correct number of arguments!")
       show_help()
       sys.exit(6)
       
    #Get the filename argument and check if it exists   
    filename = sys.argv[2] 
    if not os.path.isfile(filename):
         print(f"\nError: file '{filename}': Could not open the binary for disassembly!")
         print("Error: The file does not exist or has the wrong file extension.")
         sys.exit(7)

    #If all arguments are correct, disassemble the file using the specified mode     
    if len(sys.argv) == 3:
        mode = sys.argv[1].lstrip("--")
        if sys.argv[2][-2:] == "yc": #.pyc file
          disassemble_file_pyc(filename, mode)
        else:
          print("\nInvalid file type: the file must be .pyc")

    #check user inputs for comparing files and make sure all the inputs are correct.
    elif len(sys.argv) == 4 and sys.argv[2][-2:] == "py" and sys.argv[3][-2:] == "yc":
     filename = sys.argv[3] 
     if not os.path.isfile(filename):
         print(f"\nError: file '{filename}': Could not open the binary for disassembly!")
         print("Error: The file does not exist or has the wrong file extension.")
         sys.exit(8)
     mode = sys.argv[1].lstrip("--")
     if sys.argv[2][-2:] == "py": #.py file
         file1 = sys.argv[2]
         file2 = sys.argv[3]
         chech_file_version(file1)
         compile_file(file1, file2, mode)
    #anything else print help message
    else:
        show_help()
        sys.exit(9)
