data = 'test:testasd'
print(data)
print(chr(16 - len(data) % 16))
padded_data = data + (16 - len(data) % 16) * chr(16 - len(data) % 16)
print(padded_data)
padded_data = padded_data.encode()
padding_length = padded_data[-1]
unpadded_data = padded_data[:-padding_length]
print(unpadded_data.decode())