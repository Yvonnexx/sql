#!/usr/bin/python
import xml.etree.ElementTree as ET
import sys
from lxml import etree
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy import func 
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

app = Flask(__name__)

engine = create_engine('mysql://root:root@localhost/mydb')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False , bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)

class Node(Base):
    __tablename__ = 'Node'
    id = Column(Integer, primary_key=True)
    status = Column(String(50), unique=False)
    server_type = Column(String(50), unique=False)
    bus_type = Column(String(50), unique=False)
    hostname = Column(String(50), unique=False)
    username = Column(String(50), unique=False)
    tags = Column(String(50), unique=False)
    t = Column(String(50), unique=False)
    description = Column(String(50), unique=False)
    platform = Column(String(50), unique=False)

    def __init__(self, status=None, server_type=None, bus_type=None, hostname=None, username=None, tags=None, t=None, description=None, platform=None):
        self.status = status
        self.server_type = server_type
        self.bus_type = bus_type
        self.hostname = hostname
        self.username = username
        self.tags = tags
        self.t = t
        self.description = description
        self.platform = platform

class Database(Base):
    __tablename__ = 'database_info'
    id = Column(Integer, primary_key=True)
    db_cluster_type = Column(String(50), unique=False)
    db_name = Column(String(50), unique=False)
    db_type = Column(String(50), unique=False)

    def __init__(self, db_cluster_type=None, db_name=None, db_type=None):
        self.db_cluster_type = db_cluster_type
        self.db_name = db_name
        self.db_type = db_type

class DataCenter(Base):
    __tablename__ = 'data_center'
    id = Column(Integer, primary_key=True)
    data_center = Column(String(50), unique=False)
    data_center_site_type = Column(String(50), unique=False)

    def __init__(self, data_center=None, data_center_site_type=None):
        self.data_center = data_center
        self.data_center_site_type = data_center_site_type

class OS(Base):
    __tablename__ = 'os'
    id = Column(Integer, primary_key=True)
    osArch = Column(String(50), unique=False)
    osFamily = Column(String(50), unique=False)
    osName = Column(String(50), unique=False)
    osVersion = Column(String(50), unique=False)

    def __init__(self, osArch=None, osFamily=None, osName=None, osVersion=None):
        self.osArch = osArch
        self.osFamily = osFamily
        self.osName = osName
        self.osVersion = osVersion

class PatchRelease(Base):
    __tablename__ = 'patch_release'
    id = Column(Integer, primary_key=True)
    last_patch_date = Column(String(50), unique=False)
    patch_group = Column(String(50), unique=False)
    release_group = Column(String(50), unique=False)
    last_release_date = Column(String(50), unique=False)
    
    def __init__(self, last_patch_date=None, patch_group=None, release_group=None, last_release_date=None):
        self.last_patch_date = last_patch_date
        self.patch_group = patch_group
        self.release_group = release_group
        self.last_release_date = last_release_date

class App(Base):
    __tablename__ = 'application'

    id = Column(Integer, primary_key=True)
    role = Column(String(50), unique=False)
    app_environment = Column(String(50), unique=False)

    def __init__(self, role=None, app_environment=None):
        self.role = role
        self.app_environment = app_environment

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')
    
@app.route('/app', methods=['GET'])
def myapp():
    host = request.args.get('hostname')
    result = db_session.query(Node).filter_by(hostname=host).first()
    return result.platform + "\t" + result.username

