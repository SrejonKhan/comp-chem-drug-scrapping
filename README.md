# Computational Chemistry Drug Scrapping
For our CHEM-111 Course's assignment on Computational Chemistry, we automated the process of collecting data from PubChem, SwissADME, pkCSM and putting them into CSV files.

Our plan was improvised as soon as we figured out that all the sites are dynamic and one of them (pkCSM) has redirection for computational page. **Please note that, we had not had enough time to make whole application robust. But we covered some cases that we faced during our process.**

Fun fact, this project was the first contribution in Github for many of us who have participated. Many of our peer accompanied us by joining and watching whole process in meet.

# Usage
If you want to try out this project with existing drugs list -
1. Make sure you have installed Python in your machine. 
2. Clone the project (make sure you have git installed in your machine) 
    ```console
    git clone https://github.com/SrejonKhan/comp-chem-drug-scrapping.git
    ```
3. Change current directory to that cloned folder, typically - 
    ```console
    cd comp-chem-drug-scrapping
    ```
4. Make a virtual environment - 
    ```console
    python -m venv .venv
    ```
5. Activate virtual environemnt - 
    ```console
    source .venv/Scripts/activate
    ``` 
    For windows terminal - 
    ```console
    "./.venv/Scripts/activate.bat"
    ```
6. Install all packages from requirements.txt -  
    ```console
    pip install -r requirements.txt
    ```
7. Run main.py 
    ```console
    python main.py
    ```
8. Specify drug list when it asks for - 
    ```console
    Enter path of Drug names = data/A.txt
    ```

# Contributors 
Special thanks to all contributors for their patience, interest and participating in the Pair Programming. They all did a great job in term of their first contribution to their first collab project.

Also, thanks to other peers who have joined in meet and enjoyed the process. 