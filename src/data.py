import numpy as np

# set random seed for random and numpy packages
SEED = 4
np.random.seed(SEED)


def get_data(path_data):
    """
    Split the raw sessions into training sessions for p2v and mp2v and a common test set.

        path_data: str
        Path to .npy file with shape (nb_sessions,) containing a list of strings
            ['track_0', 'artist_0', ..., 'track_n', 'artist_n']
        in each column.
    """

    # load data
    sessions_raw = np.load(path_data)

    # for p2v get only 'track' items
    if sessions_raw[0][0].startswith('track'):
        sess_p2v = [[x for x in s if x.startswith('track')] for s in sessions_raw]
    else:
        sess_p2v = [s[0::2] for s in sessions_raw]
    # use (1 st, ..., n-1 th) items from sess_p2v to form the train set (drop last 'track' item)
    train_p2v = [sess[:-1] for sess in sess_p2v]

    # sub-sample 10k sessions, and use (n-1 th, n th) pairs of items from sess_p2v to form the disjoint
    # validaton and test sets
    if path_data.endswith('ecommerce_sessions.npy'):
        test_validation = [sess[-2:] for sess in sess_p2v]
        index = np.random.choice(range(len(test_validation)), 2000, replace=False)
        test = np.array(test_validation)[index[:1000]].tolist()
        validation = np.array(test_validation)[index[1000:]].tolist()
    else:
        test_validation = [sess[-2:] for sess in sess_p2v]
        index = np.random.choice(range(len(test_validation)), 20000, replace=False)
        test = np.array(test_validation)[index[:10000]].tolist()
        validation = np.array(test_validation)[index[10000:]].tolist()

    # for mp2v get all ('track' and 'artist') items
    sess_mp2v = sessions_raw.tolist()
    # use (1 st, ..., n-2 th) items from sess_mp2v to form the train set (drop last 'track' and 'artist' items)
    train_mp2v = [sess[:-2] for sess in sess_mp2v]

    return train_p2v, train_mp2v, validation, test
