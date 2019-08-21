import requests

IMAGE_SIZE=150
URL=f'https://picsum.photos/{IMAGE_SIZE}.jpg/'
NUMBER_OF_FILES=800

def write_to_file(response, number):
    filename = f'image-{number}.jpg'
    with open(filename, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)

def get_image(number: int):
    print(f'getting image {i+1}')
    params = {'random': number}
    r = requests.get(URL, params=params)
    write_to_file(r, number)

for i in range(NUMBER_OF_FILES):
    get_image(i)
