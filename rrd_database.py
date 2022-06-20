import rrdtool
import random
import os


def create_database(ip_address, type_data, data_size):
    database_dir = os.getcwd() + "/data/devices_files/" + ip_address
    params = [database_dir + "/" + type_data + ".rrd"]
    params += ["--start", 'N']
    params += ["--step", '5']
    if data_size > 0:
        for i in range(data_size):
            params += ["DS:" + type_data + str(i) + ":GAUGE:5:U:U"]
        for i in range(data_size):
            params += ["RRA:AVERAGE:0.5:1:100"]
    else:
        params += ["DS:" + type_data + ":GAUGE:5:U:U"]
        params += ["RRA:AVERAGE:0.5:1:100"]

    result = rrdtool.create(params)

    if result:
        print(rrdtool.error())


def update_database(ip_address, type_data, value):
    database_dir = os.getcwd() + "/data/devices_files/" + ip_address + "/" + type_data + ".rrd"
    rrdtool.update(database_dir, value)
    # graph_detection(ip_address, type_data, max_value)


def graph_detection(ip_address, type_data, values, minuts, title, label):
    database_dir = os.getcwd() + "/data/devices_files/" + ip_address + "/" + type_data + ".rrd"
    image_output = os.getcwd() + "/data/devices_files/" + ip_address + "/"

    last_update = int(rrdtool.last(database_dir))
    start_time = last_update - int(minuts)

    params = (str(image_output) + "detection_" + type_data + ".png",
              "--start", str(start_time),
              "--end", str(last_update),
              "--vertical-label=" + type_data,
              '--lower-limit', '0',
              "--title=" + title,)

    if values > 0:
        for i in range(values):
            params += ("DEF:value" + str(i) + "=" + str(database_dir) + ":" + str(type_data) + str(i) + ":AVERAGE",)
            params += ("CDEF:valueprint" + str(i) + "=value" + str(i) + ",8,*",)
            params += ("LINE" + str(i) + ":valueprint" + str(i) + "#" + ''.join([random.choice('ABCDEF0123456789') for j in range(6)]) + ":" + label[i],)
    else:
        params += ("DEF:value=" + str(database_dir) + ":" + str(type_data) + ":AVERAGE",)
        params += ("CDEF:valueprint=value,8,*",)
        params += ("LINE:valueprint#FF0000:" + label[0],)

    ret = rrdtool.graph(*params)
