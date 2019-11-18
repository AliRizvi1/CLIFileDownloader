# Installation

1. Change permissions for executable files by running `chmod +x downloader` and `chmod u+x installer.sh` in your terminal after cloning the repository.
2. Run the installer bash script (`./installer.sh`) in the terminal to download all necessary dependencies. Then you're good to go!
3. In order to run my tests, use `cd tests`, `chmod +x *nameOfTest*`, and finally `./*nameOfTest*`.

# Usage

Usage: `./downloader --c=*Number of Threads* --name=*Name of file* <URL>`

Usage notes: type `./downloader --help` for more information on the usage of the file downloader. --c=X will change the number of threads. This is an optional flag and defaults to one thread. --name=XXX will change the name of the downloaded file, and is also an optional flag.

# Design Notes

Please note: I was unable to test this on a Windows PC as I do not have access to one and have little experience with Windows. Therefore I cannot ensure it runs smoothly on Windows.

I chose to create a file downloader that first splits the file into multiple parts, depending on the number of threads. These threads are run concurrently and will download each individual chunk, which will eventually create the whole file. Threads run in the same memory space and therefore multiple threads may be writing to the same memory simultaneously. I prefer threads to processes because processes take slower to spawn and join, although they have the benefit of not writing to the same memory space.

Scaling:
The number of threads that maximizes performance scales up alongside the file size. Therefore, the program will run much better with large files if a large thread value is chosen. In this way, the program can easily scale, although it is up to the user to choose the number of threads. A fun next step in the project would be to develop a machine learning model that can predict the number of threads that yields maximum performance, including factors such as time elapsed and system resources used.

System resources:
Generally, system resources seem to be increased from a miniscule amount (<1%) to 5-12% on my Macbook laptop. I imagine this depends on the number of concurrent threads as well as the file size.

Virus scanner:
I implemented a virus scanner to protect users against themselves, however this reduced performance and may not scale particularly well. It depends on what this product is being used for - it is for internal downloads that will not have viruses then the performance increase is worth the potential risk, however if this tool will be used to simply download anything off the internet that tradeoff is not worth it. Similarly, most modern operating systems already have a virus scanner, while a VM running Linux may not come with a built-in virus scanner and may need protection. I expect performance is more important variable here and so have decided to comment out all the code relating to the virus scanner. If you would like to implement it, simply uncomment the code and follow instructions online for installing "clamd" and running a "clamav-daemon" on your machine.

# Bottlenecks

Threads seem to increase in value (a.k.a. time saved) as the size of the file increases. In fact, after a certain abritrary point, more threads seem to increase the time it takes. This is likely because there is a small initialization time per thread as well as the time to merge all created threads. The tipping point of when more threads actually increases the time spent depends on the size of the file. Generally, smaller files prefer a lower amount of threads to be optimal, while larger files prefer relatively higher amounts of threads. This can be seen in the tests.

Similarly, due to the fact that files are not always evenly divisible by the number of threads, my program may overwrite a small amount of bits of the file between threads. This is not an issue currently but is not the most efficient use of time.