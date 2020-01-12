from flask import Flask, request, render_template
import os
from flask_mail import Mail, Message 

def main():
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    mail = Mail(app)
    
    @app.route('/send')
    def send():
        print(f'Using user name "{app.config["MAIL_USERNAME"]}" and password "{app.config["MAIL_PASSWORD"]}"')
        message = Message('Hello, world!', sender='Samuel Rowe <samuelrowe1999@gmail.com>',
            recipients=[ 'samuelrowe1999@gmail.com', 'joelerego@gmail.com' ])
        message.body = 'Hi, Joel!\nHow are you doing?\nSent this mail via Flask Mail!\n\nBest regards,\nSamuel Rowe.'
        mail.send(message)
        
        return 'Successfully sent an email!<br />Message:<br />' + message.body
    
    app.run(debug=True)

if __name__ == '__main__':
    main()