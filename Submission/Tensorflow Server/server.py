#Server code from https://github.com/metaflow-ai/blog
#Model Trained in https://github.com/ArunMichaelDsouza/tensorflow-image-detection

import json, argparse, time

import tensorflow as tf

import base64

from flask import Flask, request
from flask_cors import CORS

def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the 
    # unserialized graph_def
    with open(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we import the graph_def into a new Graph and returns it 
    with tf.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.import_graph_def(graph_def, name="prefix")
    return graph

##################################################
# API part
##################################################
app = Flask(__name__)
cors = CORS(app)
@app.route("/api/predict", methods=['POST'])
def predict():
    start = time.time()
    
    data = request.data.decode("utf-8")
    if data == "":
        params = request.form
        x_in = json.loads(params['x'])
    else:
        params = json.loads(data)
        x_in = base64.b64decode(params['x'])
        #x_in = params['x']

    ##################################################
    # Tensorflow part
    ##################################################
    y_out = persistent_sess.run(y, feed_dict={
        x: x_in
        # x: [[3, 5, 7, 4, 5, 1, 1, 1, 1, 1]] # < 45
    })
    ##################################################
    # END Tensorflow part
    ##################################################
    
    json_data = json.dumps({'y': y_out.tolist()})
    print("Time spent handling the request: %f" % (time.time() - start))
    
    return json_data
##################################################
# END API part
##################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen_model_filename", default="results/frozen_model.pb", type=str, help="Frozen model file to import")
    parser.add_argument("--gpu_memory", default=.2, type=float, help="GPU memory per process")
    args = parser.parse_args()

    ##################################################
    # Tensorflow part
    ##################################################
    print('Loading the model')
    graph = load_graph(args.frozen_model_filename)

    #for op in graph.get_operations():
    #    print(op.name)

    x = graph.get_tensor_by_name('prefix/DecodeJpeg/contents:0')
    y = graph.get_tensor_by_name('prefix/final_result:0')

    print('Starting Session, setting the GPU memory usage to %f' % args.gpu_memory)
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=args.gpu_memory)
    sess_config = tf.ConfigProto(gpu_options=gpu_options)
    persistent_sess = tf.Session(graph=graph, config=sess_config)
    ##################################################
    # END Tensorflow part
    ##################################################

    print('Starting the API')
    app.run()