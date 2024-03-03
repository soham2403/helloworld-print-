# StudyBuddy AI

## Team Members

- **Manas Tare**
  - *Project Manager*

- **Soham More**
  - *Fullstack Developer*

- **Adarsh Pandey**
  - *AI Specialist*

- **Amogh Parulekar**
  - *AI Specialist*

# Doubt Solver

## Overview

- **Language model:** roberta-base
- **Language:** English
- **Downstream-task:** Extractive QA
- **Training data:** SQuAD 2.0
- **Eval data:** SQuAD 2.0
- **Code:** [See an example QA pipeline on Haystack](https://github.com/deepset-ai/haystack)
- **Infrastructure:** 4x Tesla v100

## Hyperparameters

- **batch_size:** 96
- **n_epochs:** 2
- **base_LM_model:** "roberta-base"
- **max_seq_len:** 386
- **learning_rate:** 3e-5
- **lr_schedule:** LinearWarmup
- **warmup_proportion:** 0.2
- **doc_stride:** 128
- **max_query_length:** 64

# Quiz Generator
# Multi-use Assistant
