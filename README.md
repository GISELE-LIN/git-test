# geoCity-stress-testing
## Tree
```
.
├── README.md
├── common
│   ├── constants.py            -> Store constants
│   └── lazy_propery.py
├── locust.conf                 -> Locust configuration
├── locustfile.py               -> Locust virtual user setup
├── requirements.txt
├── setup.cfg                   -> Python module setup
├── tasks
│   ├── __init__.py
│   └── keyword_tasks.py        -> Keyword tasks class
└── users
    ├── __init__.py
    ├── stress_user.py          -> Stress user class
    └── user.py

3 directories, 12 files
```

## Installation

### Clone
```bash
git clone git@github.com:17media/keyword-stress-testing.git
cd keyword-stress-testing
```

### Install virtual environment
```bash
brew update && brew install pyenv pyenv-virtualenv
echo 'eval "$(pyenv init -)"' >> ~/.zshrc && echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc && exec $SHELL
pyenv install 3.9.10 && pyenv virtualenv 3.9.10 venv
```

### Install packages
```bash
pyenv activate venv && pip install -r requirements.txt
```

## Usage

### Run Locust
- Execute the following commnad to start locust server:
```bash
locust
```
- __Number of users__: The number of virtual users you would like to simulate
    - It would be reflected in the QPS of keyword APIs, it means if you set 100 users, the QPS would be 100 with some deviations.
- __Spawn rate__: The growth rate of user (per second)
    - To avoid high travel time, recommend: 5/s
![](./locust-server.png)

### Customization
If you would like to add / update the API you would like to test, you could go to `keyword_tasks.py` to adjust

For example, if you would like to add API:
```python

    @task
    def test_get_API(self):
        self.client.GET(
            f"{API_VERSION_PATH}/tests/testGetAPI",
            headers=self.user.api_headers,
        )

```

```python
    payload = {...}

    @task
    def test_post_API(self):
        self.client.GET(
            f"{API_VERSION_PATH}/tests/testPostAPI",
            headers=self.user.api_headers,
            data=payload
        )

```
## Datadog Monitoring
[Category Service](https://app.datadoghq.com/dashboard/ci6-9dn-63r/category-service)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)