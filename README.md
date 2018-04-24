# Getting Started
This repository can be used to reproduce results of "Word2vec applied to Recommendation: Hyperparameters Matter".

## Usage with Docker [recommeded]

### Install

`git clone https://github.com/anonymous-authors-recsys/w2v_reco_hyperparameters_matter.git`

`cd recsys_submission_2018`

`docker build -t recsys_submission_2018 .`

### Run

`docker run -ti --rm --name=recsys_submission_2018_music_1 recsys_submission_2018:latest /bin/bash -c "python src/main.py --path_data='data/music_1.npy' --p2v=1 --window_size=3 --it=110 --sample=0.00001 --power_alpha=-0.5"`

`docker run -ti --rm --name=recsys_submission_2018_music_2 recsys_submission_2018:latest /bin/bash -c "python src/main.py --path_data='data/music_2.npy' --p2v=1 --window_size=3 --it=130 --sample=0.00001 --power_alpha=-0.5"`

`docker run -ti --rm --name=recsys_submission_2018_ecommerce recsys_submission_2018:latest /bin/bash -c "python src/main.py --path_data='data/ecommerce_sessions.npy' --p2v=1 --window_size=3 --it=140 --sample=0.001 --power_alpha=1"`

`docker run -ti --rm --name=recsys_submission_2018_kosarak recsys_submission_2018:latest /bin/bash -c "python src/main.py --path_data='data/kosarak_sessions.npy' --p2v=1 --window_size=7 --it=150 --sample=0.00001 --power_alpha=-1"`


## Usage without Docker

Install locally gensim following https://radimrehurek.com/gensim/install.html.

`git clone https://github.com/anonymous-authors-recsys/w2v_reco_hyperparameters_matter.git`

`cd w2v_reco_hyperparameters_matter`

Replace the file gensim/models/word2vec.py in your local gensim installation folder by word2vec.py.

`mkdir data`

Copy .npy files from https://drive.google.com/drive/folders/1S-vneh5-egjzjNP7y1ChdevOjukQopqX to the data folder.


### Run

`python src/main.py --path_data='data/music_1.npy' --p2v=1 --window_size=3 --it=110 --sample=0.00001 --power_alpha=-0.5`

`python src/main.py --path_data='data/music_2.npy' --p2v=1 --window_size=3 --it=130 --sample=0.00001 --power_alpha=-0.5`

`python src/main.py --path_data='data/ecommerce_sessions.npy' --p2v=1 --window_size=3 --it=140 --sample=0.001 --power_alpha=1`

`python src/main.py --path_data='data/kosarak_sessions.npy' --p2v=1 --window_size=7 --it=150 --sample=0.00001 --power_alpha=-1`
