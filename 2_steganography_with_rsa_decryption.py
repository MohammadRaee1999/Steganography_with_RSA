# PIL module is used to extract
# pixels of image and modify it
from PIL import Image
import hashlib
import rsa
import binascii


# load private key
def load_key(file_name):
    with open("private_keys/"+file_name, 'r') as f:
        private_key = rsa.PrivateKey.load_pkcs1(f.read())
        return (private_key)


def data_decryption(data,private_key):
    # data --> cipher_text + secure_msg
    cipher_secure = data.split(" ")
    cipher_text = cipher_secure[0]
    secure_msg = cipher_secure[1]
    cipher_text = binascii.unhexlify(bytes(cipher_text.encode('utf-8')))
    secure_msg = binascii.unhexlify(bytes(secure_msg.encode('utf-8')))
    # hashed_cipher = secure_msg + private_key
    hashed_cipher = rsa.decrypt(secure_msg, private_key).decode()
    # hash(cipher_text)
    sha256 = hashlib.sha256()
    sha256.update(cipher_text)
    cipher_text_to_hash = sha256.hexdigest()
    # if(hash(cipher_text) == hashed_cipher) --> data = cipher_text + private_key
    if cipher_text_to_hash == hashed_cipher:
        data = rsa.decrypt(cipher_text, private_key).decode()
        return (data)
    # else --> print("integrity not confirm")
    else:
        return ("integrity not confirm")


# Decode the data in the image
def decode():
    file_name = input("Enter file name for load private key (*.pem) : ")
    private_key = load_key(file_name)
    img = input("Enter encrypted_image name(with extension) : ")
    image = Image.open("images/"+img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return (data_decryption(data,private_key))

# Main Function
def main():
    print(":: Welcome to Steganography, decryption ::")
    print("Decoded Word : " + decode())

# Driver Code
if __name__ == '__main__' :

    # Calling main function
    main()