# Linear-and-Combinatorial-Optimization---LP-Programming

This is the final project of Konstantinos Stavropoulos for the course of Linear and Combinatorial Optimization.
It examines the problem of classifying texts in swedish and finnish language, both of which share the same alphabet.
It is inspired by the book LINEAR AND INTEGER OPTIMIZATION Theory and Practice Third Edition,by Gerard Sierksma and Yori Zwols,
and more specifically chapter 11. The analysis is based on methods of artificial intelligence and linear optimization.
To run the application you need to have installed python and pymprog (pip install pymprog).

The file tree is this

-project.py
-README
-Report - Final Project in the course Linear and Combinatorial Optimization.docx
-texts -f1.txt
	f2.txt
	f3.txt
	f4.txt
	f5.txt
	f6.txt
	f7.txt
	f8.txt
	f9.txt
	s1.txt
	s2.txt
	s3.txt
	s4.txt
	s5.txt
	s6.txt
	s7.txt
	s8.txt
	s9.txt


The theoretical analysis of the problem is in the file "Report - Final Project in the course Linear and Combinatorial Optimization.docx".
To set up the application you need to have 9 finnish texts and save them respectively to files f1.txt ... f9.txt  and 9 swedish texts
and save them to files s1.txt ... s9.txt. The application is the file project.py and it uses f1.txt ... f6.txt and s1.txt ... s6.txt for training
of the model and the other files as a test set to predict their language. It displays the predicted results for the texts in the test set, which 
are the texts f7.txt, f8.txt, f9.txt, s7.txt, s8.txt, s9.txt. It uses two models for training and displays the predicted results for both.
