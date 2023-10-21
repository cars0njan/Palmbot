from cryptography.fernet import Fernet
import os


key = os.environ['KEY']
fernet = Fernet(key)
e_id = b'gAAAAABlMzDXM7w35ZhQq9J2IrWxkV6I6A27vP_N6X9spItONs68Wh4ZJrN_im9BWqRKkpsHf63fE2qWxO1C6dqUIJxTkEeNPiVri9G07NFtKqIPpb_GB5I='
id = fernet.decrypt(e_id)
#key = Fernet.generate_key()
print(id)



# cipher_suite = Fernet(key)
# ciphered_text = cipher_suite.encrypt(b"Hello World")
# print(ciphered_text)
# print(cipher_suite.decrypt(ciphered_text))