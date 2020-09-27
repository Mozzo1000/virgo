# virgo protocol specification
The specification for the virgo protocol is still in the planning phase and will change drastically in a short amount of time.

## Message
There are two types of messages, a posted message and recieved message.
Most likely a client is looking to recieve a message, in the specification this is called, aquire.

A message consists of three parts, a type, a file and metadata. And is formatted in JSON.
The metadata portion is semi optional and should always be set to None if not in use.

Example: 

`{"type": "aquire", "file": "main.md", "metadata": "None"}`

This example will send a message to the server that the client is looking for the file with the name `main.md`


### aquire message
A `aquire` message is used from the client to the server. The client tells the server that it is looking for a specific file.
If no file is specified, the message will default to `main`.
#### response
The response for a `aquire` message should be json encoded and consist of two parts, status and body.

Example: 
`{"status": 1, "body": "hello"}`

### post message
A `post` message is sending information to the server for further processing on the server side.

### Header
With every message there is a header sent with it. This header consists of four parts:
* Byteorder -
* Content type - 
* Content encoding - 
* Content length -

## Status codes
### 0 - Fail
Status code 0 means that a generic error occurred. The body is always empty on error.
### 1 - Success
Status code 1 means that the request was successful. A body is supplied. 