@app.route('/generate', methods=['GET'])
def generate():
    root = ET.Element("project")
    result_app = db_session.query(App).all()
    result_database = db_session.query(Database).all()
    result_data_center = db_session.query(DataCenter).all()
    result_node = db_session.query(Node).all()
    result_os = db_session.query(OS).all()
    result_patch_release = db_session.query(PatchRelease).all()
    length = 0
    role = []
    app_environment = []
    db_cluster_type = []
    db_name = []
    db_type = []
    for i in result_app:
        print i.id, i.role, i.app_environment
        role.append(i.role)
        app_environment.append(i.app_environment)
        length += 1
    for i in result_database:
        db_cluster_type.append(i.db_cluster_type)
        db_name.append(i.db_name)
        db_type.append(i.db_type)
    data_center = []
    data_center_site_type = []
    for i in result_data_center:
        data_center.append(i.data_center)
        data_center_site_type.append(i.data_center_site_type)
    status = []
    server_type = []
    bus_type = []
    hostname = []
    username = []
    tags = []
    t = []
    description = []
    platform = []
    for i in result_node:
        status.append(i.status)
        server_type.append(i.server_type)
        bus_type.append(i.bus_type)
        hostname.append(i.hostname)
        username.append(i.username)
        tags.append(i.tags)
        t.append(i.t)
        description.append(i.description)
        platform.append(i.platform)
    osArch = []
    osFamily = []
    osName = []
    osVersion = []
    for i in result_os:
        osArch.append(i.osArch)
        osFamily.append(i.osFamily)
        osName.append(i.osName)
        osVersion.append(i.osVersion)
    last_patch_date = []
    patch_group = []
    release_group = []
    last_release_date = []
    for i in result_patch_release:
        last_patch_date.append(i.last_patch_date)
        patch_group.append(i.patch_group)
        release_group.append(i.release_group)
        last_release_date.append(i.last_release_date)

    for i in xrange(length):
        node = ET.SubElement(root, "node")
        node.set("role", role[i])
        node.set('app_environment', app_environment[i])
        node.set('db_cluster_type', db_cluster_type[i])
        node.set('db_name', db_name[i])
        node.set('db_type', db_type[i])
        node.set('data_center', data_center[i])
        node.set('data_center_site_type', data_center_site_type[i])
        node.set('status', status[i])
        node.set('server_type', server_type[i])
        node.set('bus_type', bus_type[i])
        node.set('hostname', hostname[i])
        node.set('username', username[i])
        node.set('tags', tags[i])
        node.set('type', t[i])
        node.set('description', description[i])
        node.set('platform', platform[i])
        node.set('osArch', osArch[i])
        node.set('osFamily', osFamily[i])
        node.set('osName', osName[i])
        node.set('osVersion', osVersion[i])
        node.set('last_patch_date', last_patch_date[i])
        node.set('patch_group', patch_group[i])
        node.set('release_group', release_group[i])
        node.set('last_release_date', last_release_date[i])
    tree = ET.ElementTree(root)
    """
    root_test = tree.getroot()
    for child in root_test:
        print child.attrib['role'] +'\t' + child.attrib['app_environment']
    """
    tree.write("test.xml")
    return "successfully generate xml files"

@app.route('/create', methods=['GET'])
def create_role():
    r = request.args.get('role')
    app_env = request.args.get('app_env')
    data_center = request.args.get('data_center')
    status = request.args.get('status')
    patch_group = request.args.get('patch_group')
    release_group = request.args.get('release_group')
    db_cluster_type = request.args.get('db_cluster_type')
    server_type = request.args.get('server_type')
    bus_type = request.args.get('bus_type')
    db_type = request.args.get('db_type')
    bus_type = request.args.get('bus_type')
    hostname = request.args.get('hostname')
    username = request.args.get('username')
    tags = request.args.get('tags')
    t = request.args.get('t')
    description = request.args.get('description')
    db_name = request.args.get('db_name')
    data_center = request.args.get('data_center')
    osArch = request.args.get('osArch')
    osFamily = request.args.get('osFamily')
    osName = request.args.get('osName')
    osVersion = request.args.get('osVersion')
    last_patch_date = request.args.get('last_patch_date')
    last_release_date = request.args.get('last_release_date')
    data_center_site_type = request.args.get('data_center_site_type')
    platform = request.args.get('platform')
    new_data_app = App(role=r, app_environment= app_env)
    new_data_database_info = Database(db_cluster_type=db_cluster_type, db_name=db_name, db_type=db_type)
    db_session.add(new_data_database_info)
    db_session.add(new_data_app)
    new_data_data_center = DataCenter(data_center=data_center, data_center_site_type=data_center_site_type)
    db_session.add(new_data_data_center)
    new_data_node = Node(status=status, server_type=server_type, bus_type=bus_type, hostname=hostname, username=username, tags=tags, t = t, description=description, platform=platform)
    db_session.add(new_data_node)
    new_data_os = OS(osArch=osArch, osFamily=osFamily, osName=osName, osVersion=osVersion)
    db_session.add(new_data_os)
    new_data_patch_release = PatchRelease(last_patch_date=last_patch_date, patch_group=patch_group, release_group=release_group, last_release_date=last_release_date)
    db_session.add(new_data_patch_release)
    try:
        db_session.commit()
    except:
        db_session.rollback()
    #return str(new_data_app.id) + "\t\t" + new_data_app.app_environment +"\t\t" + new_data_app.role
    return "successfully inserted into the database"

@app.route('/add/<a>/<b>', methods=['GET'])
def add(a,b):
    return str(a+b)

if __name__ == '__main__':
    app.run(debug=True)
