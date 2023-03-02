# Server-Client with Cache

The objective of this project is to create a server-client system with caching.

## Architecture

The project is divided into two files, one for the client and one for the server. The client sends the name of the file it wants, and the server initially returns the file size and additional data to the client. After that, the server returns the requested file data.

The transfer progress is displayed using a progress bar created by the `tqdm` library.

The `socket` library in Python was used for creating and connecting the client and server, along with the `sys` and `os` libraries for auxiliary functions such as file size and parameter passing.

The `_thread` and `threading` libraries were used for managing threads and file locking.

## Server

The development of the server was done in parts, starting with the basic function of serving files to the client. After that, the code was divided into threads, and a cache system was implemented with a search in the cache before opening the files to be served. After the cache was implemented and tested, locking and log cleaning were added.

### Server Usage

With Python installed, run the following command to start the server: `python server.py port directory_of_files_to_share`

## Client

For the client, only minor changes were made over time, with the progress bar being added.

### Client Usage

To list the files on the server, run: `python client.py host port list`

To download files, run: `python client.py host port directory_of_file directory_to_save`
