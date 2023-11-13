# jatw-heron-task

#### 2023-11-06

This repo is a Flask server that takes transaction data and identifies groups of recurring transactions. 

## Usage

```bash
# Create venv
conda create -n jatw-heron-task python=3.10
conda activate jatw-heron-task

# Install requirements
pip install -r requirements.txt

# Run application
python app/main.py

# Run tests (optional)
./run_pytest.sh
```

A webpage should automatically open in your browser. Please
[click here](http://127.0.0.1:5000) if not.

Just submit your data and then hit process.

## Approach

The task is to identify recurring transactions. A robust implementation may include the following elements:

- *Data preprocessing*: Ensure consistency between entries (e.g. normalise date formats/timezones, payee
  names/descriptions, maybe even currencies)


- *Source/recipient identification*: Group transactions by a unique identifier of the source/recipient of the
  transaction. This is
  assumed to be contained within the description.

- *Temporal analysis*: For each group, try to determine a pattern in the time interval between transactions (weekly,
  monthly, etc). This may allow for varying frequencies (e.g. something used to be paid fortnightly that has switched
  to a weekly payment.) Some kind of heuristic could be used here to decide whether a recent series of transactions
  with the same interval is regular enough within the history of transactions to be considered recurring. There must be
  some number of transactions with the same amount of time between them before it can be considered recurring.

- *Amount consistency*: Check the amount of the transactions and see if they are consistent. Identical values would
  indicate a subscription or salary but variable values may be something like a company lunch. The system should be
  robust enough to handle both cases. A set of transactions with the same amount would lend more credence to the
  hypothesis of it being recurring, but we can say that variable amount transactions don't provide any evidence to the
  contrary.

- *Flagging and reporting*: Flag the identified recurring transactions and provide a report or summary of findings for
  transparency and validation of the system. There may be some low confidence predictions: a company that irregularly
  takes its employees out for lunch would have transactions with a similar description but of varying amounts and at
  irregular intervals. This could be flagged as a low confidence match.

Overall, my approach would be to build a system that incorporates multiple sources of information into a prediction of
whether a subset of transactions is happening on a recurring basis. The sources of information would be: the transaction
descriptions, amounts, and time intervals between them. By combining this information (through perhaps an ensemble
model) we can make predictions with a confidence value on whether or not a hypothesised set of recurring transactions
has been identified. A simple thresholding technique could then be used to make a decision as to whether or not a set of
transactions is recurring, and an additional benefit of having a confidence value attached is that we can flag
transactions that we think may be recurring but aren't overly confident about.

Another consideration here is that this approach relies heavily on a robust method of identifying candidate sets of
recurring transactions. For small datasets it may be feasible to do a complete enumeration style approach but for larger
ones this would be too computationally inefficient. A good MVP for finding subsets of transactions would be to just use
the description, but additional sophistication could be added to this later on by considering the other variables.

## Implementation

See the function `identify_recurring_transactions()` in file `app/ML/task.py` for a starter implementation of the above
approach. My function first identifies candidate sets of recurring transactions, and then uses models to determine
probabilities that the set is recurring based on the intervals and the amounts using an ensemble model. It finally
outputs a list of predicted recurring transaction sets with an associated probability.

I have chosen to use a pandas dataframe as the default interface for the data. This ensures a unified data format and
makes it easy to manipulate the data. The data is parsed at the API layer into a dataframe and stored as a CSV.
The API layer also contains an interface for mapping a dataframe back into JSON for display on the frontend.

## Further work / limitations

Asides from some of the functions not yet being implemented, there is much room for improvement.

- The candidate generation method should not generate sets of transactions where there are only one (or perhaps few)
  transactions
- The candidate generation should combine its outputs so that the same set is not generated twice (take the higher
  probability for duplicates)
- The ensemble model could use more features instead of just purely the confidences of the intermediary models. It also
  needs training obviously but there is plenty of scope here to build a powerful predicting model.
- The candidate generation model could use hyperparameter tweaking
- I'm going to stop writing as I've run out of time
