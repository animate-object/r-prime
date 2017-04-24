## R-Prime
A rap AI


#### Start up instructions

We highly recommend you view these instructions [on github]()

As a prerequisite to run r-prime, have python 3.5.x installed on your
machine.

On windows, ensure that your Python install is on your PATH variable.

1. To run r-prime, navigate to the parent directory in cmd or git bash.
i.e. if the app is stored in `C:/Users/Tom/Programs/r-prime`, 
navigate to `C:/Users/Tom/Programs`

2. Run the command `python -m r-prime`. This should launch the
application in a window. Useful information will be printed to the
console as you run the application, so it may be helpful to monitor
both. 

    * Please note, a number of TensorFlow warnings are to be expected
    on machines that don't have the full bundle of TF support libraries
    (hd5, curses, sci py, numpy+mkl).

A few preliminary notes about r-prime in its current state:

* This application is largely unoptimized. We are relatively certain
that the various filters applied to output run in quadratic time or
less, but we wouldn't bet our lives on it. Such is the nature of a class
project.

* By far the most computationally expensive portions of our program are
the tflearn and tensorflow libraries which we wrap our application
around. The fact of the matter is that neural networks are going to be
slow on non GPU architecture. So when working with r-prime, be prepared
to wait for things to happen.

For a brief overview of our system's functionality as exposed
by our UI, see the annotated screenshots in user-guide.