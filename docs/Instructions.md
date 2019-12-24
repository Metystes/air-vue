Instructions how to use the code
================================

In future there should be makefile to run the code below

#### Creating database:
`python src/data/createDB.py`

#### Loading data:
Code: `python -m src.data.loadDataToDB`

Req: Running 'Creating database' and having propoer data in place

Info: Data is copy from smogathon and it is kept in data/raw/smogathon_airly but becuse it is too big and git-lfs is not configured, I do not share it.

#### Training Interpolation
Code: `python -m src.models.Interpolation`

Reg: 'Creating database' and 'Loading data'

Info: Create interpolation model that can be used in Flask app.


#### Starting Flask app:
`python -m src.app.app`

Req: 'Creating database' and 'Loading data' and 'Interpolation'

Useful commends
---------------
List of useful commands

**Exporting env:**
`conda env export --from-history > environment.yml`
(--from-history list only installed packages without dependecies and it makes it more platform agnostic)

**Create env from .yml:**
`conda env create -f environment.yml` 
