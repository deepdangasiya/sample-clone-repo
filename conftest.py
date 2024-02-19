def pytest_addoption(parser):
    parser.addoption("--test_case", default="all", type=str,
                     help="Give test case name. "
                          "By default it tests all test cases.")
