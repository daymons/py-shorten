# py-shorten, a lightweight yet efficient link shortener, in Python
A lightweight URL shortener that uses Flask and a SQLite database to achieve a very light program while maintaining efficiency.

## Installation
 - Make sure to have the `dotenv`, `flask`, and `sqlite3` libraries installed before continuing.<br>
 - Clone the repository (`git clone https://github.com/daymons/py-shorten`) to your machine and run the `db.py` file once. This will create the database file with the proper structure.
 - Change the settings in the `.env` file (at least the SECRET_KEY and BASE_URL variables). All the variable functionalities are explained in the .env file.

## Running
 - Run the `app.py` file and the app will be opened and available at [localhost:5000](http://localhost:5000).
 - Set up a reverse proxy appropriate for your webserver (for nginx, follow [this guide](https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-as-a-reverse-proxy-on-ubuntu-22-04)).
 - If you want to, you can set up a service on your machine to auto-start the program every time the machine boots. You can follow [this guide](https://www.siberoloji.com/how-to-configure-system-startup-services-in-debian-12/#creating-a-custom-service).

## Contact
If any doubts arise, you can contact me through [my e-mail](mailto:hyperyzen5@gmail.com).
