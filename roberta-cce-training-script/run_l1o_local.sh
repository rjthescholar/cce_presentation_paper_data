#!/bin/bash

/home/awesomerek/UniversityOfPittsburgh/ConceptExtractionPaper/roberta-cce-training-script/main.py --labeled-path /home/awesomerek/UniversityOfPittsburgh/ConceptExtractionPaper/data_annotated/labeled_data_bio/labeled/ --val-path /home/awesomerek/UniversityOfPittsburgh/ConceptExtractionPaper/dataset_doccano/data_annotated/labeled_data_bio/dev_set/ \
  -o /home/awesomerek/UniversityOfPittsburgh/ConceptExtractionPaper/roberta-models/ &> /home/awesomerek/UniversityOfPittsburgh/ConceptExtractionPaper/experiments/new_anno_course_level_eval/roberta_l1o_train_results.txt
