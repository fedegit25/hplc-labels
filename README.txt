Welcome to the database and label generator for sample analysis

Before Starting

Check you have the following programs installed:
Python 3.x
Python package manager (pip)

1. Download the 3 files in the GitHub (label7.py; read2.py; requirements.txt) 

2. Save the files to the working directory of terminal in your computer

3. Create a .csv file in the directory folder of terminal in your computer named "hplc_master_database"

4. Open a terminal window and run the following command:
pip install -r requirements.txt 
(Or install the named packages in the file manually using the command 'pip install packagenamehere')

5. Run the label generator using the following command in the terminal window:

streamlit run label7.py

6. Complete the form with the information from your sequence run and generate the barcodes for printing and the csv information that will be appended to the master file. All the successive generations will be appended there so all your data is there.

7. Open a new terminal window and start the data reader using the following command:

streamlit run read2.py

8. Input any of the 12-digit barcodes generated previously, that you can find written on the barcodes and in the master file. 
