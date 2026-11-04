# Rhea Soil Nutrient Prediction

Soil nutrient prediction from tabular soil samples and geospatial data, built as a post-competition practice project based on the Zindi challenge "Can you predict soil nutrient content when lab tests aren't an option?" (hosted by Zindi for Digital Africa and Rhea).

This project was completed after the challenge closed. It is not an official competition entry, and no leaderboard placing is claimed.

## Task

Predict 13 soil nutrients at locations without lab-tested samples: Al, B, Ca, Cu, Fe, K, Mg, Mn, N, Na, P, S, and Zn. The challenge is scored by a weighted RMSE.

## Data

- Challenge data: `Train.csv`, `TestSet.csv`, `SampleSubmission.csv`, `TargetPred_To_Keep.csv`, `Sample_Collection_Dates.csv`, `data_dictionary.csv`. Not redistributed here; download from the challenge page on Zindi.
- Additional data (planned): WorldClim, CHIRPS, Sentinel-2, Landsat, FAOSTAT/KNBS, and IFPRI/HarvestChoice, limited to the sources the challenge allows.

## Approach (in progress)

- One model per target nutrient
- Satellite and climate features extracted for each sample's location and date window
- Grouped cross-validation by location to avoid optimistic scores from nearby samples
- Zero-masking from `TargetPred_To_Keep.csv` applied as the final step

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Reproducibility

All random seeds are fixed in `config.yaml`. Download and preprocessing scripts are in `src/`.

## Status

- [x] Repository and environment setup
- [ ] Data exploration
- [ ] Download scripts
- [ ] Feature extraction
- [ ] Modelling and validation
- [ ] Submission generation

## License

Code: [choose a license, e.g. MIT]. Challenge data remains subject to the Zindi challenge rules.
