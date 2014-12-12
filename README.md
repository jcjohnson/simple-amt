simple-amt
==========
simple-amt is a microframework for working with [Amazon's Mechanical Turk](http://www.mturk.com) (AMT). It was designed with the following three principles in mind:

- Abstract away the details of AMT to let you focus on your own task.
- Place no restrictions on the structure of your AMT tasks.
- Lightweight and easy to understand.

# Quick start guide
Follow these steps to set up simple-amt and run a simple HIT on AMT.

### Check out the codebase and set up a virtualenv
```
git clone https://github.com/jcjohnson/simple-amt.git
cd simple-amt
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
```

### Configure your Amazon account
To use AMT, you'll need an Amazon AWS account. To interacti with Amazon, simple-amt needs
an access key and corresponding secret key for your Amazon account. You can find these 
[here](https://console.aws.amazon.com/iam/home?#security_credential). Once you have these,
place then in a file called config.json for simple-amt:
```
cp config.json.example config.json
# edit config.json; fill out the "aws_access_key" and "aws_secret_key" fields.
```
**WARNING**: Your AWS keys provide full access to your AWS account, so be careful about where you store your config.json file!

### Launch some HITs
We've included a sample HIT that asks workers to write sentences to describe images. To launch couple of these HITs on the AMT sandbox, run the following:
```
python launch_hits.py \
  --html_template=image_sentence.html \
  --hit_properties_file=hit_properties/image_sentence.json \
  --input_json_file=examples/image_sentence/example_input.txt \
  --hit_ids_file=examples/image_sentence/hit_ids.txt
```
This is the most complicated command that you will need to run; let's break it down:
- The file `image_sentence.html` is a simple [jinja2](http://jinja.pocoo.org/) template that defines the UI of the HIT;
you can find it in `hit_templates/image_sentence.html`.
- The file `hit_properties/image_sentence.json` defines the properties of the HIT: title, keywords, price, etc.
- The file `examples/image_sentence/example_input.txt` contains inputs for the HITs that you want to create. The input to each HIT is a JSON object, and the input file contains one such JSON object per line. One HIT is created for each line of the input file.
- The IDs of the created HITs are written to the file `examples/image_sentence/hit_ids.txt`. You will use this file as input to other commands in order to operate on the batch of HITs that you just created.

### Do your HITs
Your HITs should now be live on the [Mechanical Turk sandbox](https://workersandbox.mturk.com/mturk/findhits).
Open the sandbox and sort by "HIT creation data (newest first)".
You should see a HIT with the title "*Write sentences to describe images*" in the first page or two of results.
Complete one of the HITs.

### Check HIT progress
You can check the status of your in-progress HITs by running the following command:
```
python show_hit_progress.py --hit_ids_file=examples/image_sentence/hit_ids.txt
```

### Get HIT results
You can fetch the results of your completed HITs by running the following command:
```
python get_results.py \
  --hit_ids_file=examples/image_sentence/hit_ids.txt \
  > examples/image_sentence/results.txt
```
The results of all completed HITs are now stored as in the file `examples/image_sentence/results.txt`.
Each line of the file contains a JSON blob with the results from a single assignment.

### Approve work
If you are satisfied with the results that you have gotten, you can approve all completed assignments from your HIT batch by running the following command:
```
python approve_assignments.py --hit_ids_file=examples/image_sentence/hit_ids.txt
```

### Delete HITs
Once your HITs are completed and you have saved the results, you can delete the HITs from Amazon's database with the following command:
```
python disable_hits.py --hit_ids_file=examples/image_sentence/hit_ids.txt
```
**WARNING:** After running this command, your HITs will no longer be visible to workers, and you will no longer be able to retrieve HIT results from Amazon. Make sure that you have saved the HIT results before running this command.

### Running on the production site
To run your HITs on the production AMT site, simply append a `--prod` flag to each of the above commands.

**WARNING:** Running HITs on sandbox is free, but running HITs on the production site is not. In order to launch HITs your Mechanical Turk account must have sufficient funds to pay for all HITs; these funds will be held in escrow by Amazon once you
launch HITs, and will be paid to workers when you approve assignments. 


# Creating your own HITs
To create your own HITs, you'll need to do the following:

1. Create HTML template for HIT UI
2. Create HIT properties file
3. Prepare input file

We'll walk through each of these steps in more detail.

## Build HIT UI
Building the UI is typically the most time-consuming step in creating a new type of HIT. You will have to do most of the work yourself, but simple-amt can still help.
