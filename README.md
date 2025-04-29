# Tiny Annotation Interface Maker

> [!WARNING]
> Under construction

Tooling and examples to generate and spin up a stupidly simple custom annotation web form

This is a simple library for generating static HTML frontends and database-free Flask-based backends for annotation tasks (think student annotators, Prolific crowdworkers.)

In this framework annotation interfaces have "baked-in" input reading logic. Similar to MTurk, a static set of inputs (ie., a CSV, set of hosted URLs) are iterated through purely in client-side JS.
Annotators step through all of these inputs to reach a final submit button, which submits the entire form containing all responses as a single request to a simple Flask-based backend, which writes the responses for each submission into a simple CSV.
The annotator then recieves a randomly-generated confirmation code which they can use to redeem payment, and you use as a simple way to attribute responses to annotators.

This entire system is represented in two files: an `index.prod.html` and `app.py`.

We also include a guide for rolling this system on your own Linux Apache server. You will set up a systemd job to run the backend app with gunicorn.

## Specifying the interface

You must define the following:

- **Data iterator spec**: Logic that governs how the examples that will be shown to annotators is generated.
    - **Input arguments**: Annotator-level arguments (like `https://foo.bar/form?argument1=foo&argument2=bar`) which define variations in the form depending on which annotator sees it.
    - **Presentation spec**: How the form advances as users input answers. Whether all questions are shown at once, whether the order is randomized within/across screens, etc
- **Annotator questions**: The set of annotator-supplied labels which will be generated for each datapoint. Includes type, question, and supplementary accompanying text for each answer. This implicitly defines the output CSV file
    - **Form layout**: The desired HTML logical alignment of each question (hierarchy of divs)
    - **Element design**: A small number of pre-made framework-free HTML/CSS components to implement the supported question types (or, you can take an empty generator and style the output HTML yourself!)

## Deployment Requirements

### Server

This package generates extremely simple interfaces that can be hosted in many different stacks. 
We provide a guide for hosting them on a local server running Apache.

### Gunicorn & Flask

There are many ways to host the simple `app.py` service, we will provide instructions for running it as a systemd job with gunicorn on the same local server.

### Procedurally hosted data

By "procedurally" here we mean data hosted in a simple format such that it can be described in a simple iterator.
For example, a series of images hosted at `https://<prefix_url>/images/<identifier>/image_<n>.jpg`, where `<prefix_url>` is hard-coded into the interface, `<identifier>` is provided as an html argument and `<n>` is produced in a JS loop.