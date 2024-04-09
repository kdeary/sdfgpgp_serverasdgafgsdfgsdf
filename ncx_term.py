import os
import gnupg

'''
sudo apt-get install rng-tools
pip install python-gnupg
'''




#os.system('rm -rf /home/testgpguser/gpghome')
gpg = gnupg.GPG()
input_data = gpg.gen_key_input(
    name_email='testgpguser@mydomain.com',
    passphrase='my passphrase')
key = gpg.gen_key(input_data)
print(key)

unencrypted_string = 'Who are you? How did you get in my house?'
encrypted_data = gpg.encrypt(unencrypted_string, 'testgpguser@mydomain.com')
encrypted_string = str(encrypted_data)
print(f"ok: {encrypted_data.ok}")
print(f"encrypted_string: {encrypted_string}")

