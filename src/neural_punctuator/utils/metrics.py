import logging
import sys
from sklearn.metrics import classification_report, confusion_matrix, f1_score, roc_auc_score, precision_score, recall_score
import numpy as np

from src.neural_punctuator.utils.visualize import plot_confusion_matrix

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-9s %(message)s'))

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(handler)

# TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
output_dim = 4

def get_eval_metrics(targets, preds, config=None):
    # TODO: get the desired metric list from config.yaml
    """
    Calculates metrics on validation data
    """
    metrics = {}

    preds = np.exp(preds)
    preds = preds.reshape(-1, output_dim)
    targets = targets.reshape(-1)
    pred_index = preds.argmax(-1)
    cls_report = get_classification_report(targets, pred_index)

    print(cls_report)

    # if 'precision' in self._config.trainer.metrics:

    if True:
        macro_precision = precision_score(targets, pred_index, average='macro')
        log.info(f'Macro precision is: {macro_precision}')
        metrics['precision'] = macro_precision
    # if 'recall' in self._config.trainer.metrics:
    if True:
        macro_recall = recall_score(targets, pred_index, average='macro')
        log.info(f'Macro recall is {macro_recall}')
        metrics['recall'] = macro_recall
    # if 'f_score' in self._config.trainer.metrics:
    if True:
        macro_f1_score = f1_score(targets, pred_index, average='macro')
        log.info(f'Macro f-score is {macro_f1_score}')
        metrics['f_score'] = macro_f1_score
    # if 'auc' in self._config.trainer.metrics:
    if True:
        auc_score = roc_auc_score(targets, preds, average='macro', multi_class='ovo')
        log.info(f'AUC is: {auc_score}')
        metrics['auc'] = auc_score

    # if self._config.trainer.visualize_conf_mx:
    if True:
        conf_mx = get_confusion_mx(targets, pred_index)
        plot_confusion_matrix(conf_mx)

    return metrics


def get_classification_report(targets, preds):
    return classification_report(targets, preds, digits=3)


def get_confusion_mx(targets, preds):
    return confusion_matrix(targets, preds)


def get_total_grad_norm(parameters, norm_type=2):
    total_norm = 0
    parameters = list(filter(lambda p: p.grad is not None, parameters))
    for p in parameters:
        param_norm = p.grad.data.norm(norm_type)
        total_norm += param_norm.item() ** norm_type
    return total_norm ** (1. / norm_type)
