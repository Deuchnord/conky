# Conky configuration

This repository contains my main Conky configuration.

![Screenshot of the Conky configuration with the Weather module enabled](.misc/conky.jpg)

## How to install this configuration

If you already have an existent configuration, remember to back it up. Then
clone this repository and copy the files in your `$HOME/.config/conky` folder:

```bash
git clone https://github.com/Deuchnord/conky.git
cp conky ~/.config/conky
```

Then start (or restart) Conky. That's it, your minimal configuration is ready!

## What does it contain?

The configuration is split in two parts:

- the main, default one, which needs (almost) no configuration,
- the facultative one, which needs some configuration.

### Main default configuration

The default configuration contains the following modules:

- the current date and hour,
- the RAM and CPU usage (global and per core),
- the network usage.

To make sure the _System_ and _Network_ sections work as expected, you'll most
likely have to change some things:

- **CPU:** duplicate or remove the lines 51-53 of the `conky.conf` file in
  order to have the same number of lines as the number of CPU in your
  computer.

  Remember to update the `cpuX` part of the command to get the
  right data where you expect it, and to finish the last line with the
  `$color`.

- **Network:** replace the `wlp4s0` parameter with the name of your network
  interface (you can get it with the `ip link` command) on lines 58-59
  (it's present twice per line). Change it also in the `if_existing` command
  on line 57 (this command makes the section disappear if the interface is not
  used.

  If you have several network interfaces available (e.g Ethernet and Wi-Fi),
  you can copy the lines 57-59 and put their names to show them in your Conky
  too!

### Additional modules

There are some other modules that can be enabled if you want. They are not
enabled by default, because they either need some configuration before being
used, or are not likely to work on any distribution.

#### Weather module

This module shows the current weather (current condition, temperature,
humidity) and the sunrise and sunset hours. It is based on
[OpenWeatherMap](https://openweathermap.org).

##### Activation

This module requires the [“Weather Icons”](https://erikflowers.github.io/weather-icons/)
font, which provides very nice... weather icons! If you are on Arch Linux, there
is [a package](https://aur.archlinux.org/packages/ttf-weather-icons/) on the
AUR, otherwhise download the archive on the font's website and install the TTF
file located in the `/font` folder.

First, you will have to [sign up](https://home.openweathermap.org/users/sign_up)
on OpenWeatherMap. This is necessary step to be able to call their APIs. The
free plan should be enough.
Then go to [the API keys section](https://home.openweathermap.org/api_keys) on
your account, type an app name (e.g Conky) and click _Generate_. A new line will
appear in the table: it's your sesame to use the APIs! **Don't share the key**,
it is personal!

Now, go to [OpenWeatherMap's homepage](https://openweathermap.org), search
your city in the searchbox and click on the result that corresponds to your
home. The URL should be something like this:

```
https://openweathermap.org/city/<some number>
```

The number is the unique identifier for your city. For instance, for Paris,
France, it is `2988507`.

Create a new file (name if for instance `weather.json`) and put in it the
following content:

```json
{
    "token": "your OpenWeatherMap key here",
    "language": "fr",
    "city": "your city ID here",
    "units": "metric"
}
```

You can change the language to get the weather in your own one. Here the values
will be displayed with the metric units (°C, km/h...). You can use `imperial`
instead if you are more used to the imperial units (°F, miles/h...). If you want
to stick to the International System of Units (Kelvin, m⋅s⁻¹), just
remove the `units` line and the trailing coma on the previous line.

Finally, edit the `~/.config/conky/conky.conf` file and add the following line
where you want the module to appear:

```conky
${execpi 600 python ~/.config/conky/weather.py --config ~/.config/conky/weather.json}
```

