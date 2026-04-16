import os

def fix_paths():
    scripts_dir = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5\scripts"
    old_file = "US/MASTER/SP500_STANDARD.csv"
    new_path = "US/MASTER/SP500_STANDARD.csv"
    
    for filename in os.listdir(scripts_dir):
        if filename.endswith(".py"):
            path = os.path.join(scripts_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_file in content:
                print(f"Repairing path in: {filename}")
                new_content = content.replace(old_file, new_path)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

if __name__ == "__main__":
    fix_paths()
