from flask import Flask, request, send_file, render_template
import datetime

app = Flask(__name__)

@app.route('/<string:img_name>')
def index(img_name):
    last_image = request.cookies.get('last_image')
    user_agent = request.headers.get('User-Agent')
    timestamp = str(datetime.datetime.now())
    ip = str(request.remote_addr)
    
    with open('user_agents.txt', 'a') as f:
        f.write(user_agent + ' - ' + timestamp + ' - ' + ip + '\n')
    try:
        if last_image == img_name:
            img_name2 = "orso.JPG"
        else:
            img_name2 = img_name
        response = make_response(send_file(img_name2))
        response.headers.set('Content-Type', 'image/jpeg')
        response.set_cookie('last_image', img_name)
        return response
    except FileNotFoundError:
        return 'Image not found', 404

@app.route('/user_agents')
def user_agents():
    with open('user_agents.txt', 'r') as f:
        user_agents = f.readlines()
    return render_template('user_agents.html', user_agents=user_agents)

if __name__ == '__main__':
    app.run(debug=True)