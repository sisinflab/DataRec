CONF = """
experiment:
  dataset: {dataset}
  data_config:
    strategy: dataset
    dataset_path: {path}
  splitting:
    strategy: fixed
    train_path: {train}
    validation_path: {val}
    test_path: {test}
  models:
    ItemKNN:
      meta:
        hyper_opt_alg: grid
        save_recs: True
      neighbors: [50, 100]
      similarity: cosine
  evaluation:
    simple_metrics: [nDCG]
  top_k: 10"""
