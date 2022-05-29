import sys
sys.path.append("../")

import common_utils as cu
from load_model.util_functions import *
from load_model.model_operation import dataset_list, get_data_path_list, get_data_shape_list


# predict
dataset_name_list = dataset_list()
dataset_path_list = get_data_path_list()
dataset_shape_list = get_data_shape_list()



def learn_all_rankers():
    for i in range(len(dataset_name_list)):
        input_shape = dataset_shape_list[i]
        nb_classes = 2
        tf.set_random_seed(1234)
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        # config.gpu_options.per_process_gpu_memory_fraction = 0.8
        sess = tf.Session(config=config)
        x = tf.placeholder(tf.float32, shape=input_shape)
        y = tf.placeholder(tf.float32, shape=(None, nb_classes))
        model = dnn(input_shape, nb_classes)
        preds = model(x)

        saver = tf.train.Saver()
        model_path = '../model_from_aif360data/' + dataset_name_list[i] + '/999/test.model'
        saver.restore(sess, model_path)
        # construct the gradient graph
        grad_0 = gradient_graph(x, preds)

        # learn ranker
        x_path = dataset_path_list[i] + 'features-train.npy'
        y_path = dataset_path_list[i] + '2d-labels-train.npy'
        x_origin = np.load(x_path)
        y_origin = np.load(y_path)
        ranker_array = np.ndarray((x_origin.shape[0], 2), dtype=np.float32)
        for i in range(x_origin.shape[0]):
            # label_tmp = model_argmax(sess, x, preds, np.array([x_origin[i]]))
            ranker_score = model_probab(sess, x, preds, np.array([x_origin[i]]))
            ranker_array[i] = ranker_score

        #    save result
        np.save('ranker_result_origin/' + dataset_name_list[i] + '/2dims_result.npy', ranker_array)
    print('done with learn all rankers')


if __name__ == '__main__':
    learn_all_rankers()
    print('end')

