# Importing create_app function from the website directory 
from website import create_app

# Creating a Flask App instance 
app = create_app()


if __name__ == "__main__":
    # Running Flask app with the specified parameters
    # debug is set to True, to restart the server automatically when developing
    # port=5901 | you can specify any other port 
    # host="0.0.0.0" to be able to connect to the raspberry pi server from any other device that connected to the same local network 
    # by default, the host is set to localhost and port 5000 => "127.0.0.1:5000" 
    app.run(debug=True, port=5900, host="0.0.0.0")