from typing import List
import os
import shutil

def gen_paths(prefix: str, number_of_nodes: int) -> List:
    return list(map(lambda x : prefix+str(x+1), range(number_of_nodes)))

def make_path(path: str) -> bool:
    if not os.path.isdir(path):
        os.mkdir(path)
    return True

def check_paths(path: str) -> bool:
    return make_path(path) and make_path(path+"/conf") and make_path(path+"/logs") and make_path(path+"/data")

def load_config(filename):
    config_dict = dict()
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0 or line[0] == "#":
                continue
            flds = line.split("=")
            config_dict[flds[0]]=flds[1]
    return config_dict

def save_config(path: str, config, id: int) -> bool:
    with open(path, 'w') as out:
        if "broker.id" in config:
            config["broker.id"] = str(id)
        hostname = "kafka-"+str(id)
        for k,v in config.items():
            if k == "advertised.listeners" or k == "listeners":
                out.write(k+"="+v.format(hostname)+"\n")
            else:
                out.write(k+"="+v+"\n")

kafka_paths = gen_paths("kafka-", 4)
zk_paths = gen_paths("zk-", 3)

kk_config = load_config("kafka-server.properties")
for path in kafka_paths:
    if check_paths(path):
        shutil.copyfile("kafka-log4j.properties", path+"/conf/log4j.properties")
        save_config(path+"/conf/server.properties", kk_config, int(path[-1]))

for path in zk_paths:
    if check_paths(path):
        shutil.copyfile("zoo.cfg", path+"/conf/zoo.cfg")
        shutil.copyfile("zk-log4j.properties", path+"/conf/log4j.properties")
        shutil.copyfile("configuration.xsl", path+"/conf/configuration.xsl")
        with open(path+"/data/myid", 'w') as out:
            out.write(path[-1])

