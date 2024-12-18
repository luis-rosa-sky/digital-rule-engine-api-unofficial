# eudr-webappmain
Template version 

## Prepare environment
```bash
python3 -m virtualenv venv/
source venv/bin/activate
pip install -r app/requirements.txt
```

## Run locally
```bash
make streamlit-local-run
```

## Test
```bash
make test
```

## Deployment
Create pipelines based on the service CodeCommit repo and the three buildspec files: `buildspec.yml`, `buildspec-uat.yml` and `buildspec-prod.yml`. 