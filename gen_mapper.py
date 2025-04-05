import json
import os

def main(path):
    class_path = os.listdir(path)
    mapper = {}
    for i, name in enumerate(class_path):
        cur_folder = os.path.join(path, name)
        if os.path.isdir(cur_folder) and name != "pool":
            subfolder = os.listdir(cur_folder)
            total = 0
            for sub in subfolder:
                if os.path.isdir(os.path.join(cur_folder, sub)):
                    total += 1
            mapper[str(i)]={
                "class": name,
                "total": total
            }

    with open(os.path.join(path, "mapper.json"), "w") as file:
        json.dump(mapper, file, indent=2)

if __name__ == "__main__":
    main("data")
