import pandas as pd
import datetime as dt
import smtplib
from random import choice

MY_EMAIL = 'Your email'
MY_PASSWORD = 'Your password'

birthdays = {
    'name': ['Nika', 'Giorgi', 'Lasha', 'Daviti', 'Tornike'],
    'email': ['testemail1@gmail.com', 'testemail2@gmail.com',
              'testemail3@gmail.com', 'testemail4@gmail.com', 'testemail5@outlook.com'],
    'year': ['1992', '1994', '1970', '1980', '1990'],
    'month': ['04', '06', '10', '06', '08'],
    'day': ['08', '11', '12', '20', '20'],
}
convert = pd.DataFrame(birthdays)
convert.to_csv("birthdays.csv", index=False)

now = dt.datetime.now()
current_year = now.year
current_month = now.month
current_day = now.day

data = pd.read_csv('birthdays.csv')
bday_data = data[(data['day'] == current_day) & (data['month'] == current_month)]
bday_dict = bday_data.to_dict()

bday_names_list = []
bday_emails_list = []
for i in range(len(bday_dict['name'])):
    bday_names_list.append(bday_dict['name'][i])
    bday_emails_list.append(bday_dict['email'][i])

all_letters = []

for i in range(1, 4):
    with open(f'letter_templates\letter_{i}.txt', 'r') as letter_templates:
        letter_list = letter_templates.readlines()
        all_letters.append(letter_list)

try:
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        for name, email in zip(bday_names_list, bday_emails_list):
            random_letter = choice(all_letters)
            letter = '\n'.join([line.replace('Angela', 'Nika').replace('[NAME]', name) for line in random_letter])
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=f'{email}',
                msg=f"Subject: Happy Birthday!\n\n"
                    f"{letter}"
            )
            print(f"Email sent successfully to Name: {name} and Email: {email}")
except Exception as e:
    print(f"Error sending email: {e}")
