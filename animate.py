import os
import json
import colorsys
from PIL import Image, ImageEnhance
import logging
from tqdm import tqdm
import imageio

# Set logging level
logging.basicConfig(level=logging.ERROR)
#logging.basicConfig(level=logging.DEBUG)

def list_images_in_inbox(inbox_folder):
    image_files = [f for f in os.listdir(inbox_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print("No images found in the inbox.")
        return None

    print("Images in the inbox:")
    for idx, file in enumerate(image_files, start=1):
        print(f"{idx}. {file}")

    return image_files

def get_image_selection(image_files):
    while True:
        try:
            selection = int(input("Enter the number of the image you want to process: "))
            if 1 <= selection <= len(image_files):
                return image_files[selection - 1]
            else:
                print(f"Please enter a number between 1 and {len(image_files)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def shift_hue(arr, hue_shift_fraction, pixel_position, image_size):
    # Unpack the original RGB values and alpha
    r, g, b, a = arr
    # Convert RGB to HLS
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    # Apply the hue shift
    h = (h + hue_shift_fraction) % 1.0
    # Convert HLS back to RGB
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    # Scale the RGB values back up to 0-255
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b, a

def calculate_hue_shift(start_hue, end_hue, frame_idx, num_frames):
    hue_range = end_hue - start_hue
    hue_shift_fraction = (start_hue + (hue_range * (frame_idx / num_frames))) % 360
    hue_shift_fraction /= 360.0  # Convert to 0-1 range
    return hue_shift_fraction

def adjust_image(original, frame_idx, num_frames, start_hue, end_hue, start_brightness, end_brightness, start_contrast, end_contrast):
    logging.debug(f"Processing frame {frame_idx}/{num_frames}")
    current_hue_shift = calculate_hue_shift(start_hue, end_hue, frame_idx, num_frames)
    # Calculate the interpolation factor for the current frame
    interpolation_factor = frame_idx / float(num_frames)
    # Linearly interpolate brightness and contrast values
    brightness_value = start_brightness + (end_brightness - start_brightness) * interpolation_factor
    contrast_value = start_contrast + (end_contrast - start_contrast) * interpolation_factor
    # Map the brightness and contrast values
    def map_brightness(value):
        if value < 0:
            return 0.1 + (value + 100) * 0.9 / 100
        elif value == 0:
            return 1
        else:
            return 1.0 + value * 1.0 / 100
    def map_contrast(value):
        if value < 0:
            return max(0.0, 1 + (value / 100.0) * 0.5)
        else:
            return 1 + (value / 100.0) * 3.0
    brightness = map_brightness(brightness_value)
    contrast = map_contrast(contrast_value)
    # Shift hue and apply adjustments to each pixel
    shifted_image = Image.new('RGBA', original.size)
    pixels = [shift_hue(original.getpixel((x, y)), current_hue_shift, (x, y), original.size)
              for y in range(original.size[1])
              for x in range(original.size[0])]
    shifted_image.putdata(pixels)
    # Apply brightness and contrast enhancements
    enhancer_brightness = ImageEnhance.Brightness(shifted_image)
    adjusted_image = enhancer_brightness.enhance(brightness)
    enhancer_contrast = ImageEnhance.Contrast(adjusted_image)
    adjusted_image = enhancer_contrast.enhance(contrast)
    return adjusted_image

def create_animated_frames(image_path, frames_folder, num_frames, start_hue, end_hue, start_brightness, end_brightness, start_contrast, end_contrast):
    original = Image.open(image_path).convert('RGBA')
    logging.debug(f"Num frames {num_frames}")
    for i in tqdm(range(num_frames), desc="Generating frames"):
        try:
            adjusted_image = adjust_image(original, i, num_frames, start_hue, end_hue, start_brightness, end_brightness, start_contrast, end_contrast)
            frame_path = os.path.join(frames_folder, f"frame_{i:03d}.png")
            adjusted_image.save(frame_path)
        except Exception as e:
            logging.error(f"Error processing frame {i}: {e}")

def create_output_files(frames_folder, output_folder, image_name, output_format, fps=30):
    if output_format in ["1", "3"]:  # 1 for GIF, 3 for Both
        frames = [Image.open(os.path.join(frames_folder, f)) for f in sorted(os.listdir(frames_folder)) if f.endswith('.png')]
        frames[0].save(os.path.join(output_folder, f'{image_name}.gif'), save_all=True, append_images=frames[1:], optimize=False, duration=40, loop=0)
    if output_format in ["2", "3"]:  # 2 for MP4, 3 for Both
        with imageio.get_writer(os.path.join(output_folder, f'{image_name}.mp4'), fps=fps) as writer:
            for frame_file in sorted(os.listdir(frames_folder)):
                if frame_file.endswith('.png'):
                    frame_path = os.path.join(frames_folder, frame_file)
                    writer.append_data(imageio.imread(frame_path))

def load_presets():
    try:
        if os.path.isfile('presets.json'):
            with open('presets.json', 'r') as file:
                data = file.read().strip()
                return json.loads(data) if data else {}
    except json.JSONDecodeError:
        logging.error("Error reading presets.json. The file may be corrupted.")
        return {}

def save_preset(name, settings):
    presets = load_presets()
    presets[name] = settings
    with open('presets.json', 'w') as file:
        json.dump(presets, file, indent=4)

def get_boolean_input(prompt):
    response = input(prompt).lower()
    return response.startswith('y')

def process_selected_image(image_file, inbox_folder, outbox_folder, num_frames, start_hue, end_hue, start_brightness, end_brightness, start_contrast, end_contrast, output_format):
    logging.info(f"Processing {image_file}")
    image_path = os.path.join(inbox_folder, image_file)
    image_name = os.path.splitext(image_file)[0]

    output_subfolder = os.path.join(outbox_folder, image_name)
    folder_suffix = 0
    while os.path.exists(output_subfolder):
        folder_suffix += 1
        output_subfolder = os.path.join(outbox_folder, f"{image_name}-{folder_suffix}")

    os.makedirs(output_subfolder, exist_ok=True)

    frames_folder = os.path.join(output_subfolder, 'frames')
    os.makedirs(frames_folder, exist_ok=True)

    create_animated_frames(image_path, frames_folder, num_frames, start_hue, end_hue, start_brightness, end_brightness, start_contrast, end_contrast)
    create_output_files(frames_folder, output_subfolder, image_name, output_format)

def get_user_input():
    presets = load_presets()
    use_preset = get_boolean_input("Would you like to use a preset? (yes/no, default no): ")
    if use_preset:
        print("Available presets:")
        for idx, name in enumerate(presets, start=1):
            print(f"{idx}. {name}")
        preset_number = input("Enter the number of the preset you'd like to use: ")
        try:
            preset_number = int(preset_number) - 1
            if preset_number < 0 or preset_number >= len(presets):
                raise IndexError
            preset_name = list(presets.keys())[preset_number]
            preset = presets[preset_name]
            num_frames = int(preset["num_frames"])
            start_hue = float(preset["start_hue"])
            end_hue = float(preset["end_hue"])
            start_brightness = float(preset["start_brightness"])
            end_brightness = float(preset["end_brightness"])
            start_contrast = float(preset["start_contrast"])
            end_contrast = float(preset["end_contrast"])
        except (IndexError, ValueError):
            print("Invalid preset number. Proceeding with manual input.")
    else:
        # Get custom inputs if not using a preset
        start_hue = float(input("Enter starting hue value (-180 to 180, default 0): ") or 0)
        end_hue = float(input("Enter ending hue value (-180 to 180, default 0): ") or 0)
        start_brightness = float(input("Enter start brightness (-100 to 100, default 0): ") or 0)
        end_brightness = float(input("Enter end brightness (-100 to 100, default 0): ") or 0)
        start_contrast = float(input("Enter start contrast (-100 to 100, default 0): ") or 0)
        end_contrast = float(input("Enter end contrast (-100 to 100, default 0): ") or 0)
        num_frames_input = input("Enter number of frames (default 120): ")
        num_frames = int(num_frames_input) if num_frames_input.isdigit() else 120

    print("Select the output format:")
    print("1. GIF")
    print("2. MP4")
    print("3. Both GIF and MP4")
    while True:
        selection = input("Enter your choice (1, 2, or 3): ")
        if selection in ["1", "2", "3"]:
            output_format = selection
            break

    return num_frames, start_hue, end_hue, start_brightness, end_brightness, start_contrast, end_contrast , output_format

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    inbox_folder = 'inbox'
    outbox_folder = 'outbox'

    if not os.path.exists(inbox_folder):
        logging.warning(f"Inbox folder '{inbox_folder}' does not exist. Creating it now.")
        os.makedirs(inbox_folder)

    if not os.path.exists(outbox_folder):
        logging.warning(f"Outbox folder '{outbox_folder}' does not exist. Creating it now.")
        os.makedirs(outbox_folder)

    image_files = list_images_in_inbox(inbox_folder)
    if image_files:
        selected_image = get_image_selection(image_files)
        num_frames, start_hue, end_hue, start_brightness, end_brightness, start_contrast, end_contrast, output_format = get_user_input()
        process_selected_image(selected_image, inbox_folder, outbox_folder, num_frames, start_hue, end_hue, start_brightness, end_brightness, start_contrast, end_contrast, output_format)

if __name__ == "__main__":
    main()
