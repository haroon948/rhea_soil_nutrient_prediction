# Soil Nutrient Prediction from Climate and Depth Features

A post-competition practice project based on the Zindi challenge "Can you predict soil nutrient content when lab tests aren't an option?", hosted for Digital Africa and Rhea. The challenge closed before this work was done. This is not an official competition entry, and no leaderboard placement is claimed.

## Task

Predict 13 soil nutrients at test locations where no lab measurement exists: Al, B, Ca, Cu, Fe, K, Mg, Mn, N, Na, P, S, and Zn. The challenge scores a weighted RMSE, and only the entries marked 1 in `TargetPred_To_Keep.csv` are scored.

## Data

- **Challenge data:** `Train.csv`, `TestSet.csv`, `SampleSubmission.csv`, `TargetPred_To_Keep.csv`, `Sample_Collection_Dates.csv`, and `data_dictionary.csv`. These are not redistributed in this repository. Download them from the challenge page on Zindi and place them in `data/raw/`.
- **Climate data:** WorldClim 2.1 climate normals for 1970 to 2000 at 2.5 minute resolution, comprising 19 bioclimatic variables and elevation (source: worldclim.org). Check the WorldClim terms of use before reuse.

## Approach

- One LightGBM regressor per nutrient, trained only on the training rows where that nutrient was measured. The random seed is fixed at 42.
- Features: the 19 bioclimatic variables, elevation, and sampling depth. Depth labels are converted to the midpoint of their range (0 to 20 cm becomes 10, and 20 to 50 cm becomes 35).
- Raw target values. A log transform was tested and did not help: it lowered RMSE for only three nutrients, and it biased predictions low for the high-concentration samples.
- Validation uses `GroupKFold` with 5 folds, grouped by location, so samples from one site never appear in both training and validation folds.
- Negative predictions are clipped to zero. Entries marked 0 in `TargetPred_To_Keep.csv` are set to zero in the submission.

Monthly temperature and precipitation were tested as extra features. They gave no measurable gain (under 1% change for every nutrient), so they are not used in the final model.

## Results

Grouped CV RMSE with depth, and the change from the model without depth:

| Target | RMSE with depth | Change from depth |
|--------|-----------------|-------------------|
| Al | 168.55 | -0.7% |
| B | 0.069 | 0.0% |
| Ca | 1336.98 | -1.0% |
| Cu | 0.963 | 0.0% |
| Fe | 30.54 | -2.9% |
| K | 135.09 | +0.1% |
| Mg | 202.10 | -0.1% |
| Mn | 48.11 | -0.1% |
| N | 0.479 | -4.3% |
| Na | 17.93 | 0.0% |
| P | 4.217 | 0.0% |
| S | 3.371 | 0.0% |
| Zn | 0.362 | 0.0% |

Without depth, the models improve on predicting the training mean by about 45% to 48% for Al, Ca, and Mg, and by about 5% to 10% for B, Na, P, S, and Zn. The full tables are in `results/baseline_bio_raw.csv` and `results/depth_comparison.csv`.

A seed check (seeds 42, 7, and 123, with random group folds) showed run-to-run spread below 1.3% for every nutrient. Differences smaller than about 1% between experiments are therefore within noise.

## Known issues

## Known issues

- **Sparse targets.** B, Na, P, S, and Zn have about 1,900 measured rows each, and the models only slightly beat predicting the training mean for them. Their predictions carry more uncertainty than the other nutrients.
- **Test-set shift.** For P, B, and S, the average of the kept test predictions is 1.5 to 2.3 times the measured training average. Depth does not explain this. Treat these submitted values with caution until the cause is found.

## Reproducing the results

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

1. Place the challenge files in `data/raw/`.
2. Run `python src/extract_worldclim.py` to build the bioclimatic features, then `python src/extract_worldclim.py --monthly` if you want the monthly variant.
3. Run `notebooks/01_worldclim_features.ipynb` and `notebooks/03_baseline_model.ipynb` to reproduce the baseline and seed check.
4. Run `notebooks/04_final_model.qmd` to produce the depth model, the predictions, and the submission file.

Predictions and submission files are written to `results/` and are excluded from version control.

## Project structure

```
data/           challenge files and processed features (not tracked)
notebooks/      feature extraction, baseline, and final model
src/            download, extraction, and preprocessing scripts
results/        CV tables and comparison outputs
requirements.txt
```

## Status

- [x] Environment and project setup
- [x] WorldClim feature extraction
- [x] Grouped CV baseline and seed check
- [x] Depth comparison and final model
- [x] Submission file format checked

## Author

Haruna Aremu