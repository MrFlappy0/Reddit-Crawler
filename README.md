# Reddit Image Scraper   

## language 

# For [Fr](https://github.com/MrFlappy0/Reddit-Crawler/blob/main/readme/README%20FR.md)

## Description

Reddit Image Scraper is a Python script that allows you to download images from Reddit posts. It is capable of downloading images from external links such as Imgur.

## Features

- Downloads images from Reddit posts.
- Supports external links like Imgur.
- Handles different types of image formats (JPEG, PNG, etc.).
- Error handling for invalid URLs or inaccessible content.

## How it Works

The script works by making HTTP requests to the specified Reddit post URLs. It parses the HTML response to find the image links and then downloads the images using the `requests` library.

## Prerequisites

- Python 3.6 or higher
- Python `requests` library

## Installation

1. Ensure Python 3.6 or higher is installed on your machine.
2. Clone this repository to your local machine using `git clone https://github.com/yourusername/reddit-image-scraper.git`.
3. Install the `requests` library using pip: `pip install requests`.

## Usage

1. Open a terminal and navigate to the directory where you cloned the repository.
2. Run the Python script `reddit_scraper.py` with the URL of the Reddit post as an argument. For example: `python reddit_scraper.py https://www.reddit.com/r/examplepost`.

## Contributing

Contributions are welcome! To contribute to this project, please fork this repository, make your changes, and then open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Author

MrFlappy0 (Discord: [mrflappy0](https://discord.com/users/mrflappy0))

## Acknowledgements

Thank you for using Reddit Image/info Scraper!
