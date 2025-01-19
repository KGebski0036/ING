PYTHON = python3
FILE_TO_TRAIN_MODEL="data/generated_logs.csv"
NUMBERS_OF_GROUP_TO_TRAIN=10000

FILE_TO_TEST_CUSTOM="data/generated_logs_test.csv"
NUMBERS_OF_GROUP_TO_TEST_CUSTOM=20000

LOGS_FOR_TEST="data/logs.csv"

HUMANIZE_LOGS_FILE="data/humanized_logs.txt"

create_model:
	@echo "Creating logs for model"
	$(PYTHON) ./scripts/logs_generator.py -f $(FILE_TO_TRAIN_MODEL) -g $(NUMBERS_OF_GROUP_TO_TRAIN)
	@echo "Creating model"
	$(PYTHON) ./scripts/create_model.py -f $(FILE_TO_TRAIN_MODEL)

test_model_custom:
	@echo "Creating logs for test"
	$(PYTHON) ./scripts/logs_generator.py -f $(FILE_TO_TEST_CUSTOM) -g $(NUMBERS_OF_GROUP_TO_TEST_CUSTOM)
	@echo "Testing model"
	$(PYTHON) ./scripts/analyze_logs.py -f $(FILE_TO_TEST_CUSTOM)

test_model:
	@echo "Testing model"
	$(PYTHON) ./scripts/analyze_logs.py -f $(LOGS_FOR_TEST)

humanize_logs:
	$(PYTHON) ./scripts/logs_humanizer.py -f $(HUMANIZE_LOGS_FILE)

clean:
	@echo "Cleaning"
	rm -rf $(FILE_TO_TRAIN_MODEL) $(FILE_TO_TEST_CUSTOM) $(HUMANIZE_LOGS_FILE) vectorizer.pkl vulnerabilities_classification_model.pth model_metadata.pkl