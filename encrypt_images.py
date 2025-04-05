"""
create an uuid for each image
"""

import os
import json

from utils import *

base_path = "data"
mapper: dict = load_json(os.path.join(base_path, "mapper.json"))

os.makedirs(os.path.join(base_path, "pool"), exist_ok=True)


if __name__ == "__main__":
    r2f = {}
    f2r = {}
    for key in mapper.keys():
        class_info = mapper[key]
        ref_img = os.path.join(base_path, class_info["class"], "ref.png")
        ref_md5 = get_md5(ref_img)
        r2f[ref_img] = ref_md5
        f2r[ref_md5] = {"path": ref_img}

        for idx in range(class_info["total"]):
            sub_path = os.path.join(base_path, class_info["class"], str(idx))

            tar_img = os.path.join(sub_path, "tar.png")
            tar_md5 = get_md5(tar_img)
            r2f[tar_img] = tar_md5
            f2r[tar_md5] = {"path": tar_img}

            ours = os.path.join(sub_path, "ours.gif")
            ours_md5 = get_md5(ours)
            r2f[ours] = ours_md5
            f2r[ours_md5] = {"path": ours, "label": "ours"}

            texture = os.path.join(sub_path, "tex.gif")
            texture_md5 = get_md5(texture)
            r2f[texture] = texture_md5
            f2r[texture_md5] = {"path": texture, "label": "tex"}

            texpainter = os.path.join(sub_path, "painter.gif")
            texpainter_md5 = get_md5(texpainter)
            r2f[texpainter] = texpainter_md5
            f2r[texpainter_md5] = {"path": texpainter, "label": "painter"}

            paint3d = os.path.join(sub_path, "paint3d.gif")
            paint3d_md5 = get_md5(paint3d)
            r2f[paint3d] = paint3d_md5
            f2r[paint3d_md5] = {"path": paint3d, "label": "paint3d"}

    with open(os.path.join(base_path, "r2f.json"), "w") as file:
        json.dump(r2f, file, indent=2)
    with open(os.path.join(base_path, "f2r.json"), "w") as file:
        json.dump(f2r, file, indent=2)
