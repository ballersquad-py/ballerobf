import argparse
import ast
import os
import random
import string
import marshal
import zlib

def obf(name):
    return ''.join(random.choice(string.ascii_letters) for _ in range(len(name)))

def obfuscate(code):
    try:
        parsed_code = ast.parse(code)
    except SyntaxError:
        return "Error: Invalid Python code"

    def obf_node(node):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            return ast.copy_location(ast.Name(id=obf(node.id), ctx=node.ctx), node)
        return node

    obfd_ast = ast.fix_missing_locations(obf_node(parsed_code))

    obfd_code = ast.fix_missing_locations(obfd_ast)
    obfd_code = compile(obfd_code, filename="<ast>", mode="exec")

    return obfd_code

def save(output_file, obfd_code):
    with open(output_file, 'w') as f:
        f.write(obfd_code)

def obf_source(source: str, complexity: int) -> str:
    encoded_source = source
    for _ in range(complexity):
        encoded_source = encode(source=encoded_source)
    return encoded_source

def encode(source: str) -> str:
    marshal_encoded = marshal.dumps(compile(source, "Py-Fuscate", "exec"))
    zlib_encoded = zlib.compress(marshal_encoded)
    return f"exec(__import__('marshal').loads(__import__('zlib').decompress({repr(zlib_encoded)})))"

def main_menu():
    while True:
        menu()
        print("1. Obfuscate")
        print("2. Quit")

        choice = input("Enter your choice (1/2): ")
        if choice == "1":
            obfuscate_code()
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please enter 1 or 2")

def obfuscate_code():
    parser = argparse.ArgumentParser(description="Code Obfuscator")
    parser.add_argument("--input", type=str, help="Input Python file to obfuscate")
    parser.add_argument("--output", type=str, help="Output file for the obfuscated code")
    parser.add_argument("--complexity", type=int, help="Obfuscation complexity")
    args = parser.parse_args()

    file = args.input
    output_file = args.output

    if file is None:
        file = input("Enter the file name: ")

    with open(file, "r", encoding="utf-8") as f:  # Specify encoding as utf-8
        code = f.read()

    if args.complexity is None:
        args.complexity = 100

    obfd_code = obf_source(code, args.complexity)

    if output_file is None:
        output_file = "obfuscated_code.py"

    save(output_file, obfd_code)

    print(f"Obfuscated code saved to {output_file}")


def menu():
    ascii_art = """
    ______       _ _               _________________ 
    | ___ \     | | |             |  _  | ___ \  ___|
    | |_/ / __ _| | | ___ _ __ ___| | | | |_/ / |_   
    | ___ \/ _` | | |/ _ \ '__/ __| | | | ___ \  _|  
    | |_/ / (_| | | |  __/ |  \__ \ \_/ / |_/ / |    
    \____/ \__,_|_|_|\___|_|  |___/\___/\____/\_|    
                                                 
                                                 
    """
    print(ascii_art)

if __name__ == "__main__":
    main_menu()
