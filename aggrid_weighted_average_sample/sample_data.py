

import numpy as np
import pandas as pd


def build_data(
        li_client=['client-A', 'client-B', 'client-C'],
        nb_row=20,
        seed=123456):
    """
    """

    np.random.seed(seed)

    clients = np.random.choice(li_client, nb_row)
    levels = np.random.randint(0, 100, nb_row)
    volumes = np.random.randint(1000, 10000, nb_row)
    prices = np.random.randint(100, 1000, nb_row)
    data = {
        'client': clients,
        'level': levels,
        'volume': volumes,
        'price': prices,
    }

    df = pd.DataFrame(data=data)
    return df
