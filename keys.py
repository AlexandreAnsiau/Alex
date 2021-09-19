import random
import string

letters = [letter for letter in string.ascii_letters]
random.shuffle(letters)
substitution_key = [(letter_org, letter_mel) for letter_org, letter_mel in zip(string.ascii_letters, letters)]
substitution_key = dict(substitution_key)


def substitution_keys_encrypt(clear_message):
	list_letters_message = [letter for letter in clear_message]
	encrypt = "".join([substitution_key[letter] if letter is not " " else letter for letter in list_letters_message])
	return encrypt


def substitution_key_decrypt(encrypted_message):
	key_decrypt = [(value, key) for key, value in zip(substitution_key.keys(), substitution_key.values())]
	key_decrypt = dict(key_decrypt)
	encrypt = [letter for letter in encrypted_message]
	decrypt = "".join([key_decrypt[letter] if letter is not " " else letter for letter in encrypt])
	return decrypt


def one_time_pad_encrypt(message):
	from itertools import zip_longest

	key = [random.choice(["0", "1"]) for i in range(len(message) * 8)]
	letters = [i for i in message]

	for i in range(len(letters)):
		letters[i] = ord(letters[i])
		letters[i] = bin(letters[i])
		letters[i] = letters[i].replace("0b", "")
		ajusted_letter = [i for i, j in zip_longest(letters[i][::-1], range(8), fillvalue="0")][::-1]
		letters[i] = "".join(ajusted_letter)
    
	message_bytes = "".join(letters)  
	message_bytes = [i for i in message_bytes]
	message_crypt = ["0" if message_byte == key_byte else "1" for message_byte, key_byte in zip(message_bytes, key)]
	message_crypt = "".join(message_crypt)

	return message_crypt, key


def one_time_pad_decrypt(message, key):

	# input : message = one_time_pad_encrypt()[0], key = one_time_pad_encrypt()[1]

    import re
    
    message_bytes = [i for i in message]
    message_decrypt = ["0" if message_byte == key_byte else "1" for message_byte, key_byte in zip(message_bytes, key)]
    message_decrypt = "".join(message_decrypt)
    
    pattern = r"\w{8}"
    octets = re.findall(pattern, message_decrypt)
    
    for i in range(len(octets)):
        octets[i] = int(octets[i], 2)
        octets[i] = chr(octets[i])
        
    letters = octets 
    message = "".join(letters)
    
    return message