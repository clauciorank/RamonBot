import time
import cv2
import numpy as np
from PIL import Image, ImageDraw
import tweepy
import credentials
import urllib.request



def reading_image(image_file):
    try:
        image = Image.open(image_file)
        new_size = (640, 360)
        image = image.resize(new_size)
        img_cv2 = np.array(image)

        # Warping
        pts1 = np.float32([[0, 0], [0, 360], [640, 0], [640, 360]])
        pts2 = np.float32([[614, 523], [605, 823], [1212, 607], [1154, 962]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        output = cv2.warpPerspective(img_cv2, matrix, (1300, 1600))
        output_pil = Image.fromarray(output)

        # Read Ramon and Paste
        ramon = Image.open('ramon.png')

        # Mask image
        mask_im = Image.new("L", ramon.size, 0)

        draw = ImageDraw.Draw(mask_im)
        draw.polygon(((614, 523), (1212, 607), (1154, 962), (605, 823)), fill=255)
        ramon.paste(output_pil, mask_im)

        # Crop and save
        crop = (0, 0, 1200, 1600)
        ramon = ramon.crop(crop)
        ramon.save('montagem.png')
    except:
        print('error making image')

def append(file_name, string):
    f = open(file_name, 'a')
    f.write(string+"\n")
    f.close()

def read_file(file):
    f = open(file, 'r')
    replied_file = f.read().splitlines()
    f.close()
    return(replied_file)

def tweet():
    auth = tweepy.OAuthHandler(credentials.API_key, credentials.API_secret_key)
    auth.set_access_token(credentials.access_token, credentials.access_token_secret)
    auth.secure = True
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print('Connection Working')
    except:
        print('Connection Not Working')


    mention = api.mentions_timeline()
    already_replied = read_file('replied.txt')


    for tweet in mention:
        id_tweet = tweet.in_reply_to_status_id_str
        id_mention = tweet.id_str
        if id_mention not in already_replied:
            print(id_mention)
            tweet = api.get_status(id_tweet)._json['extended_entities']['media']
            media_url = tweet[0]['media_url']
            file_extension = media_url[-3:]

            try:
                urllib.request.urlretrieve(media_url, 'image.' + file_extension)
                reading_image('image.' + file_extension)
                print('Image Downloaded and generated')
            except:
                print('Problem Downloading or making picture')

            try:
                api.create_favorite(id_mention)
                media = api.media_upload('montagem.png')
                api.update_status("Here is your Ramon", in_reply_to_status_id=id_mention,
                                  auto_populate_reply_metadata=True, media_ids=[media.media_id])
                print('tweet replied')
                append('replied.txt', str(id_mention))
            except:
                print('error uploading and posting tweet')
        else:
            print('All replied')


if __name__ == '__main__':
    while True:
        try:
            tweet()
            print('All Ok')
        except:
            print('error')
        time.sleep(60)





