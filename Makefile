NAME = eudr-webappmain
TAG = latest
REGION = eu-west-1
ACCOUNT_ID = 631990896579

.PHONY: test clean

venv:
	python3 -m venv venv/
	. venv/bin/activate

build-streamlit-app:
	cd app && docker build -t $(NAME) .

ecr-login:
	aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com

clean-ecr-repository: ecr-login
	aws ecr batch-delete-image --region $(REGION) --repository-name $(NAME) --image-ids imageTag=latest

docker-deploy: build-streamlit-app ecr-login
	docker tag $(NAME):$(TAG) $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(NAME):$(TAG)
	docker push $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(NAME):$(TAG)

docker-local-run:
	docker run -p 8501:8501 $(NAME)

run:
	cd app && python3 app.py

deploy-model-from-config:
	cd model && python model.py $(model_name)

format:
	black .

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -r {} +
	find . -name '.pytest_cache' -type d -exec rm -r {} +

test:
	mkdir -p reports/
	npm install sarif-junit@1.1.4 -g
	pip install bandit[sarif] pycodestyle
	bandit -r --configfile bandit.yaml ./app -o bandit-report.sarif
	sarif-junit -i bandit-report.sarif -o reports/bandit-report.xml
	pycodestyle --first --ignore=E121,E123,E126,E226,E24,E704,W503,W504,E501,W391 ./app/app.py && echo "OK"
	pip install -r app/requirements.txt
	cd app && python3 test_app.py && cd -
	npm install snyk@1.1292.1 -g
	snyk auth "${SNYK_TOKEN}"
	snyk ignore --id="SNYK-CC-K8S-15" --reason="private-networking"
	snyk code test app --sarif-file-output="snyk-report-code.sarif"
	sarif-junit -i snyk-report-code.sarif -o reports/snyk-report-code.xml
	snyk iac test chart/components*.yaml --policy-path=".snyk" --sarif-file-output="snyk-report-k8s.sarif" --report
	snyk iac test terraform/environment/dev/*.tf terraform/environment/uat/*.tf terraform/environment/prod/*.tf --policy-path=".snyk" --sarif-file-output="snyk-report-tf.sarif" --report
	sarif-junit -i snyk-report-k8s.sarif -o reports/snyk-report-k8s.xml
	sarif-junit -i snyk-report-tf.sarif -o reports/snyk-report-tf.xml
	ls -l reports/*.xml
	cat reports/*.xml