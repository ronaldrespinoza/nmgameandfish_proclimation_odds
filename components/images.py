import base64


def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
    return f"data:image/jpeg;base64,{encoded_string}"

encoded_image = encode_image("..//input//Map-New-Mexico-State-Game-Management-Unit-Boundaries.jpg")