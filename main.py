import os
import logging

from domainadaptation.experiment import DANNExperiment

if __name__ == '__main__':

    # disable useless tf warnings
    logging.disable(logging.WARNING)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    experiment = DANNExperiment(config={
        'backbone': {
            'type': 'alexnet',
            'num_trainable_layers': 2,
            'img_size': (224, 224),
            'weights': 'imagenet',
            'pooling': 'max'
        },
        'dataset': {
            'classes': 12,
            'path': '/data/eikolodin/visda',
            'augmentations': {},
            'source': 'train',
            'target': 'validation'
        },
        'batch_size': 16,
        'learning_rate': 3e-4,
        'epochs': 2,
    })

    experiment()
