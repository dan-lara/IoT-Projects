import base64

# Base64-encoded message
encoded_message = "PEFCQ0RFRjAxMiwtNDA7Pg=="

# Decode the message
decoded_message = base64.b64decode(encoded_message)
# Print the decoded message as a string
print(decoded_message.decode('utf-8'))
