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
* Byteorder
* Content type
* Content encoding
* Content length

#### Content type
The content type returned is the type of which content is inside the message body. This is not the content type of the
message itself. 
Content type should be compliant with the MIME type specification.


## Status codes
### 0 - Fail
Status code 0 means that a generic error occurred. The body is always empty on error.
### 1 - Success
Status code 1 means that the request was successful. A body is supplied. 
### 3 - Not implemented
Staus code 3 means that the requested type is not implemented on the server.
All server implementations should return this on all types that they have not yet implemented. Body is empty.


## Client
### About page
A client should always return a local about page for the url `virgo://about`  
This page should show relevant information about the client and it is up to the creator of the client to decide what is relevant for this page. 
Except for the following information that is required to be shown on the about page,
* Client name and version
* Supported virgo protocol version
* Link to virgo repository

A client can open up a separate window with this information when a user goes the about url but it can also be displayed as a local website.
 
