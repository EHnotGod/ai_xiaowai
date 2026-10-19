from config import AVATAR_PATH

def nailong():
    import base64
    def image_to_data_url(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            data_url = f"data:image/jpeg;base64,{encoded_string}"
        return data_url

    data_url = image_to_data_url(AVATAR_PATH)
    return data_url
