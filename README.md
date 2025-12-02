# Assessment Protocol

## Part 1: Theoretical Fundamentals

1. What is gRPC and why does it work across languages and platforms?

gRPC is a modern open source high performance RPC framework. It works across languages because it relies on Protocol Buffers as a binary Interface Definition Language. A single proto file defines the data and service, which is then compiled into native code for different languages. It uses HTTP/2 for transport, ensuring bidirectional streaming, header compression, and multiplexing across all platforms.

---

2. Describe the RPC life cycle starting with the RPC client?

First, the Client Call invokes a local method known as the stub. Second, Request Marshaling occurs where the client stub serializes the request parameters into a binary Protocol Buffer message. Third, Transport sends the message over the network to the server using HTTP/2. Fourth, Server Unmarshaling receives the message and deserializes it into a language specific object. Fifth, Execution invokes the actual service logic on the server. Finally, the Response follows the reverse path back to the client.

---

3. Describe the workflow of Protocol Buffers?

The first step is Definition, where you define the service interface and message structure in a proto file. The second step is Compilation, where you run the protoc compiler. The third step is Generation, where the compiler generates data access classes and the service base classes for the chosen languages. The fourth step is Implementation, where the developer uses these generated classes to implement the business logic.

---

4. What are the benefits of using protocol buffers?

The binary format is significantly smaller and faster to parse than JSON or XML. It is language agnostic, meaning one definition file generates code for Java, Python, Go, and others. It offers backward compatibility, so fields can be added or deprecated without breaking existing clients. It provides strong typing, which enforces strict data types and reduces runtime errors.

---

5. When is the use of protocol not recommended?

It is not recommended when human readability is a priority, such as needing to debug via simple text tools or read data without decoding tools. It is also less convenient for pure browser based clients where standard JSON and REST are natively supported.

---

**6. List 3 different data types that can be used with protocol buffers?**

- string

- int32

- bool


---

## Part 2: Practical Implementation

**Scenario:** A Hybrid Application with a Java Server and a Python Client.

Step 1: Service Definition

I defined the service HelloWorldService which takes a request containing a first and last name, and returns a greeting text.

File: `src/main/proto/hello.proto`

Protocol Buffers

```
syntax = "proto3";

option java_multiple_files = true;
option java_package = "org.example.grpc";

service HelloWorldService {
  rpc hello (HelloRequest) returns (HelloResponse);
}

message HelloRequest {
  string firstname = 1;
  string lastname = 2;
}

message HelloResponse {
  string text = 1;
}
```

---

Step 2: Java Server Implementation

I used Gradle to manage dependencies and generate the Java source code.

File: `src/main/java/org/example/grpc/HelloWorldServer.java`

Java

```
package org.example.grpc;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;
import java.io.IOException;

public class HelloWorldServer {
    public static void main(String[] args) throws IOException, InterruptedException {
        Server server = ServerBuilder.forPort(50051)
                .addService(new HelloWorldImpl())
                .build();
        System.out.println("JAVA Server started on port 50051...");
        server.start();
        server.awaitTermination();
    }

    static class HelloWorldImpl extends HelloWorldServiceGrpc.HelloWorldServiceImplBase {
        @Override
        public void hello(HelloRequest req, StreamObserver<HelloResponse> responseObserver) {
            String result = "Hello World, " + req.getFirstname() + " " + req.getLastname();
            HelloResponse response = HelloResponse.newBuilder().setText(result).build();
            responseObserver.onNext(response);
            responseObserver.onCompleted();
        }
    }
}
```

---

Step 3: Python Client Implementation

I configured a Python virtual environment and generated the Python gRPC code using grpc_tools.protoc. I placed the client in the resources folder.

File: `src/main/resources/helloWorldClient.py`

Python

```
import grpc
import hello_pb2
import hello_pb2_grpc

def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = hello_pb2_grpc.HelloWorldServiceStub(channel)

        request = hello_pb2.HelloRequest(firstname="Florian", lastname="Marschalek")

        response = stub.hello(request)

        print(response.text)

if __name__ == "__main__":
    main()
```

---

Step 4: Execution and Results

I ran the application in two parallel processes within IntelliJ IDEA.

1. Started the Java Server.

Plaintext

```
JAVA Server started on port 50051...
```

2. Ran the Python Client.

Plaintext

```
Hello World, Florian Marschalek


Process finished with exit code 0
```