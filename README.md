# ProteomicsDB-Contributions

### www.proteomicsdb.org

This repository contains all my contributions to the ProteomicsDB project hosted on GitLab.

1. All contributions were fetched from the GitLab API endpoint https://gitlab.lrz.de/api/v4/users/{USER_ID}/events and exported in a JSON file with getAllContributions.py script.
2. The JSON file was parsed and converted to a readable .txt file with convertJSONToTxt.py.
3. A GitLab-style contribution heatmap was generated from the .txt file using the generateHeatmapFromTxt.py script.
