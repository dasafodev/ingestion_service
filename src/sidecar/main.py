from concurrent import futures
import logging

import grpc
from saludtech.pb2py import processed_datas_pb2
from saludtech.pb2py import processed_datas_pb2_grpc


from saludtech.servicios.processed_datas import ProcessedDatas

def agregar_servicios(servidor):
    processed_datas_pb2_grpc.add_ProcessedDatasServicer_to_server(ProcessedDatas(), servidor)

def serve():
    port = '50051'
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agregar_servicios(servidor)

    servidor.add_insecure_port('[::]:' + port)
    servidor.start()
    print("Servidor corriendo por el puerto:" + port)
    servidor.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()