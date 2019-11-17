# Installation

1. Change permissions for executable by running `chmod +x downloader` in your terminal after cloning the repository.

#Usage

Usage: ./downloader --c=*Number of Threads* --name=*Name of file* <URL>

Notes: type ./downloader --help for more information on the usage of the file downloader. --c=X will change the number of threads. This is an optional flag and defaults to one thread. --name=XXX will change the name of the downloaded file. This is a mandatory flag (an error will occur if the name is not given, so please change your autotests to incorporate this).

#Design Notes

I chose to create a file downloader that first splits the file into multiple parts, depending on the number of threads. These threads are run concurrently and will download each individual chunk. 

# Notes

Threads seem to increase in value as the size of the file increases. In fact, for a very small picture (i.e. <100KB) more threads seem to increase the time it takes. This is likely because there is a small initialization time per thread.

Todo:
1. Implement virus scanner https://pypi.org/project/clamd/