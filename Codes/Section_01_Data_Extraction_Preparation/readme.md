## Overview
This section is focused on preparing files and extracting metadata. 
Run main.py in this section.

Below are the steps of file preparation and metadata extraction.

1.	Download PDF File <br>
With a csv table listing the pdf file information provided, we create a pandas Dataframe Index0 from it.
Here we download the PDF Files using the downloadable link provided in the Index0 Dataframe and saving the files to our desktop. 

2.	Rotate the PDF Files  <br>
Some pages in the PDF files for the ESA projects were rotated by 90 degrees. Extraction of data from those files can be extremely time taking. Hence, this function was used to keep the rotated PDF files in a separate folder. 

3.  Convert PDF to Pickled Files  <br>
In this section we are using the pickle library which implements binary protocols for serializing and de-serializing on the python object of the PDF files and converts teh PDF files into pickled files. The pickle data format uses a relatively compact binary representation, allowing faster processing of the files with a reduced failure rate. 

4.	Convert rotated PDF Files to rotated Pickled Files <br>
The data for the rotated pages of the PDF Files will not be extracted correctly unless the PDF files are rotated too. Hence, in this step, we are pickling the rotated PDF files too.

5.  Extract PDF Metadata  <br>
In this section, we are trying to extract some useful metadata from these PDF files.
