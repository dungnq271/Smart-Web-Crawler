import numpy as np


def pagerank(trans_mat, num_iterations: int = 100, d: float = 0.85):
    n = len(trans_mat)
    v = np.ones((n, 1), dtype=np.float64) / n
    out_edges = np.sum(trans_mat, axis=1, keepdims=True)
    np.place(out_edges, out_edges == 0, [1])
    trans_mat = trans_mat / out_edges
    trans_mat = trans_mat.T
    uni_mat = 1. / n * np.ones((n, n))
    M = d * trans_mat + (1 - d) * uni_mat
    for _ in range(num_iterations):
        v = M @ v
    return v


def rank_pages(priorities: np.ndarray, data):
    priorities = priorities.flatten()
    priorities = np.argsort(priorities) + 1
    upd_data = {}
    for i, (k, v) in enumerate(data.items()):
        upd_data[k] = v
        upd_data[k]['prestige'] = str(priorities[i])
    sort_data = dict(sorted(upd_data.items(), key=lambda x: int(x[1]['prestige']), reverse=True))
    filtered = {k: v for k, v in sort_data.items() if v['sentences'][0] is not None}
    sort_data.clear()
    sort_data.update(filtered)
    del data
    return sort_data


def hits():
    pass
