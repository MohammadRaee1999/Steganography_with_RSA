# PIL module is used to extract
# pixels of image and modify it
from PIL import Image
import hashlib
import rsa
import binascii

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):

        # list of binary codes
        # of given data
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):

    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
def data_encryption(data,public_key):
    # cipher_text = data + public_key
    cipher_text = rsa.encrypt(data.encode(),public_key)
    # hashed_cipher = hash(cipher_text)
    sha256 = hashlib.sha256()
    sha256.update(cipher_text)
    hashed_cipher = sha256.hexdigest()
    # secure_msg = hashed_cipher + public_key
    secure_msg = rsa.encrypt(hashed_cipher.encode(),public_key)
    # data = cipher_text + secure_msg
    cipher_text = str(binascii.hexlify(cipher_text).decode('utf-8'))
    secure_msg = str(binascii.hexlify(secure_msg).decode('utf-8'))
    return (cipher_text+" "+secure_msg)

# save private key
def save_key(private_key,file_name):
    pri = private_key.save_pkcs1('PEM').decode()
    with open(file_name, 'w+') as myfile:
        myfile.write(pri)
        myfile.close()


# Encode data into image
def encode():
    key_len = input("Enter rsa key length : ")
    public_key, private_key = rsa.newkeys(int(key_len))
    file_name = input("Enter file name for save private key (*.pem) : ")
    save_key(private_key,"private_keys/"+file_name)
    img = input("Enter image name(with extension) : ")
    image = Image.open("images/"+img, 'r')

    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty!!')

    newimg = image.copy()
    encode_enc(newimg, data_encryption(data, public_key))

    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save("images/"+new_img_name, str(new_img_name.split(".")[1].upper()))

# Main Function
def main():
    print(":: Welcome to Steganography, encryption ::")
    encode()

# Driver Code
if __name__ == '__main__' :

    # Calling main function
    main()