# Py Animate Hue

This script allows the user to create an animation from a still image by shifting hue, brightness, and contrast in a simple programatic way.

## Project Structure
- `animate.py`: The main script for processing images.
- `inbox/`: Folder containing sample images for processing.
- `presets.json`: File containing predefined settings for image processing.

## Demonstration

_The following gif was generated with the "huego" preset which rotates hue 360 degrees over 30 frames:_

![atwellpub_Usher_moonwalking_in_the_color_spectrum_5d77486e-a88b-4e86-9249-eb5e6fd48e6b](https://github.com/gbti-labs/py-animate-hue/assets/125175036/cdb3df08-ed40-4a76-9827-c9b7c33d7e84)

_The following mp4 was generated with the "huegolong" preset which rotates hue 360 degrees over 920 frames:_

https://github.com/gbti-labs/py-animate-hue/assets/125175036/fbb76e1f-6794-4477-8ebe-90409866f718


## Requirements
Ensure you have Python 3.x installed on your system. Dependencies are listed in `requirements.txt`, typically including:
- [Pillow (PIL Fork)](https://python-pillow.org/) - The Python Imaging Library adds image processing capabilities.
- [tqdm](https://github.com/tqdm/tqdm) - A Fast, Extensible Progress Bar for Python.
- [imageio](https://imageio.github.io/) - A Python library for reading and writing image data.

## Installation
To install the required libraries, use the following command in your project's root directory:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Script
To start the image processing, run the script from your command line:
```bash
python animate.py
```

### User Interaction and Inputs
Once the script is running, it interacts with the user through the command line interface (CLI) to collect the following inputs:

1. **Image Selection**:
   - The script lists all images in the `inbox` folder.
   - You will be prompted to enter the number corresponding to the image you wish to process.

2. **Using Presets**:
   - If presets are available (defined in `presets.json`), you can choose to apply one.
   - The script will list available presets and ask if you wish to use one.
   - Selecting a preset applies predefined settings for hue, brightness, contrast, and number of frames.

3. **Custom Settings**:
   - If not using a preset, you can customize the following settings:
      - **Hue**: Define the start and end hue values (range -180 to 180). This changes the color tone of the image.
      - **Brightness**: Set the start and end brightness levels (range -100 to 100). This affects the lightness or darkness of the image.
      - **Contrast**: Adjust the start and end contrast values (range -100 to 100). This alters the difference between dark and light areas of the image.
      - **Number of Frames**: Determines the smoothness and length of the animation (higher number for smoother animation).

### Understanding the Settings
- **Hue Shift**: Alters the color spectrum of the image, creating visually dynamic effects.
- **Brightness Adjustment**: Useful for creating a transition from dark to light or vice-versa.
- **Contrast Modification**: Enhances or reduces the sharpness and clarity of the image.
- **Number of Frames**: Affects the duration and fluidity of the resulting animation. A higher number results in a longer and smoother animation but increases processing time.

After these inputs, the script processes the selected image and saves the animated result in the `outbox` folder either as a **gif**, **mp4**, or both depending on user direction.

## Features
- Adjust hue, brightness, and contrast of images.
- Generate animated image transitions in GIF and MP4 formats.
- Use preset configurations for consistent effects.
- Interactive CLI for selecting and processing images.

## Configuration and Presets
- `presets.json` contains predefined settings.
- You can create custom presets or modify existing ones.

### Preset Examples:
- `huego`: Cycle through the color spectrum in 30 frames (good for a gif)
- `huegolong`: Same as huego but for 920 frames. (better for a mp4)
- `darktolight`: Gradually increase brightness.
- `contra`: Enhance contrast over time.
- `party`: A combination of color and contrast changes for a party-like effect.

## Contributing

Id you like our project please consider staring it and following our account for more novel applications like this one. 

Contributions to this project are welcome. Please adhere to the following steps:
1. Fork the repository.
2. Make your changes.
3. Submit a pull request.


## Follow GBTI for more

Thanks for reading! If you like our content, please consider following us!

[Twitter/X](https://twitter.com/gbtilabs) | [GitHub](https://github.com/gbti-labs) | [YouTube](https://www.youtube.com/channel/UCh4FjB6r4oWQW-QFiwqv-UA) | [Dev.to](https://dev.to/gbti) | [Daily.dev](https://dly.to/zfCriM6JfRF) | [Hashnode](https://gbti.hashnode.dev/) | [Discord](https://gbti.io)
