# Copycat
Hack the North++ 2021 project

https://devpost.com/software/copycat-ir98wa

# Running the sample project

Next, download the dependencies using Pip, from the current directory:

(venv)$ pip install -r requirements.txt
Then add your own API Key and API Secret to the environment variables. There are a few ways to do this but the simplest would be to do it right in your shell.

You also need to install the appropriate Python wheel as listed [here](https://www.tensorflow.org/lite/guide/python)

For example, if you have a Raspberry Pi that's running Raspberry Pi OS 10 (which has Python 3.7), install the Python wheel as follows:
(venv)$ pip3 install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp37-cp37m-linux_armv7l.whl

(venv)$ export API_KEY=0000000
(venv)$ export API_SECRET=abcdef1234567890abcdef01234567890abcdef
Finally, start the server.

(venv)$ python helloworld.py
Visit http://localhost:5000/ in your browser. Open it again in a second window. Smile! You've just set up a group chat.
