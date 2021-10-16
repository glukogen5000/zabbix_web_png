import hashlib
import requests
from bottle import Bottle, run, abort
from bottle import response
from bottle import static_file
import config



def graph(id, dt="", size=""):
    requests.packages.urllib3.disable_warnings()

    data_api = {"name": str(config.user), "password": str(config.password), "enter": "Sign in"}
    auth = requests.post(config.server, data=data_api, verify=False,
                         auth=requests.auth.HTTPBasicAuth(str(None), str(None)))
    cookie = auth.cookies
    if size:
        z_size = "&width=" + str(size)
    else:
        z_size = ""
    if dt:
        z_dt = "&from=now-"+dt+"&to=now"
    else:
        z_dt = ""
    server_str = config.server + "chart2.php?graphid=" + str(id) + z_size + z_dt + "&profileIdx=web.graphs.filter"
    # chart6 круговая
    # print(server_str)
    zapros = requests.get(server_str, cookies=cookie, verify=False)
    # print(zapros.status_code)

    # image_hash = hashlib.md5()
    # file_img = "external_{0}.png".format(image_hash.hexdigest())
    res_img = zapros.content
    response.content_type = 'image/png'
    return res_img

app = Bottle()

@app.route('/graph/<id:int>')
def graf1(id):
    return graph(id)


@app.route('/graph/<id:int>/<dt>')
def date(id,dt):
    return graph(id,dt)


@app.route('/graph/<id:int>/<dt>/<size>')
def size(id,dt,size):
    return graph(id, date, size)

# with open(file_img, "wb") as fd:
#         fd.write(res_img)


#
# @app.route('/err')
# def err():
#     abort(401, 'My Err')
#
# def file_bwrite(filename, data):
#     with open(filename, "wb") as fd:
#         fd.write(data)
#     return True

# @app.route('/static/<filename:path>')
# def send_static(filename):
#     return static_file(filename, root="C:\Users\user\PycharmProjects\zabbix_api")


if __name__ == '__main__':
    app.run(host='localhost', port=8080, quiet=True, debug=True)
