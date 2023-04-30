import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from cryptography.fernet import Fernet

def main():

    # Get user input for encryption or decryption

    user_input = input("Do you want to encrypt or decrypt? (e) (d): ")

    # Check if the user wants to encrypt

    if user_input == 'e':

        # Get user input for input file and type

        file_name = input("Enter the file name to encrypt: ")
        file_type = input("Enter the file type: (no leading '.') ")

        # Take input file and convert to plaintext
        # Put a "." between file_name and file_type so computer can read it

        with open(file_name + '.' + file_type, 'rb') as input_file:
            plaintext = input_file.read()

        # Use Fernet library for the key

        key = Fernet.generate_key()

        # Use Fernet library for seed

        seed = Fernet(key)

        # Encrypt the plaintext using the seed

        ciphertext = seed.encrypt(plaintext)

        # Write the ciphertext to the output file

        with open('secret.txt', 'wb') as output_file:
            output_file.write(ciphertext)

        # Write the key to a separate file for safety

        with open('key.txt', 'wb') as key_file:
            key_file.write(key)

        print("Encryption successful.")

        # Ask user if they want to send an email
        # If user input is yes: ask user for recipient's email address and store input as recipient_email
        # if user input is no: goto line 97

        send_email = input("Do you want to send the encrypted message and key via email? (y) (n): ")
        if send_email.lower() == 'y':
            recipient_email = input("Enter the recipient's email address: ")

        # Create email using MIME multipart
        # 'To' field uses the previously stored input for recipient_email
        # 'From' email intentionally left blank for security

            message = MIMEMultipart()
            message['From'] = 'XXX'
            message['To'] = recipient_email
            message['Subject'] = 'Encrypted message and key'

        # Attach the secret.txt file to the email
            with open('secret.txt', 'rb') as attachment:
                secret_attachment = MIMEApplication(attachment.read(), _subtype='txt')
                secret_attachment.add_header('Content-Disposition', 'attachment', filename='secret.txt')
                message.attach(secret_attachment)

        # Attach the key.txt file to the email
            with open('key.txt', 'rb') as attachment:
                key_attachment = MIMEApplication(attachment.read(), _subtype='txt')
                key_attachment.add_header('Content-Disposition', 'attachment', filename='key.txt')
                message.attach(key_attachment)

        # Send the email using smtplib
        # 465 is used since 587 failed
        # app_password and email intentionally left blank for security

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                app_password = "XXXX"
                server.login('XXXX', app_password)
                server.sendmail('XXXX', recipient_email, message.as_string())

            print("Email sent.")
        elif send_email.lower() == 'n':
            print("Email not sent.")
        else:
            print("Invalid input. Email not sent.")

    # Check if the user wants to decrypt

    elif user_input == 'd':
        
        # Read secret file

        with open('secret.txt', 'rb') as input_file:
            ciphertext = input_file.read()

        # Take key file and read the encryption key

        with open('key.txt', 'rb') as key_file:
            key = key_file.read()

        # Use Fernet for the seed

        seed = Fernet(key)

        # Get user input for output file and type

        file_name = input("Enter a file name to save the decrypted message as: ")
        file_type = input("Enter the file type: (no leading '.') ")

        # Decrypt the ciphertext using the seed

        plaintext = seed.decrypt(ciphertext)

        # Write the plaintext to the output file
        # Put a "." between file_name and file_type so computer can read it 

        with open(file_name + '.' + file_type, 'wb') as output_file:
            output_file.write(plaintext)

        print("Decryption successful.")

    # Invalid input

    else:
        print("Invalid input. Please enter 'e' or 'd'.")

if __name__ == '__main__':
    main()
