# Goldphish phishing server

Goldphish is a http phishing server that clones a website, modifies it and captures the POST request to extract potential credentials from it.

## Getting Started

### Installing

``` bash
pip install -r requirements.txt
```

### Basic usage

``` bash
Usage:
    goldphish <website> [options]

Arguments:
    website             The website to clone to.

Options:
    -h --help           Show this help and exit.
    -v --version        Show version and exit.

    -a <host>           Http server address.
    -p <port>           Http server port number.
    
    --ngrok             Use ngrok for local server tunneling.

    --config-restore    Restore config.ini to defaults.
    --no-banner         Dont print banner art.

By using goldphish u agree to the terms of use.
For more info read DISCLAIMER in the installation dir.
```

### Example

``` bash
python3 goldphish.py https://example.com
```

Goldphish with clone 'https://example.com' to the default cloning folder and modify html forms action attribute to prevent redirecting to real server.


### Config

You can edit goldphish's behaviour in the config.ini file.

``` ini
[http_server]
host = localhost
port = 80
custom_redirect = ; Specify a link or file for redirect after post request.

[cli]
bannerart_file = data/banner/default.txt
colored_banner = True
colored_output = True
default_hcolor = red

[cloner]
cloning_dir   = webroot ; Default cloning dir. Do not change if its not necessary
timeout_sec   = 300  ; Cancel cloning website after timeout reached
ignore_robots = True ; By set it to true you agree with terms of use
auto_clean    = True ; Clean cloning dir folder after program exit

[ngrok]
authtoken = ; Request one at https://dashboard.ngrok.com/user/signup
subdomain = ; !Note: Custom subdomain only with paid account
```

## Compatibility

Actually, goldphish is only compatible with python3.

## Requirements

* [docopt](https://github.com/docopt/docopt)
* [bs4](https://github.com/getanewsletter/BeautifulSoup4)
* [termcolor](https://github.com/hfeeki/termcolor)
* [lxml](https://github.com/lxml/lxml)

## Authors

* **Nico Duitsmann**

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details

## Disclaimer

Goldphish is for education/research purposes only.
The author takes NO responsibility and/or liability
for how you choose to use any of the tools/source
code/any files provided. The author and anyone affiliated
with will not be liable for any losses and/or damages in
connection with use of ANY files provided with goldphish.
By using goldphish or any files included, you understand
that you are AGREEING TO USE AT YOUR OWN RISK.
Once again goldphish and ALL files included are for
EDUCATION and/or RESEARCH purposes ONLY. goldphish is ONLY
intended to be used on your own pentesting labs, or with
explicit consent from the owner of the property being tested.
