import json
import os
import random
import copy
from copy import deepcopy
import uuid

from utils import *

base_path = "data"
mapper: dict = load_json(os.path.join(base_path, "mapper.json"))
r2f = load_json(os.path.join(base_path, "r2f.json"))
f2r = load_json(os.path.join(base_path, "f2r.json"))


def create_questions():

    questions = []
    for key in mapper.keys():
        class_info = mapper[key]
        sub_idx = random.randint(0, class_info["total"] - 1)
        sub_path = os.path.join(base_path, class_info["class"], str(sub_idx))

        ref_img = os.path.join(base_path, class_info["class"], "ref.png")
        tar_img = os.path.join(sub_path, "tar.png")
        ours = os.path.join(sub_path, "ours.gif")
        texture = os.path.join(sub_path, "tex.gif")
        texpainter = os.path.join(sub_path, "painter.gif")
        paint3d = os.path.join(sub_path, "paint3d.gif")

        options = [r2f[ours], r2f[texture], r2f[texpainter], r2f[paint3d],]
        random.shuffle(options)

        questions.append(
            {
                "ref_img": r2f[ref_img],
                "tar_img": r2f[tar_img],
                "options": options
            }
        )
    random.shuffle(questions)
    uid = str(uuid.uuid4())

    return questions, uid


def backup(questions, uid):
    qs = {}
    for idx, q in enumerate(questions):
        qs[idx] = q

    output_path = f"./summary/questions/{uid}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as file:
        json.dump(qs, file, indent=2)


def save_result(result, uid):
    output_path = f"./summary/results/{uid}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    ans = []
    for key in result.keys():
        ans.append(f2r[result[key]]["label"])
    with open(output_path, "w") as file:
        json.dump(ans, file, indent=2)
