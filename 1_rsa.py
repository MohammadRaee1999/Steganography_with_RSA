import rsa

def generate_key():
    key_len = input("Enter rsa key length: ")
    public_key, private_key = rsa.newkeys(int(key_len))
    return public_key, private_key

def encryption(public_key):
    msg = input("Enter message: ")
    cipher_text = rsa.encrypt(msg.encode(), public_key)
    print("cipher text: ",cipher_text)
    return cipher_text

def decryption(cipher_text,private_key):
    plain_text = rsa.decrypt(cipher_text, private_key).decode()
    print("plain text: ", plain_text)


# Driver Code
if __name__ == '__main__':
    print(":: generating keys ::")
    public_key, private_key = generate_key()
    print(":: encryption ::")
    cipher_text = encryption(public_key)
    print(":: decryption ::")
    decryption(cipher_text,private_key)