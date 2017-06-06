#!/usr/bin/env python
"""pacman-mirrors api functions"""

import os
import sys
import tempfile

from . import miscfn
from . import txt


def find_mirrorlist_branch(filename):
    """find and return the branch found in mirrorlist"""
    try:
        with open(filename) as mirrorlist:
            for line in mirrorlist:
                if "Server = " in line:
                    workstring = line.strip()[-21:]  # /unstable/$repo/$arch
                    pos = workstring.find("/")
                    workstring = workstring[pos + 1:]
                    pos = workstring.find("/")
                    return workstring[:pos]
    except OSError as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_READ_FILE,
                                        err.filename,
                                        err.strerror))
        sys.exit(2)


def normalize_config(filename):
    """Normalize configuration"""
    normalize_country(filename)
    normalize_protocols(filename)
    normalize_ssl(filename)


def normalize_country(filename):
    """Write default OnlyCountry = """
    with open(
        filename) as cnf, tempfile.NamedTemporaryFile(
        "w+t", dir=os.path.dirname(
            filename), delete=False) as tmp:
        replaced = False
        for line in cnf:
            if "OnlyCountry =" in line:
                tmp.write("# OnlyCountry =\n")
                replaced = True
            else:
                tmp.write("{}".format(line))
        if not replaced:
            tmp.write("# OnlyCountry =\n")
    os.replace(tmp.name, filename)
    os.chmod(filename, 0o644)


def normalize_protocols(filename):
    """Write default Protocols = """
    with open(
        filename) as cnf, tempfile.NamedTemporaryFile(
        "w+t", dir=os.path.dirname(
            filename), delete=False) as tmp:
        replaced = False
        for line in cnf:
            if "Protocols =" in line:
                tmp.write("# Protocols =\n")
                replaced = True
            else:
                tmp.write("{}".format(line))
        if not replaced:
            tmp.write("# Protocols =\n")
    os.replace(tmp.name, filename)
    os.chmod(filename, 0o644)


def normalize_ssl(filename):
    """Write default SSLVerify = False """
    with open(
        filename) as cnf, tempfile.NamedTemporaryFile(
        "w+t", dir=os.path.dirname(
            filename), delete=False) as tmp:
        replaced = False
        for line in cnf:
            if "SSLVerify =" in line:
                tmp.write("# SSLVerify = False\n")
                replaced = True
            else:
                tmp.write("{}".format(line))
        if not replaced:
            tmp.write("# SSLVerify = False\n")
    os.replace(tmp.name, filename)
    os.chmod(filename, 0o644)


def sanitize_prefix(prefix):
    """Sanitize prefix
    :param prefix:
    :returns sanitized prefix
    """
    if prefix.endswith("/"):
        prefix = prefix[:-1]
    return prefix


def sanitize_url(url):
    """Sanitize url
    :param url:
    :returns sanitized url
    """
    if not url.endswith("/"):
        url = url + "/"
    return url


def write_config_branch(branch, filename, quiet=False):
    """Write branch"""
    if branch == "stable":
        branch = "# Branch = stable\n"
    else:
        branch = "Branch = {}\n".format(branch)
    try:
        with open(
            filename) as cnf, tempfile.NamedTemporaryFile(
            "w+t", dir=os.path.dirname(
                filename), delete=False) as tmp:
            replaced = False
            for line in cnf:
                if "Branch =" in line:
                    tmp.write(branch)
                    replaced = True
                else:
                    tmp.write("{}".format(line))
            if not replaced:
                tmp.write(branch)
        os.replace(tmp.name, filename)
        os.chmod(filename, 0o644)
        if not quiet:
            print(".: {} {}".format(txt.INF_CLR, txt.API_CONF_RE_BRANCH))
    except OSError as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_READ_FILE,
                                        err.filename,
                                        err.strerror))
        sys.exit(2)


def write_mirrorlist_branch(newbranch, filename, quiet=False):
    """"""
    branch = find_mirrorlist_branch(filename)
    try:
        with open(filename) as mirrorlist, tempfile.NamedTemporaryFile(
            "w+t", dir=os.path.dirname(
                filename), delete=False) as tmp:
            for line in mirrorlist:
                if "Server =" in line:
                    line = line.replace(branch, newbranch)
                    tmp.write("{}".format(line))
                else:
                    tmp.write("{}".format(line))
        os.replace(tmp.name, filename)
        os.chmod(filename, 0o644)
        if not quiet:
            print(".: {} {}".format(txt.INF_CLR, txt.API_MIRRORLIST_RE_BRANCH))
    except OSError as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_READ_FILE,
                                        err.filename,
                                        err.strerror))
        sys.exit(2)


def write_protocols(protocols, filename, quiet=False):
    """Write branch"""
    if protocols:
        protocols = "Protocols = {}\n".format(",".join(protocols))
    else:
        protocols = "# Protocols = \n"
    try:
        with open(
            filename) as cnf, tempfile.NamedTemporaryFile(
            "w+t", dir=os.path.dirname(
                filename), delete=False) as tmp:
            replaced = False
            for line in cnf:
                if "Protocols =" in line:
                    tmp.write(protocols)
                    replaced = True
                else:
                    tmp.write("{}".format(line))
            if not replaced:
                tmp.write(protocols)
        os.replace(tmp.name, filename)
        os.chmod(filename, 0o644)
        if not quiet:
            print(".: {} {}".format(txt.INF_CLR, txt.API_CONF_PROTOCOLS))
    except OSError as err:
        print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                        txt.CANNOT_READ_FILE,
                                        err.filename,
                                        err.strerror))
        sys.exit(2)
