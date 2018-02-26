# PyOL

**What?**
A tool to execute local python code in the remote server.

**How?**
Write python code locally in your crappy PC, execute it with your horse-powered workstation miles away, retrieve back the output.

**Why?**
I like to work flexibly, with a high mobility, on my (old) laptop. Alas, it is not enough to fulfill my requirement, as I work with big chunk of data processing on a daily basis. Fortunately my lab provides me a high-end PC. So I write this tool to connect the high computing power of that PC and the pervasiveness of my laptop.

### Installing

##### a) On the server side (i.e., our powerful PC)
Clone this reporsitory:
```
$ git clone https://github.com/ariaghora/pyol.git
$ cd pyol
```

Optional: Activate the virtual environment, in which all libraries have been installed to run our project scripts:
```
$ source activate your_env
```

PyOL server requires Flask, thus we need to install it:
```
$ pip install Flask
```
For more complete flask installation guide, visit [Flask documentation](http://flask.pocoo.org/docs/0.12/installation/).

Create a configuration file for server ("server.json") inside the "script" folder. Determine the location to store and maintain the clone of our projects in the server by setting the `"upload_folder"` key. For example:
```json
{
	"upload_folder":"/home/ariaghora/pyol_upload"
}
```

Finally run the server:
```
$ python script/serve.py
```
Output:
```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 313-479-971
```
**Note:** keep the server host information (i.e., IP and port number) since we will need this for client configuration.

##### b) On the client side (i.e., our crappy PC)
Clone this reporsitory:
```
$ git clone https://github.com/ariaghora/pyol.git
```

Install required dependencies:
```
$ pip install requests colorama
```

Add "pyol" folder to the PATH environment variable to make it accessible anywhere.

### Usage example
Create an empty project folder named "hello" containing "hello.py" file:
```python
# hello.py
print("Hello world")
```

Initialize pyol in our project root directory with "pyol init" command, and  the project name and server host.
```
$ pyol init
Enter the project name: hello
Enter the pyol server host: http://127.0.0.1:5000
```

Now our project should be uploaded and synchronized in the server, inside the folder whose name is based on the project name (e.g., in `"/home/ariaghora/pyol_upload/hello/"`).

Run "hello.py" with pyol:
```
$ pyol run hello.py
```

Output:
```
Checking if any modifications have been made...
Executing hello.py...
Output:

Hello world
```

That was a simple hello world program. Next, we can try with deep learning. Note that we don't need to install any python libraries (other than the ones required by pyol) on client side, as long as they are already installed on server side. Pretty neat, eh?

## Known limitations

- No _stdin_ handling yet. Thus, users cannot provide any input.
- Cannot display _stdout_ line-by-line, i.e., we need to wait the execution for the complete output
- pyol execution must be from project's root directory

## License

MIT
