A webpage inliner in Python
-----------------------------
This script works by checking what external resources (css, javascript, images)
a webpage references, downloading them and replacing their references with
their content. Images will be replaced by data: URI's.


Requirements
-------------
- BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/)
- Feedparser (http://www.feedparser.org/)

Example
--------

Lets say you have a webpage like this:

::


    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="style.css">
        </head>
        <body>
            <script type="text/javascript" src="script.js"></script>
            <h1>Hello world! <img src="smile.png"></h1>
        </body>
    </html>

Your *style.css* can be something like:

::

    body { background-image: url(sun.png); }
    h1 { font-size: 12px; }

and your script.js:

::

    alert("Welcome!");

Download the page and pass it through the inliner like this:

::

    python-webpage-inliner -u index.html -o index-inlined.html


and you'll get the following result:

::

    <html>
        <head>
            <style>body { background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1gEQFyQsv5MTDQAAAB10RVh0Q29tbWVudABDcmVhdGVkIHdpdGggVGhlIEdJTVDvZCVuAAADHElEQVQ4y8WVT2hcVRTGf+e+N5k/SbOQKakmtCgalLQVbaAxwk0JBGIXGVLoSkEXZqUuxE1B6CJu3InYXdwILisvySKKYKFTSIOChnahJi3UqP1DkjHpZN5kmvvucTEhjk0aRhB6Vgfuud/57rnf/S487nCTdtxN2QvN1huar3wbeMNF1vxnYBfZgovsiV1sI9tHIG2kjQCDe6x3u8gW9mP8M/CDmx6YdZG1DVVjdGRyHEofIGCsAbDXTdsZ4Bfgj0Yg2dV92s6QC4bZ9DEqt+TQ4KKGqQIY4cEqlH9XKsufwINXMXKUrMkR+7lw5HJ/I064azgJ56l6y0udrRIP9ZB/sce0dkCQhmQdjRfFL868L6vXhGNtMF+ukOi5h2FkTwVMD8xJ9+sn5chrkM5Dsoy6JUjugjowWfzNr5Hbv0LNXw8Ll483p4oOe5P8y9CS3zmYSKqe+jto7Srm8LNoth28frcXRNhwEQYYJGAMw1lp7wJ/D0iBVkG3AAeagFbRrQWkMw/ra++5KduOZyIcLc79i7GbshcwlMiarzicPYtJCaYF3boFyRKa3EH9X+A3UI1BN8GvQiuoENCZeZMW+dZN29tu0o7/w1gpYYhJtA2nXmsrAVqF5E/UpwAPvgy+BH69nqPgynVqoRgCUZzmEJ7YdXkusn0YxjSTf8ucfMeoWUJ8CfCoVsGv1Zn6tTqn1RhuVDxwkYQJ4FI4WvSPVsXkwGd6pP9d81wvWputz1c3QTdAK9vbFH5aR6v+o9Ro8XxzqhA9Jfeu4n+bBXMQtAx+eRs0BPXojXoDCXSoKRNykbUE8jQ9B2DpR3T+e6WcgeQguBysxHCtjGw4ONoGYo65yPY+Um47EcjHZEyO+fsV8f66VlcuUV45p8YYVBHVBKefEsgQ8/efqT/pZBw4vZ+7nSDRPuLkG5yeCgtXXkmdKX4IXJSutMqT6QTli/DMlQ/CQvE4W3qa2M+RMOwi270f4y7g+XCkuPCQf0xwtzZMooJnYmfzaLEI9G9b7QvAwr5escfcDYYSQhyOFJ/6336QbW1+iefzx/5H/g3sVGkFNbe16AAAAABJRU5ErkJggg==); }
            h1 { font-size:12px; }
            </style>
        </head>
        <body>
            <script>alert("Welcome!");
            </script>
            <h1>Hello world! <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA3XAAAN1wFCKJt4AAAAB3RJTUUH1QocFjcDz/359gAAA/5JREFUOMvV1W9olVUcwPHv8/9e3XW7d131bsOpbToTcRWSRVuC1cBeGOlGL4oIKZogGVhZZEiE9k8yko0IX0SlMF0QQVK4ejHJnKKTm5qrzTmdine7u/Pu/n2e55xe7Nm4drXsZQd+POc5zzmf58c55zkP/N+K8k8PD7Tdv8evx1v82li5oSZVAFsERMYNjmWc4MHmjSdf+k9wR9vKN8rM/u3KzPu0mns3aOFIHT7Lj5QO2WyS65fP0h/9WpDudRP5hdtbNh7b8a9wZ3v9/jJr8Omahi/dqurlmsj3IZxLIFIg80gkijYXzajl0oXzcqBnk5LIVR9c13q6+bbwgfYV75WZF19dsfZHpaREV9xsD4piIKWBqoKUaaSbxLXjQA7TeJjkDYcTXS/KRL76w+bW46/fEj68t9RZtGp/vqIi7Hczv3L0xAhf7DuFZVo80riUJ5qWsPOjbxkdjdHwQIj1j5diGI1ciQnRd2ITj24Y16YsdaryTXt9hww05Soqa/xO6icURWfgQpy2T16mbc825syJcObsNd7c0sSnH6xhfDwFmoIY+4HKkKW6M1a7ne31B4oyPvR51Wjtgx9rVZGRUkQMVQ+j6OHJqxYEmUM4owhnBOnGEE4M8qNoiTFUZw4XMovdP37bObHmheEyAH0K9mmjwfDs+bmO97cihQPouK7EMEwUVQMktm1j6ApSCoRroyCYVVaKnTnFmucbtctafNaUNw3rSlbxW6ZP81dS39KOz+cjGo3S2NhIMBgEoLu7m4aGBgCi0SjBYBDLsjiy91kMmUZXskrRHDvSJ9OpcdswjenF9Pl8N21F0zSn65ZloWmTa6UqCjl30iiCs25o7OrV/nR5OEImMXxHsKpODo/MW8BwLCYybuhGEZxxwl1D578zV65ey6VjnwHg9/tvgg3DKMp48Pg+5leWMzh0RGSc8OEi+KnW3hYt02VeSyTzobuqcO3sHWWcj51hQg1II/ezuq61d30RDKixVO3ugd6tRt3yZQwd2YMhJ24Lazic7HiF6nmzGejbxfV0ze5CTysYp3UeuvLLY6sWLsvGDy6aX/ck184dxee3KJtbC0A6nSYQCDDyZze93+8ksqCKi0NtDCciXc9sPr0RcABR+IEo3tYLAOF3t9zz2orFseeEuVS13IgiHRPDmolwXbKpEWx7BD0kUO3zouf38q+27Tq3A4gBSQ+XhWeFDswAQl6U7Hpryba7K3IPlVhxv6kmFYC8CMiJfHlm8Kp5fPM7594GJoC4F2kPvukQUgHDw2d64fPatIL5E4AL2EAWSHmR9trErc5j1ctcB0wP1b32qb7SG+x4UN6rT8/v7f4gihdqAfj3frLgBaLgfrr8BbfCnbnZ8qIoAAAAAElFTkSuQmCC" /></h1>
        </body>
    </html>

Now you can stash it somewhere and do neat stuff with it


Tests
-----
You can run tests via the usual

::

    python setup.py test

Which will install nose/mock for test runs.

*Note:* Tests are just starting and not all covered. Please submit more if you
can find an edge case!
