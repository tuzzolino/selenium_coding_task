<!--
*** Selenium Coding Task
*** Testing for Python Selenium Automation
-->

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps.

### Prerequisites

Note: This was tested and ran using MAC OS 11.2 and Python3

Set up a virtual environment in Python3.
* virtualenv
  ```sh
  python3 -m venv env
  ```
* Activate the virtual environment.
  ```sh
  source env/bin/activate
  ```
* Get the latest Selenium Chrome driver for your testing env from:
* https://chromedriver.chromium.org/downloads
  
1. Go into virtual env directory
  ```sh
  cd ./env/bin
  ```
2. Get the driver.
  ```sh
  wget <driver link>
  ```
3. Unzip the driver
  ```sh
  unzip chromedrive.zip
  ```
4. Delete the unneeded zip file once it has been extracted.
  ```sh
  rm chromedriver.zip
  ```
  
Get the latest Selenium Chrome driver

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/tuzzolino/selenium_coding_task.git
   ```
2. Go into the directory
  ```sh
   cd selenium_coding_task/
   ```
3. Install Python packages
   ```sh
   pip3 install requirements.txt
   ```

<!-- USAGE EXAMPLES -->
## Usage

This program run in pytest.

1. Make sure you are in the src directory:
   ```sh
   cd ./selenium_coding_task/src
   ```
2) Run Pytest
   ```sh
   python -m pytest
   ```
3) That's it. It should ruun with the following output if successful.
   ```sh
   (venv) frank.tuzzolino@frank-tuzzolino--MacBookPro16 src % python -m pytest             
=============================================================== test session starts ================================================================
platform darwin -- Python 3.8.2, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: /Users/frank.tuzzolino/selenium_coding_task/src
collected 17 items                                                                                                                                 

selenium_test.py .................                                                                                                           [100%]

========================================================== 17 passed in 62.53s (0:01:02) ===========================================================
(venv) frank.tuzzolino@frank-tuzzolino--MacBookPro16 src % 
   ```

