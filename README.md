# Copycat
Hack the North++ 2021 project

# Running the sample project

Next, download the dependencies using Pip, from the current directory:

(venv)$ pip install -r requirements.txt
Then add your own API Key and API Secret to the environment variables. There are a few ways to do this but the simplest would be to do it right in your shell.

(venv)$ export API_KEY=0000000
(venv)$ export API_SECRET=abcdef1234567890abcdef01234567890abcdef
Finally, start the server.

(venv)$ python helloworld.py
Visit http://localhost:5000/ in your browser. Open it again in a second window. Smile! You've just set up a group chat.
