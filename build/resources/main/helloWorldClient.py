import sys
import grpc

import hello_pb2 as hello_pb2
import hello_pb2_grpc as hello_pb2_grpc


def main():
    firstname = sys.argv[1] if len(sys.argv) > 1 else "Omar"
    lastname = sys.argv[2] if len(sys.argv) > 2 else "Hemida"

    # Connect to server
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = hello_pb2_grpc.HelloWorldServiceStub(channel)
        request = hello_pb2.HelloRequest(firstname=firstname, lastname=lastname)
        response = stub.hello(request)
        print()
        print(response.text)
        print()

if __name__ == "__main__":
    main()