import argparse
import ast
import os
import random
import string
import zlib
import colorama
import pyfiglet
import lzma
import gzip
import bz2
import binascii
import marshal

def obfuscate_variable_name(name):
    return ''.join(random.choice(string.ascii_letters) for _ in range(len(name)))

def obfuscate_code(input_code):
    try:
        parsed_code = ast.parse(input_code)
    except SyntaxError:
        return "Error: Invalid Python code"

    def obfuscate_node(node):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            return ast.copy_location(ast.Name(id=obfuscate_variable_name(node.id), ctx=node.ctx), node)
        return node

    obfuscated_ast = ast.fix_missing_locations(obfuscate_node(parsed_code))

    obfuscated_code = ast.fix_missing_locations(obfuscated_ast)
    obfuscated_code = compile(obfuscated_code, filename="<ast>", mode="exec")

    return obfuscated_code

def save_obfuscated_code(output_file, obfuscated_code):
    with open(output_file, 'w') as f:
        f.write(obfuscated_code)

def obfuscate_source(source: str, complexity: int) -> str:
    encoded_source = source
    for _ in range(complexity):
        encoded_source = encode(source=encoded_source)
    return encoded_source

def print_ascii_art():
    ascii_art = """
    ______       _ _               _________________ 
    | ___ \     | | |             |  _  | ___ \  ___|
    | |_/ / __ _| | | ___ _ __ ___| | | | |_/ / |_   
    | ___ \/ _` | | |/ _ \ '__/ __| | | | ___ \  _|  
    | |_/ / (_| | | |  __/ |  \__ \ \_/ / |_/ / |    
    \____/ \__,_|_|_|\___|_|  |___/\___/\____/\_|    
                                                 
                                                 
    """
    print(colorama.Style.BRIGHT + colorama.Fore.LIGHTCYAN_EX + ascii_art)

def encode(source: str) -> str:
    selected_mode = random.choice((lzma, gzip, bz2, binascii, zlib))
    marshal_encoded = marshal.dumps(compile(source, "Py-Fuscate", "exec"))
    if selected_mode is binascii:
        return "import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads(binascii.a2b_base64({})))".format(
            binascii.b2a_base64(marshal_encoded)
        )
    return "import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads({}.decompress({})))".format(
        selected_mode.__name__, selected_mode.compress(marshal_encoded)
    )

def main_menu():
    while True:
        print_ascii_art()
        print("1. Obfuscate")
        print("2. Quit")

        choice = input("Enter your choice (1/2): ")
        if choice == "1":
            obfuscate_main()
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please enter 1 or 2")

def obfuscate_main():
    parser = argparse.ArgumentParser(description="Code Obfuscator")
    parser.add_argument("--input", type=str, help="Input Python file to obfuscate")
    parser.add_argument("--output", type=str, help="Output file for the obfuscated code")
    )
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    if input_file is None:
        input_file = input("Enter the input file name (must be in the same folder as the script): ")

    with open(input_file, "r") as f:
        input_code = f.read()

    if args.complexity is None:
        args.complexity = 100

    obfuscated_code = obfuscate_source(input_code, args.complexity)

    if output_file is None:
        output_file = "obfuscated_code.py"

    save_obfuscated_code(output_file, obfuscated_code)

    print(f"Obfuscated code saved to {output_file}")

if __name__ == "__main__":
    main_menu()
