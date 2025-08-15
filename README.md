📢 SpeedTweeter - Internet Speed Complaint Bot
Automatically tweet at your ISP when your internet speeds are slower than promised!

🤔 What Does This Do?
This Python bot:

Measures your current internet speed using Speedtest.net

Compares it to the speeds you're paying for

Tweets at your ISP if speeds are below expectations

Perfect for when you're tired of overpaying for slow internet!

🛠️ Setup (1 Minute)
Requirements
Google Chrome installed

Python 3.8+

A Twitter/X account

Installation
Clone this repo:

bash
git clone [https://github.com/yourusername/SpeedTweeter.git](https://github.com/fuad-tafese-dev/internet-speed-complaint-bot)
cd SpeedTweeter
Install dependencies:

bash
pip install selenium python-dotenv
Create .env file and add your Twitter login:

ini
TWITTER_EMAIL=your@email.com
TWITTER_PASSWORD=yourpassword
⚡ How to Use
Edit promised_speeds.py:

python
PROMISED_DOWN = 150  # Download speed you pay for (Mbps)
PROMISED_UP = 10     # Upload speed you pay for (Mbps)
Run the bot:

bash
python main.py
The bot will:

Run a speed test

Log into Twitter

Post a complaint tweet if speeds are slow

🌟 Example Tweet
"Hey @ISPProvider, why is my internet speed 85down/5up when I pay for 150down/10up? #InternetSpeed #ISP"

⚠️ Note
This is for educational purposes

Don't spam your ISP (use responsibly)

Twitter may block automated activity - use at your own risk

🚀 Future Ideas
Schedule daily speed checks

Add ISP's Twitter handle automatically


Made with ❤️ and 😤 at slow internet speeds
