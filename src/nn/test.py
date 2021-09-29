import json

from dataset import create_bin_dataloader
from model import Model


def test(model : Model, positive_path, negative_path, metrics_path):
    """
    Test the Model of the NN 
    Args: 
        model : the model of the NN
        positive_path : path to test crossed boxes
        negative_path : path to test not-crossed boxes
        metrics_path : path to save test metrics
    """
    # Test Loader
    test_dataloader = create_bin_dataloader(positive_path, negative_path, 1)

    p = 0
    n = 0
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    al = 0
    for i, (img, target) in enumerate(test_dataloader):
        if i % 1000:
            print(f"TEST: {i} / {len(test_dataloader)}")
        pred = model.forward(img[0])
        al += model.compute_loss(pred, target[0])
        if pred[0][0] > pred[0][1]:
            if target[0][0] == 1:
                tn += 1
                n += 1       
            else:
                fn +=1 
                p += 1
        else:
            if target[0][0] == 1:
                fp += 1
                n += 1       
            else:
                tp +=1 
                p += 1
    al /= len(test_dataloader)

    metrics = dict()
    metrics["average loss"] = al
    if tp == 0:
        metrics["precision"] = 0
        metrics["recall(true positive rate)"] = 0
    else:    
        metrics["precision"] = tp / (tp + fp)
        metrics["recall(true positive rate)"] = tp / (tp + fn)
    if tn == 0:
        metrics["true negative rate"] = 0
    else:    
        metrics["true negative rate"] = tn / (tn + fp)

    f = open(metrics_path, "w")
    f.write(json.dumps(metrics))
    f.close()

