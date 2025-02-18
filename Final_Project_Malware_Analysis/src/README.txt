The tool is designed to run on the following environment:
Kali GNU/Linux
Python 3.10

NOTE: The code for the tool is in the 'disassembler.py' file. All the other files are for testing purposes.

Give permission to the file, use the following command:
chmod +x disassembler.py


You need to install the following packages with pip:
pip install py_compile
pip install filecmp
pip install uncompyle6
pip install dis
pip install sys
pip install os
pip install marshal
pip install difflib

#To run the tool in the terminal, use the following command:
#./disassembler.py
This will print the user guide on how to use the tool. Alternatively, you can run the guide by typing:
#./disassembler.py --Help


To compile a .py file with a .pyc file, use the following format:
./disassembler.py --[option] [filename].py [filename].pyc
Available options include:
--h/--Help: Show help message
--d/--Disassemble: Disassemble bytecode
--R/--Read: Read the entire file into memory.
--D/--Display: Display a human-readable interpretation of the bytecode instructions.
--I/--Instructions: Bytecode instructions that the Python interpreter would execute when running the program.

To disassemble a .pyc file, use the following format:
./disassembler.py --[option] [filename].pyc
Available options include:
--d/--Disassemble: Disassemble bytecode from a Python.
--r/--Read: Reads the entire file into memory.
--D/--Display: Displays a human-readable interpretation of the bytecode instructions.
--i/--Instructions: Bytecode instructions that the Python interpreter would execute when running the program.
--f/--Find: Find the offsets which are the starts of lines in the source code.

Note that all files have to be Python 3.10 in order to get the best results.
