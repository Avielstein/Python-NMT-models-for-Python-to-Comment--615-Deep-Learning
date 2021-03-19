# PythonCommentGenerataor
Automatic Comment Generation for Python Source Code

* **Dataset**: https://zenodo.org/record/3472050/files/code_and_comments.tar.gz?download=1
    * To set up the database, you must run the version of `initialize.py` submitted with our project. The version in that download is not compatible with python3. This will produce a ~21 GB file called `all_data.db`.
* **Dependencies**: python3, tensorflow, numpy, matplotlib, sklearn, jupyter
    * All python dependencies can be installed via `pip3 install LIBRARY`, although tensorflow seems to be easier to install via a package manager such as apt, brew, pacman, etc.
    * Our evaluation script is in a jupyter notebook so you need to install that as well.
* **Running**:
    * Open `tf_nmt_tutorial_adapted.py` and change `DB_FILE` at the top to the location of `all_data.db` on your system.
    * `python3 tf_nmt_tutorial_adapted.py` will train the model, and can also generate attention matrices. If you want to test specific code snippets, add a new line at the bottom of the `main` function that calls `translate("SNIPPET")`, and it will output an attention matrix to `figure.png`.
    * Once trained, open the `Translation_Score_metrics.ipynb` notebook and run that to generate evaluation metrics.
    * The other notebooks are not used directly for anything in our final report, but we included them to show additional work we attempted.
