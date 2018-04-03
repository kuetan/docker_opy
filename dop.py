#!/usr/bin/env python3

import argparse
import docker
import sys

parser = argparse.ArgumentParser(description='help operation docker command..')
parser.add_argument('-p', action='store_true',
                    help='List containers')
parser.add_argument('-e', nargs='+',
                    help='exec [container] [command]')
parser.add_argument('-i', action='store_true',
                    help='List images')
parser.add_argument('-r', metavar='container', nargs='+',
                    help='remove container')
parser.add_argument('-a', action='store_true',
                    help='all flag:True')
parser.add_argument('-f', action='store_true',
                    help='force flag:True')

args = parser.parse_args()

class Docker():
    def __init__(self, allflag, forceflag):
        self.client = docker.from_env()
        self.allflag = allflag
        self.forceflag = forceflag

    def contrainers_list(self):
        clist = self.client.containers.list(all=self.allflag)
        return clist

    def rm(self,clist):
        for container in clist:
            try:
                self.client.remove(container,force=self.forceflag)
            except:
                print("==no container==\n{}".format(container))

    def images_list(self):
        ilist = self.client.images.list(all=self.allflag)
        return ilist

    def exec_run(self,exec_opt):
        """
        exec_opt[0]:container_name
        exec_opt[1]:cmd
        """
        try:
            container = self.client.containers.get(exec_opt[0])
        except:
            print("==no container==\n{}".format(exec_opt[0]))
            sys.exit()
        result = container.exec_run(exec_opt[1],environment=['TERM=xterm'])
        return result[1]

if __name__ == "__main__":
    docker = Docker(args.a, args.f)
    if args.p:
        clist = docker.contrainers_list()
        for container in clist:
            print(container.name)
    if args.i:
        ilist = docker.images_list()
        for image in ilist:
            print(image.tags[0])
    if args.r:
        docker.rm(args.r)
    if args.e:
        print(docker.exec_run(args.e).decode(encoding='utf-8'))
