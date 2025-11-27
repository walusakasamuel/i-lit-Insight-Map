import os
import ast

project_dir = "."
imports = set()

for root, _, files in os.walk(project_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    node = ast.parse(f.read())
                    for n in ast.walk(node):
                        if isinstance(n, ast.Import):
                            for name in n.names:
                                imports.add(name.name.split(".")[0])
                        elif isinstance(n, ast.ImportFrom):
                            if n.module:
                                imports.add(n.module.split(".")[0])
            except:
                pass

print("Detected imports:")
for lib in sorted(imports):
    print(lib)
