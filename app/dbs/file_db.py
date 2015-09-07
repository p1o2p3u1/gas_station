from flask import g
import socket
import subprocess
import json

server = socket.getfqdn()


def cur_repo_revision(path):
    p = subprocess.Popen(
        ['svn', 'info', path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    info, err = p.communicate()

    version = 0
    for line in info.split('\n'):
        if line.startswith('Revision'):
            version = line[line.index(':') + 1:].strip()
    return version


def query_dirs(path):
    """
    query dirs by server, path, version
    :return:
    """
    version = cur_repo_revision(path)
    sql = "select dirs from dirs where path=%s and server=%s and version=%s"
    data = (path, server, version)
    g.cursor.execute(sql, data)
    rows = g.cursor.fetchall()
    if len(rows) == 0:
        return None
    else:
        return json.loads(rows[0]['dirs'])


def save_dirs(path, result):
    version = cur_repo_revision(path)
    sql = "insert into dirs(path, server, version, dirs) values (%s, %s, %s, %s)"
    data = (path, server, version, json.dumps(result))
    g.cursor.execute(sql, data)
    g.conn.commit()
    return g.cursor.lastrowid


def query_file(path, filename, revision):
    sql = "select source from file where server=%s and path=%s and filename=%s and version=%s"
    data = (server, path, filename, revision)
    g.cursor.execute(sql, data)
    rows = g.cursor.fetchall()
    if len(rows) == 0:
        return None
    else:
        return rows[0]['source']


def save_file(path, filename, revision, source):
    sql = "insert into file (server, path, filename, version, source) values (%s, %s, %s, %s, %s)"
    data = (server, path, filename, revision, source)
    g.cursor.execute(sql, data)
    g.conn.commit()
    return g.cursor.lastrowid


def query_diff(filename, pre_v, cur_v):
    sql = "select diff from diff where filename=%s and pre_version=%s and cur_version=%s"
    data = (filename, pre_v, cur_v)
    g.cursor.execute(sql, data)
    rows = g.cursor.fetchall()
    if len(rows) == 0:
        return None
    else:
        diff = rows[0]['diff']
        return [int(x) for x in diff.split(',')]

def save_diff(filename, pre_v, cur_v, diff):
    sql = "insert into diff (filename, pre_version, cur_version, diff) values (%s, %s, %s, %s)"
    data = (filename, pre_v, cur_v, ','.join(str(x) for x in diff))
    g.cursor.execute(sql, data)
    g.conn.commit()
    return g.cursor.lastrowid
