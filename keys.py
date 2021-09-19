"""
	This script aims to encrypt and decrypt messages.
"""


import random
import string

letters = [letter for letter in string.ascii_letters]
random.shuffle(letters)
substitution_key = [(letter_org, letter_mel) for letter_org, letter_mel in zip(string.ascii_letters, letters)]
substitution_key = dict(substitution_key)


def substitution_keys_encrypt(clear_message):

	"""
	encrypt a clear message

	Parameters
	----------
	clear_message : str
		clear_message that must be encrypted

	Returns
	-------
	str
		encrypted message
	"""

	list_letters_message = [letter for letter in clear_message]
	encrypt = "".join([substitution_key[letter] if letter is not " " else letter for letter in list_letters_message])

	return encrypt


def substitution_key_decrypt(encrypted_message):

	"""
	decrypt an encrypted message

	Parameters
	----------
	encrypted_message : str
		encrypted message that must be decrypted

	Returns
	-------
	str
		clear message
	"""

	key_decrypt = [(value, key) for key, value in zip(substitution_key.keys(), substitution_key.values())]
	key_decrypt = dict(key_decrypt)
	encrypt = [letter for letter in encrypted_message]
	decrypt = "".join([key_decrypt[letter] if letter is not " " else letter for letter in encrypt])
	return decrypt


def one_time_pad_encrypt(clear_message):

	"""
	encrypt a clear message

	Parameters
	----------
	clear_message : str
		clear_message that must be encrypted

	Returns
	-------
	tuple(str, str)
		encrypted message, key
	"""

	from itertools import zip_longest

	key = [random.choice(["0", "1"]) for i in range(len(message) * 8)]
	letters = [i for i in clear_message]

	for i in range(len(letters)):
		letters[i] = ord(letters[i])
		letters[i] = bin(letters[i])
		letters[i] = letters[i].replace("0b", "")
		ajusted_letter = [i for i, j in zip_longest(letters[i][::-1], range(8), fillvalue="0")][::-1]
		letters[i] = "".join(ajusted_letter)
    
	message_bytes = "".join(letters)  
	message_bytes = [i for i in message_bytes]
	encrypted_message = ["0" if message_byte == key_byte else "1" for message_byte, key_byte in zip(message_bytes, key)]
	encrypted_message = "".join(encrypted_message)

	return encrypted_message, key


def one_time_pad_decrypt(encrypted_message, key):

	# input : message = one_time_pad_encrypt()[0], key = one_time_pad_encrypt()[1]

	"""
	decrypt an encrypted message

	Parameters
	----------
	encrypted_message : str
		encrypted message that must be decrypted. It is genererate by the 
		one_time_pad_encrypt function.
	key : str
		random key which is created by the one_time_pad_encrypt function.

	Returns
	-------
	str
		clear message
	"""

    import re
    
    message_bytes = [i for i in encrypted_message]
    decrypted_message = ["0" if message_byte == key_byte else "1" for message_byte, key_byte in zip(message_bytes, key)]
    decrypted_message = "".join(decrypted_message)
    
    pattern = r"\w{8}"
    octets = re.findall(pattern, decrypted_message)
    
    for i in range(len(octets)):
        octets[i] = int(octets[i], 2)
        octets[i] = chr(octets[i])
        
    letters = octets 
    clear_message = "".join(letters)
    
    return clear_message