import os
from astropy.io import fits
from pipeline import extract_trace, remove_cosmic_rays


class TouImage(object):

    order_width = 12
    image_hdu = 0
    output_dir = '/home/ben/pipeline_output'

    def __init__(self, path, time):
        self.path = path
        self.time = time
        self.image = None
        self.header = None
        self.extracted = None

    def __lt__(self, other):
        return self.time < other.time

    def load(self):
        hdu = fits.open(self.path)[TouImage.image_hdu]
        self.header = hdu.header
        self.image = hdu.data

    def extract(self, trace_solution, wavelength_solution):
        self.extracted = extract_trace(self.image, trace_solution, wavelength_solution, TouImage.order_width)
        self.image = None

    def save(self):
        output_path = os.path.join(TouImage.output_dir, os.path.basename(self.path))
        fits.writeto(output_path, self.extracted, header=self.header)


# Example use case, very stripped-down
image_list = []
for path in list_of_paths:
    time = fits.open(path)[0].header['MJD']
    image_list.append(TouImage(path, time))

image_list = sorted(image_list)

for image in image_list:
    image.load()
    image.extract()

remove_cosmic_rays(image_list)

for image in image_list:
    image.save()
    del image