import os

def fix_files():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.py') and f != 'fix.py':
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Replace literal backslash-quote with just quote
                content = content.replace('\\"\\"\\"', '\"\"\"')
                
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)

if __name__ == "__main__":
    fix_files()
    print("Fixed files.")
