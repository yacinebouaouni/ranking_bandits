"""Docs

   export pyinstrument=1
   python simulation.py  run    #--dirout 

   ### Check if  
   python simulation.py   test1





"""
import pandas as pd
import numpy as np
import os
import fire
import pyinstrument
from bandits_to_rank.opponents.top_rank import TOP_RANK
from utilmy import (log, os_makedirs, config_load)
from scipy.stats import kendalltau


def binomial_sample(p: float, size: int = 1, n: int = 1):
    return np.random.binomial(n=n, p=p, size=size)


def generate_click_data(cfg: str, T: int, dirout='data_simulation.csv'):
    """
    Generate a dataframe with sampled items and locations with binomial sampling

    Args:
    - cfg: A dictionary containing location_id and their probabilities, item_id and their conditional probabilities
    - T: number of timestamps

    Returns:
    - dataframe: A pandas DataFrame with the following columns:
        - ts: Timestamp (int)
        - loc_id: Location ID (int)
        - item_id: Item ID (int)
        - is_clk: Binary reward (1 for click, 0 for no click) sampled from the given probabilities. (int)
    """
    data = []
    cfg = config_load(cfg)
    cfg = config_load(cfg['probas_json'])
    locations, items = list(cfg['loc_probas'].keys()), list(
    cfg['item_probas'].keys())
    for ts in range(T):
        loc_id    = np.random.choice(locations)
        item_id   = np.random.choice(items)
        loc_prob  = cfg['loc_probas'][loc_id]
        item_prob = cfg['item_probas'][item_id][loc_id]

        is_clk = binomial_sample(item_prob*loc_prob)[0]
        data.append([ts, int(loc_id), int(item_id), is_clk])

    df = pd.DataFrame(data, columns=['ts', 'loc_id', 'item_id', 'is_clk'])
    df.to_csv(dirout, index=False)
    return df

def test_toprank(cfg):
    """
    Simulate and test a TOP_RANK-based recommendation system using a provided dataset.

    Args:
    - cfg (str): Path to the configuration file containing dataset information and other settings.

    Returns:
    None
    """
    
    cfg = config_load(cfg)
    df = pd.read_csv(cfg['dataframe_csv'])

    nb_arms = len(df['item_id'].unique())
    discount_factors = [0.5, 0.5, 0.5]
    T = len(df)
    player = TOP_RANK(nb_arms, T=T, discount_factor=discount_factors)

    # Iterate through the DataFrame rows and simulate game actions
    for _, row in df.iterrows():
        item_id = row['item_id']
        is_clk = row['is_clk']

        # Simulate a game action and reward
        action_list, _ = player.choose_next_arm()
        reward_list = np.where(np.arange(nb_arms) == item_id, is_clk, np.zeros(nb_arms))
        player.update(action_list, reward_list)

    return player

def evaluate_ranking_kendall(player, df):

    clicked_items = df[df['is_clk'] == 1]

    item_click_counts = clicked_items.groupby('loc_id')['is_clk'].sum().reset_index()
    ground_truth_ranking = item_click_counts.sort_values(by='is_clk', ascending=False)['loc_id'].tolist()

    action_list, _ = player.choose_next_arm()
    kendall_tau, _ = kendalltau(ground_truth_ranking, action_list)
    return kendall_tau



def test1():
    ### pytest
    # Generate a sample cfg dictionary and T value
    cfg = {
        'loc_probas': {
            'loc1': 0.5,
            'loc2': 0.3,
            'loc3': 0.2,
        },
        'item_probas': {
            'item1': {'loc1': 0.6, 'loc2': 0.4, 'loc3': 0.2},
            'item2': {'loc1': 0.4, 'loc2': 0.5, 'loc3': 0.3},
        }
    }
    T = 1000

    # Call the generate_click_data function
    df = generate_click_data(cfg, T)
    assert len(df)>0




##########################################################################
def run():
    generate_click_data(cfg= "config.yaml", T=5000)
    df = pd.read_csv('data_simulation.csv')
    player = test_toprank("config.yaml")
    print(f'kendall tau score = {evaluate_ranking_kendall(player, df)}')




if __name__ == "__main__":
    if os.environ.get('pyinstrument', "0") == "1":
        profiler = pyinstrument.Profiler()
        profiler.start()

        fire.Fire()
        profiler.stop()
        print(profiler.output_text(unicode=True, color=True))
    else:
        fire.Fire(main)


