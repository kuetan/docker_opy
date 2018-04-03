#!/usr/bin/env python3

import argparse
import docker

parser = argparse.ArgumentParser(description='help operation docker command..')
parser.add_argument('-p', action='store_true',
                    help='List containers')
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
