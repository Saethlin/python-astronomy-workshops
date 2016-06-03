"""
A dictionary is a mapping from keys to values. They're often used to store properties of an item or to
categorize things.
"""

# Create an empty dictionary
empty_dict = dict()

# Initalize a dictionary with some keys and values
example = dict([('spam', 1), ('eggs', 2)])
print(example)
print(example['spam'])
print(example['eggs'])

# A dictionary can also be constructed by zipping together an iterable of keys and an iterable of values
keys = 'spam', 'eggs'
values = 1, 2
example = dict(zip(keys, values))

"""
To see what I mean by 'unordered', run this script a bunch of times. You'll notice that sometimes line 13 prints
{'eggs': 2, 'spam': 1} instead of using the ordering I used when I defined the dictionary
"""

print()
# key,value pairs can be added on-the-fly
example['sausage'] = 'foobararino'
print(example)

# Iterating over a dictionary with a for loop produces its keys
print('\nsimple for loop:')
for item in example:
    print(item)

# If you want the key, value pairs you'll need
print('\niterating over keys and values:')
for key, value in example.items():
    print(key, value)

# You can also work with a dictionary's keys and values individually,
print('\njust the keys:')
print(example.keys())

print('\njust the values:')
print(example.values())

# Dictionaries are also useful for counting
targets = ['HD_10700', 'HD_172167', 'HD_10700', 'HD_10700', 'HD_172167', 'HD_4478']
counter = dict()
for target in targets:
    if target in counter:
        counter[target] += 1
    else:
        counter[target] = 1
print('\ncounting example:')
print(targets)
print(counter)

# We can actually get rid of the if statement above by using defaultdict
# defaultdict takes a function that is called with no arguments to provide a default value
# if you try to access a value that does not exist. Remember that x += y requires that we evaluate x + y first
from collections import defaultdict
counter = defaultdict(int)
for target in targets:
    counter[target] += 1
print('\ncounting with defaultdict')
print(counter)

# You can also use defaultdict with lists to keep track of categories of things, such as files based on header keywords
from astropy.io import fits

image_types = defaultdict(list)
for filename in ['sample_file.fits']:
    header = fits.open(filename)[0].header
    this_imtype = header['IMAGETYP']
    image_types[this_imtype].append(filename)