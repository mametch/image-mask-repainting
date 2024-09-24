import os


class ImgFileManager:
    def __init__(self) -> None:
        self.img_names = []
        self.dir_path = ""

    def load_img_paths(self, dir_path: str):
        self.dir_path = dir_path
        self.img_names.clear()

        img_list = os.listdir(dir_path)
        img_list.sort()
        for img_name in img_list:
            if "_FRONT." not in img_name:
                continue

            img_name_back = img_name.replace("_FRONT.", "_BACK.")
            img_back_path = os.path.join(self.dir_path, img_name_back)
            if not os.path.isfile(img_back_path):
                continue

            names_dict = {}
            names_dict["front"] = img_name
            names_dict["back"] = img_name_back
            self.img_names.append(names_dict)

    def get_by_index(self, index):
        img_names = self.img_names[index]
        front_path = os.path.join(self.dir_path, img_names["front"])
        back_path = os.path.join(self.dir_path, img_names["back"])
        return front_path, back_path

    def get_length(self):
        return len(self.img_names)
