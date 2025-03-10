<!-- Our title -->
<div align="center">
  <h3>ranking_bandits </h3>
</div>

<!-- Short description -->
<p align="center">
A Python-toolkit for bandit algorithms choosing a ranked-list of $K$ items among $L$ at each iteration


at every time step t,
    choose K items out of a list of L items
    ranking problems at each time t.

    To focus:
       Top Rank (ie)

    Data wrapper.


Need to 
    Model State Save, Model State load in pickle.   ONLY for TopRank

    All code is numpy --> in dictionary ---> pickle.


</p>





```
Next step:


   Player --> action        ENV: reward

 Setup an environnment easy to use
 and DECOUPLE from player.


Binomial sampling for click. P =0.12 
  ---> Truth dataframe
  ---> use this dataframe as FIXED enviroonment ( == Truth)
        isclik

  ---> run the playe agasint this ENV
  ---> check convergence of the Best.


#### Sampling dataframe + run the timestep simulation 

At each time:
   Select K items out of L items.

       --> check if those items are clicked or not (reward_list = [0,0,1,0,0 ]

      ,ts: timestamp in int
      ,loc_id : location_id
      ,item_id:  
      ,is_clk :  reward 1/0 of the action.

 At each time step,
    loc_id: L items
    Select K items out of L items of loc_id


   Proba( Loc_id= L0 has one click) = Ploc

   Proba( item=i of Loc_id=L0) =  Proba(item=i/L0) * Ploc



USER Input:
    loc_id_1 --> proba_1 (sample as binomial)     ,  
    loc_id_2 --> proba_2 (sample as binomial)
    loc_id_k --> proba_k (sample as binomial)


   #### L items in total
       proba( click on item A / Loc_id_1 ) = P(A/1)
       proba( click on item B / Loc_id_1 ) = P(B/1)
       proba( click on item C / Loc_id_1 ) = P(C/1)


       proba( click on item A / Loc_id_2 ) = P(A/2)
       proba( click on item B / Loc_id_2 ) = P(B/2)
       proba( click on item C / Loc_id_2 ) = P(C/2)


OUTPUT IS: 
      ,ts: timestamp in int
      ,loc_id : location_id
      ,item_id:  
      ,is_clk :  reward 1/0  is Sampled from.   Proba_1 * Proba(item_id/1) (Binomial sampling )



def generate_sample_1(cfg)--> dataframe



def simulate_toprank(df):  --> dfsimul (agent actual action)




def simulate_check(dftrue, dfsimul):  --> dataframe loation_id ,  score


   scipy.kendall.
   Score: Kendall correl between lists, ranking metrics ?



    Thruth
    Validation ranking of condtional per Location_id
    loc_id_1 :  Best ranking list 1       P(item 1 / loc_id_1),  P(item 2 / loc_id_1),  
    loc_id_2 :  Best ranking list 2
    loc_id_k :  Best ranking list k


#####
dfsample.groupby('location_id, item_iud).agg('imp')
dfsample.groupby('location_id, item_iud).agg('true')

    ctr = click / imp  = proba of binomial






```



```
#### New conda env 
pip install -r reqs.txt


### Data sample
      ,ts: timestamp in int

      ,loc_id : location_id
      ,item_id:  
      ,user_id:  Not used here
      ,is_clk :  reward 1/0 of the action.

      Location_id ----> a list of L items.
      At each time step ts,     
         we choose K item_id out of each location_id (zipcode)

####
    Bernoulli sample of each item_id



#### trace code
   pip install pyinstrument 
       Function call ---> easy to track what is called.




##### run code
source activate bandit

TESTDIR=`pwd`/test
DATA_FNAME=`pwd`/hist.csv
mkdir $TESTDIR
mkdir $TESTDIR/dev_null
mkdir $TESTDIR/dev_null_bis

set -x

### run Bandit Env simulation ---> output files on disk
python exp.py --play 2 100 -r 10 --csv $DATA_FNAME --TopRank 100 --horizon_time_known $TESTDIR/dev_null --force || exit


### Merge the output files
python exp.py --merge 100 -r 10 --csv $DATA_FNAME --TopRank 100 --horizon_time_known $TESTDIR/dev_null || exit








##### Experiment with Top rank

    ### run the simulation
       python exp.py --play 2 100 -r 10 --csv $DATA_FNAME --TopRank 100 --horizon_time_known $TESTDIR/dev_null --force || exit

       ---> generates  2 files : 1 for each play/run.
             logs/  simulation.zip 
                    simulation. : sample headers.


    ###  Merging output file into 1 single one
       python exp.py --merge 100 -r 10 --csv $DATA_FNAME --TopRank 100 --horizon_time_known $TESTDIR/dev_null || exit

            output is : 1 file merging previous simulation play file.



   ### exp.py :  
      setup config param.py









```


```
TODO

Bandit Recommendation at algo: 

at each time step

    t0:    bandit select top -k items out of L items.

    t2:    bandit select top -k items out of L items.     
               --->  Next step, check which item is clicked. --> reward --> update the algo.

    t3:    bandit select top -k items out of L items.


   5 or 6 algos: in this repo,
   interest only in one:   TopRank





1) run the example in the repo : only TopRANK

    https://github.dev/arita37/ranking_bandits/blob/main/README.md

    test_exp.sh

       python3 exp.py --play 2 100 -r 10 --small --TopRank 100  --horizon_time_known $TESTDIR/dev_null --force || exit
       python3 exp.py --merge 100 -r 10 --small  --TopRank 100  --horizon_time_known $TESTDIR/dev_null || exit




2) Plug the dataset : (CSV file)

   time, locationid,  itemid, is_click
                                 1
   each locationid as L itemid
       Recommend top-K items for each locationid


  Goal is to load/transform into the correct format and run the algo TopRank.
     map the CSV into correct JSON format










```




<!-- Draw horizontal rule -->
<hr>

> This contains the code used for the research articles
> * [Parametric Graph for Unimodal Ranking Bandit]() (Camille-Sovaneary Gauthier, Romaric Gaudel, Elisa Fromont, and Boammani Aser Lompo,  2021) presented at the 38$^{th}$ International Conference on Machine Learning ([ICML'21](https://icml.cc/Conferences/2021)).
> * [Bandit Algorithm for Both Unknown BestPosition and Best Item Display on Web Pages]() (Camille-Sovaneary Gauthier, Romaric Gaudel, and Elisa Fromont, 2021) presented at the 19$^{th}$ Symposium on Intelligent Data Analysis ([IDA'21](https://ida2021.org/)).


## Requirements

* Python >= 3.6
* libraries (see `requirements.txt` build with Python 3.8.7)
    * numpy
    * scipy
    * (for PMED) tensorflow 
    * (for `exp.py` and `run_experiments.py`) docopt
    * (for `run_experiments.py`) matplotlib

## (Re)run experiments

See corresponding README file:

* [README_IDA_2021.md](README_IDA_2021.md)
* [README_ICML_2021.md](README_ICML_2021.md)


```bibtex
  pdf = 	 {http://proceedings.mlr.press/v139/gauthier21a/gauthier21a.pdf},
  url = 	 {http://proceedings.mlr.press/v139/gauthier21a.html}
}
```



